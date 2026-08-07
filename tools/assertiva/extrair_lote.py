#!/usr/bin/env python3
"""
extrair_lote.py — ESTREIA PAGA da Assertiva (autorizada pelo dono 2026-08-06: "assertiva
autorizado, extraia via api que é barato ... puxe 100 de imóveis do triângulo histórico").

Lê tools/assertiva/alvos_lote1_100.csv (proprietario_doc,proprietario,fonte_nome,tier,sqls)
e, para cada DONO único (1 consulta por documento — nunca paga duas vezes pelo mesmo dado):
  1) Localize v3 (CPF/CNPJ) via assertiva_client;
  2) grava DIRETO no Supabase (SUPABASE_DB_URL): public.crm_lead (um por sql_mestre do dono,
     estagio 'novo', proprietario_nome + fonte primária) e public.crm_contato (telefones/
     e-mails achados, fonte='assertiva', payload bruto p/ auditoria).
O contato NUNCA entra no git (doutrina: contato fora do git; o repo guarda só o alvo).

IDEMPOTENTE: pula documento cujo lead principal já tem contato fonte='assertiva'.
Custo-consciente (1.4): --limite N corta o lote (validação começa com N pequeno).

Env: ASSERTIVA_CLIENT_ID/SECRET, SUPABASE_DB_URL.
Uso: python3 tools/assertiva/extrair_lote.py [--limite N] [--dry-run]
"""
import csv
import json
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from assertiva_client import AssertivaClient, AssertivaErro  # noqa: E402

ALVOS = Path(__file__).parent / "alvos_lote1_100.csv"


def achar_contatos(obj, saida=None, trilha=""):
    """Varre o JSON da Assertiva atrás de telefones/celulares/e-mails (estrutura por produto
    varia por conta — parser genérico, guarda também de onde veio no payload)."""
    if saida is None:
        saida = []
    if isinstance(obj, dict):
        # Forma REAL do Localize v3 (Swagger da conta, 2026-08-07): telefones vivem em
        # resposta.telefones.{fixos,moveis}[].numero — a CHAVE é 'numero' e o heurístico
        # por nome de chave não pegava (lote-100: 457 e-mails, 0 fones; 166 recuperados
        # depois por reparse SQL do payload arquivado). WhatsApp = aplicativos.whatsapp.
        if "numero" in obj and any(t in trilha.lower() for t in ("telefone", "fixos", "moveis")):
            s = str(obj.get("numero") or "").strip()
            if sum(c.isdigit() for c in s) >= 10:
                whats = bool((obj.get("aplicativos") or {}).get("whatsapp"))
                saida.append(("whatsapp" if whats else "telefone", s, trilha + "/numero"))
        for k, v in obj.items():
            kl = k.lower()
            if isinstance(v, (str, int)) and str(v).strip():
                s = str(v).strip()
                if any(t in kl for t in ("celular", "telefone", "fone", "phone", "whats")) and sum(c.isdigit() for c in s) >= 10:
                    saida.append(("whatsapp" if "whats" in kl else "telefone", s, trilha + "/" + k))
                elif "mail" in kl and "@" in s:
                    saida.append(("email", s, trilha + "/" + k))
            else:
                achar_contatos(v, saida, trilha + "/" + k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            achar_contatos(v, saida, f"{trilha}[{i}]")
    return saida


def esqueleto(obj, prof=0):
    """Estrutura SEM VALORES (chaves, tipos, tamanhos) — segura p/ commitar no git."""
    if prof > 8:
        return "..."
    if isinstance(obj, dict):
        return {k: esqueleto(v, prof + 1) for k, v in obj.items()}
    if isinstance(obj, list):
        return [esqueleto(obj[0], prof + 1)] + ([f"(+{len(obj)-1} itens)"] if len(obj) > 1 else []) if obj else []
    if isinstance(obj, str):
        return f"str({len(obj)})"
    return type(obj).__name__


def main(argv):
    limite = None
    dry = "--dry-run" in argv
    debug_estrutura = "--debug-estrutura" in argv
    if "--limite" in argv:
        limite = int(argv[argv.index("--limite") + 1])

    import psycopg  # psycopg3 (instalado no workflow)
    db_url = os.environ.get("SUPABASE_DB_URL")
    if not db_url and not dry:
        print("ERRO: SUPABASE_DB_URL ausente.")
        return 2

    alvos = list(csv.DictReader(open(ALVOS)))
    if limite:
        alvos = alvos[:limite]
    print(f"lote: {len(alvos)} donos únicos (limite={limite}, dry={dry})")

    cli = AssertivaClient()
    cli.token()
    print("auth: OK")

    consultados = pulados = leads_criados = contatos_gravados = falhas = 0
    # pooler do Supabase intermitente ('tenant not found' esporádico): retenta MUITO, com
    # backoff e alternando a porta de sessão (5432) com a de transação (6543) do Supavisor.
    con = None
    if not dry:
        # mesma vacina do carregar_tabelas_supabase.py: o tenant pode viver na frota
        # alternada do Supavisor (aws-0 <-> aws-1) — o segredo pode estar defasado
        import re as _re
        urls = [db_url]
        m = _re.search(r"aws-(\d)-", db_url)
        if m:
            alt = "0" if m.group(1) != "0" else "1"
            urls.append(_re.sub(r"aws-\d-", f"aws-{alt}-", db_url, count=1))
        if ":5432/" in db_url:
            urls += [u.replace(":5432/", ":6543/") for u in list(urls)]
        ultimo = None
        for tent in range(10):
            u = urls[tent % len(urls)]
            try:
                con = psycopg.connect(u, connect_timeout=15)
                print(f"  conexão DB OK (tentativa {tent + 1}, porta {'6543' if ':6543/' in u else '5432'})")
                break
            except Exception as e:
                ultimo = e
                print(f"  conexão DB falhou (tentativa {tent + 1}/10): {str(e)[:110]}")
                time.sleep(min(30, 4 * (tent + 1)))
        if con is None:
            print(f"ERRO: banco inacessível após 10 tentativas: {ultimo}")
            return 2
    try:
        for i, a in enumerate(alvos, 1):
            docn = a["proprietario_doc"].strip()
            sqls = [s for s in (a.get("sqls") or "").split(";") if len(s) == 10]
            if not sqls:
                continue
            if con:
                with con.cursor() as cur:
                    # idempotência: dono já consultado = tem contato assertiva OU a nota da consulta
                    cur.execute(
                        "select 1 from public.crm_lead l where l.sql_mestre = any(%s) and ("
                        " exists (select 1 from public.crm_contato c where c.lead_id=l.id and c.fonte='assertiva')"
                        " or exists (select 1 from public.crm_nota n where n.lead_id=l.id and n.texto like 'Assertiva Localize%%')"
                        ") limit 1", (sqls,))
                    if cur.fetchone():
                        pulados += 1
                        continue
            try:
                resp = cli.localizar(docn)
            except AssertivaErro as e:
                print(f"  [{i}] FALHA consulta ({str(e)[:120]})")
                falhas += 1
                time.sleep(1.0)
                continue
            # chamar() devolve (payload, http_status) — desempacota SEMPRE
            http_status = None
            if isinstance(resp, tuple):
                resp, http_status = (resp + (None,))[:2]
            if http_status is not None and http_status != 200:
                erro_txt = ""
                if isinstance(resp, dict):
                    erro_txt = str(resp.get("erro") or "")[:160]
                print(f"  [{i}] HTTP {http_status} na consulta ({erro_txt}) — pulando doc")
                falhas += 1
                time.sleep(1.0)
                continue
            consultados += 1
            if debug_estrutura and consultados == 1:
                Path(__file__).parent.joinpath("debug_estrutura.json").write_text(
                    json.dumps(esqueleto(resp), ensure_ascii=False, indent=1), encoding="utf-8")
                print("  debug_estrutura.json gravado (chaves/tipos, sem valores)")
            contatos = achar_contatos(resp)
            # dedupe por (tipo, valor-normalizado)
            vistos, unicos = set(), []
            for tipo, valor, origem in contatos:
                chave = (tipo, "".join(ch for ch in valor if ch.isalnum() or ch == "@").lower())
                if chave not in vistos:
                    vistos.add(chave)
                    unicos.append((tipo, valor, origem))
            print(f"  [{i}] doc …{docn[-4:]}: {len(unicos)} contato(s) | {len(sqls)} imóvel(is)")
            if dry or not con:
                continue
            with con.cursor() as cur:
                lead_ids = []
                for s in sqls:
                    cur.execute(
                        "insert into public.crm_lead (sql_mestre, estagio, proprietario_nome, fonte_nome) "
                        "values (%s,'novo',%s,%s) on conflict (sql_mestre) do update "
                        "set proprietario_nome=coalesce(public.crm_lead.proprietario_nome, excluded.proprietario_nome), "
                        "    fonte_nome=coalesce(public.crm_lead.fonte_nome, excluded.fonte_nome) "
                        "returning id", (s, a.get("proprietario") or None, a.get("fonte_nome") or None))
                    lead_ids.append(cur.fetchone()[0])
                    leads_criados += 1
                payload = json.dumps({"consulta": "localize/v3", "doc_final": docn[-4:], "resposta": resp},
                                     ensure_ascii=False)[:200000]
                for lid in lead_ids:
                    for tipo, valor, origem in unicos:
                        cur.execute(
                            "insert into public.crm_contato (lead_id, tipo, valor, fonte, payload) "
                            # %s::text: jsonb_build_object aceita 'any' e o psycopg não infere o tipo
                            # do parâmetro (IndeterminateDatatype na estreia do lote-2, 2026-08-07)
                            "values (%s,%s,%s,'assertiva', jsonb_build_object('origem',%s::text,'lote','lote1-triangulo'))",
                            (lid, tipo if tipo in ("telefone", "whatsapp", "email") else "telefone", valor, origem))
                        contatos_gravados += 1
                    # payload bruto completo uma vez por dono, no primeiro lead
                    if lid == lead_ids[0]:
                        cur.execute(
                            "insert into public.crm_nota (lead_id, texto) values (%s, %s)",
                            (lid, "Assertiva Localize (lote1-triângulo): payload bruto arquivado no contato; "
                                  f"{len(unicos)} contato(s) p/ {len(sqls)} imóvel(is) deste dono."))
                        cur.execute(
                            "update public.crm_contato set payload=%s::jsonb where lead_id=%s and fonte='assertiva' "
                            "and payload->>'origem' is not null and id = (select id from public.crm_contato "
                            "where lead_id=%s and fonte='assertiva' order by consultado_em limit 1)",
                            (payload, lid, lid))
            con.commit()
            time.sleep(0.4)
    finally:
        if con:
            con.close()
    print("=== FIM ===")
    print(f"consultados={consultados} pulados(idempotência)={pulados} leads={leads_criados} "
          f"contatos={contatos_gravados} falhas={falhas}")
    return 0 if falhas < max(1, consultados) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

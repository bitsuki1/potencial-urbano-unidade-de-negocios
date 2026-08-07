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


def main(argv):
    limite = None
    dry = "--dry-run" in argv
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
    # pooler do Supabase às vezes responde 'tenant not found' transitório — retenta com backoff
    con = None
    if not dry:
        ultimo = None
        for tent in range(4):
            try:
                con = psycopg.connect(db_url)
                break
            except Exception as e:
                ultimo = e
                print(f"  conexão DB falhou (tentativa {tent + 1}/4): {str(e)[:120]}")
                time.sleep(3 * (tent + 1))
        if con is None:
            print(f"ERRO: banco inacessível após 4 tentativas: {ultimo}")
            return 2
    try:
        for i, a in enumerate(alvos, 1):
            docn = a["proprietario_doc"].strip()
            sqls = [s for s in (a.get("sqls") or "").split(";") if len(s) == 10]
            if not sqls:
                continue
            if con:
                with con.cursor() as cur:
                    cur.execute(
                        "select 1 from public.crm_contato c join public.crm_lead l on l.id=c.lead_id "
                        "where c.fonte='assertiva' and l.sql_mestre = any(%s) limit 1", (sqls,))
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
            consultados += 1
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
                            "values (%s,%s,%s,'assertiva', jsonb_build_object('origem',%s,'lote','lote1-triangulo'))",
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

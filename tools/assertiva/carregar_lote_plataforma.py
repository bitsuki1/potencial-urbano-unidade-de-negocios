#!/usr/bin/env python3
"""
carregar_lote_plataforma.py — carrega no CRM o RESULTADO da Consulta em Lote da plataforma
Assertiva (o arquivo "Enriquecimento_*.csv" que o dono baixa do painel e NUNCA entra no git).

Fluxo (D-DONO 2026-08-07: a via barata é o lote): o dono sobe a lista de CNPJs no painel,
baixa o resultado e o entrega; o CSV chega ao runner por input de workflow (gzip+base64) e
este script grava em public.crm_lead / crm_contato / crm_nota — IDEMPOTENTE (re-rodar não
duplica: contato deduplicado por (lead, valor); nota por rótulo do lote).

O que entra por dono/CNPJ (minimização LGPD — só o que a prospecção usa):
  • empresa: TELEFONE1, CELULAR1, CELULAR_WHATSAPP_1, EMAIL1, EMAIL2;
  • sócios 1..3 (decisores): CELULAR_1, TELEFONE_1, EMAIL_1 (origem = "socioN:<nome>");
  • nota: razão social, situação cadastral, sócios (nome+cargo), contagem de contatos.
Campos de família/score/faturamento do layout completo são IGNORADOS de propósito.

Uso: python3 tools/assertiva/carregar_lote_plataforma.py --csv <resultado.csv> [--lote rotulo]
Env: SUPABASE_DB_URL. Mapeamento CNPJ→imóveis: tools/assertiva/alvos_lote2_radial.csv.
"""
import argparse
import csv
import re
import sys
import time
from pathlib import Path

AQUI = Path(__file__).parent
FILA = AQUI / "alvos_lote2_radial.csv"

EMPRESA = (("TELEFONE1", "telefone"), ("CELULAR1", "telefone"),
           ("CELULAR_WHATSAPP_1", "whatsapp"), ("EMAIL1", "email"), ("EMAIL2", "email"))


def _dig(s):
    return re.sub(r"\D", "", s or "")


def _ok(tipo, v):
    return ("@" in v) if tipo == "email" else len(_dig(v)) >= 10


def conectar(url):
    import psycopg
    # mesma vacina de pooler do extrair_lote.py (tenant intermitente no Supavisor)
    urls = [url]
    m = re.search(r"aws-(\d)-", url)
    if m:
        alt = "0" if m.group(1) != "0" else "1"
        urls.append(re.sub(r"aws-\d-", f"aws-{alt}-", url, count=1))
    if ":5432/" in url:
        urls += [u.replace(":5432/", ":6543/") for u in list(urls)]
    ultimo = None
    for t in range(10):
        try:
            return psycopg.connect(urls[t % len(urls)], connect_timeout=15)
        except Exception as e:
            ultimo = e
            time.sleep(min(30, 4 * (t + 1)))
    raise SystemExit(f"ERRO: banco inacessível: {ultimo}")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--lote", default="lote-plataforma")
    args = ap.parse_args(argv)

    import os
    url = os.environ.get("SUPABASE_DB_URL")
    if not url:
        print("ERRO: SUPABASE_DB_URL ausente.")
        return 2

    fila = {r["proprietario_doc"]: r for r in csv.DictReader(open(FILA, encoding="utf-8"))}
    rows = list(csv.DictReader(open(args.csv, encoding="utf-8-sig"), delimiter=";"))
    print(f"resultado do painel: {len(rows)} CNPJs ({args.csv})")

    donos = leads = contatos_n = notas = fora = 0
    con = conectar(url)
    with con:
        for r in rows:
            doc = _dig(r.get("CNPJ")).rjust(14, "0")
            alvo = fila.get(doc)
            if not alvo:
                fora += 1
                continue
            sqls = [s for s in (alvo["sqls"] or "").split(";") if len(s) == 10]
            if not sqls:
                continue
            donos += 1
            cts = []
            for campo, tipo in EMPRESA:
                v = (r.get(campo) or "").strip()
                if v and _ok(tipo, v):
                    cts.append((tipo, v, campo))
            socios = []
            for i in (1, 2, 3):
                nome = (r.get(f"SOCIO_{i}_NOME") or "").strip()
                if not nome:
                    continue
                cargo = (r.get(f"SOCIO_{i}_CARGO") or "").strip()
                socios.append(f"{nome} ({cargo})" if cargo else nome)
                for campo, tipo in ((f"SOCIO_{i}_CELULAR_1", "telefone"),
                                    (f"SOCIO_{i}_TELEFONE_1", "telefone"),
                                    (f"SOCIO_{i}_EMAIL_1", "email")):
                    v = (r.get(campo) or "").strip()
                    if v and _ok(tipo, v):
                        cts.append((tipo, v, f"socio{i}:{nome[:35]}"))
            with con.cursor() as cur:
                for s in sqls:
                    cur.execute(
                        "insert into public.crm_lead (sql_mestre, estagio, proprietario_nome, fonte_nome) "
                        "values (%s,'novo',%s,%s) on conflict (sql_mestre) do nothing",
                        (s, alvo.get("proprietario") or None, alvo.get("fonte_nome") or None))
                    if cur.rowcount:
                        leads += 1
                    for tipo, v, orig in cts:
                        cur.execute(
                            "insert into public.crm_contato (lead_id, tipo, valor, fonte, payload) "
                            "select l.id, %s, %s, 'assertiva', jsonb_build_object('origem', %s::text, 'lote', %s::text) "
                            "from public.crm_lead l where l.sql_mestre=%s "
                            "and not exists (select 1 from public.crm_contato c where c.lead_id=l.id and c.valor=%s)",
                            (tipo, v, orig, args.lote, s, v))
                        contatos_n += cur.rowcount
                nota = (f"Assertiva Localize ({args.lote}): {(r.get('RAZAO') or '').strip()} — situação "
                        f"{(r.get('SITUACAOCADASTRAL') or '').strip()}; {len(cts)} contato(s). "
                        f"Sócios (decisores): {'; '.join(socios) if socios else '—'}. "
                        f"CSV bruto do painel com o dono (LGPD/minimização — família/score ignorados).")
                cur.execute(
                    "insert into public.crm_nota (lead_id, texto) "
                    "select l.id, %s from public.crm_lead l where l.sql_mestre=%s "
                    "and not exists (select 1 from public.crm_nota x where x.lead_id=l.id "
                    "and x.texto like 'Assertiva Localize (' || %s || ')%%') limit 1",
                    (nota, sqls[0], args.lote))
                notas += cur.rowcount
            con.commit()
    print(f"donos={donos} fora_da_fila={fora} leads_novos={leads} contatos_novos={contatos_n} notas={notas}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

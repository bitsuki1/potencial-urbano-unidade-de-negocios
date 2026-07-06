#!/usr/bin/env python3
"""
sanear_duplicatas_sa.py — manda para a LIXEIRA (recuperável ~30 dias) as CÓPIAS DUPLICADAS do
Drive, mantendo SEMPRE 1 canônica por grupo. Autentica como a conta de serviço (o robô).
Dirigido pela lista AUDITADA `drive-arrumacao/LISTA-APAGAR-script.csv` (Escritório do MOU, 2026-06-20;
decisão do MOU = EXCLUIR). PU 18 · 2026-07-06.

SEGURANÇA (o saneamento APAGA — trava dupla):
- ENSAIO PRIMEIRO: DRY_RUN=true (padrão) só LISTA o que apagaria, sem tocar em nada.
- RE-VERIFICAÇÃO POR ITEM (contra IDs stale — os IDs são de 20/06 e pode ter havido re-upload):
  só marca lixeira se (a) a CANÔNICA (MANTER) do grupo EXISTE e é legível, E (b) o alvo (APAGAR)
  EXISTE, não está já na lixeira, e tem o MESMO TAMANHO da canônica (duplicata real por tamanho).
  Qualquer divergência → PULA e loga AVISO (nunca apaga na dúvida — vacina anti-perda).
- NUNCA apaga a canônica. Um item que não confirma como duplicata FICA.
- Falha por item = ERRO logado, segue (não derruba o lote). O log é lido pelo assistente pela API;
  a aceitação é a contagem/tamanho antes-depois, não este log sozinho.

Uso (CI):  DRY_RUN=true  GOOGLE_SA_KEY="$(cat sa.json)"  python3 scripts/sanear_duplicatas_sa.py
"""
import csv
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
LISTA = RAIZ / "drive-arrumacao" / "LISTA-APAGAR-script.csv"
DRY_RUN = os.environ.get("DRY_RUN", "true").strip().lower() != "false"


def _drive():
    raw = os.environ.get("GOOGLE_SA_KEY", "").strip()
    if not raw:
        print("ERRO: secret GOOGLE_SA_KEY ausente/vazio.", file=sys.stderr); sys.exit(2)
    try:
        info = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERRO: GOOGLE_SA_KEY não é JSON válido ({e}).", file=sys.stderr); sys.exit(2)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"])
    print(f"autenticado como: {info.get('client_email')} (projeto {info.get('project_id')})")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def _meta(drive, fid):
    """Devolve (existe, dict) — name/size/trashed. Não-fatal: erro => (False, motivo)."""
    try:
        m = drive.files().get(fileId=fid, fields="id,name,size,trashed,mimeType",
                              supportsAllDrives=True).execute()
        return True, m
    except Exception as e:  # noqa: BLE001
        return False, f"{type(e).__name__}: {str(e)[:120]}"


def main():
    if not LISTA.exists():
        print(f"ERRO: lista auditada ausente: {LISTA}", file=sys.stderr); sys.exit(2)
    rows = list(csv.DictReader(LISTA.open(encoding="utf-8")))
    grupos = defaultdict(lambda: {"keep": None, "trash": []})
    for r in rows:
        g = grupos[r["grupo"].strip()]
        if r["acao"].strip().upper() == "MANTER":
            g["keep"] = r["drive_id"].strip()
        elif r["acao"].strip().upper() == "APAGAR":
            g["trash"].append(r["drive_id"].strip())

    modo = "ENSAIO (DRY_RUN — nada será apagado)" if DRY_RUN else "APAGANDO (lixeira, recuperável ~30d)"
    print(f"=== sanear_duplicatas — {modo} — {len(grupos)} grupos ===")
    drive = _drive()

    trashed = skipped = err = 0
    for nome, g in grupos.items():
        keep = g["keep"]
        if not keep:
            print(f"AVISO grupo '{nome}': sem canônica (MANTER) — pulando o grupo inteiro (não apago sem canônica)")
            skipped += len(g["trash"]); continue
        ok_k, mk = _meta(drive, keep)
        if not ok_k:
            print(f"AVISO grupo '{nome}': canônica {keep} não legível ({mk}) — pulando grupo (vacina)")
            skipped += len(g["trash"]); continue
        if mk.get("trashed"):
            print(f"AVISO grupo '{nome}': canônica {keep} está na LIXEIRA — pulando (não deixaria o grupo sem cópia)")
            skipped += len(g["trash"]); continue
        keep_size = mk.get("size")  # None p/ Google-nativos
        for tid in g["trash"]:
            ok_t, mt = _meta(drive, tid)
            if not ok_t:
                print(f"PULA {nome}/{tid}: alvo não existe/ilegível ({mt})"); skipped += 1; continue
            if mt.get("trashed"):
                print(f"PULA {nome}/{tid}: já está na lixeira"); skipped += 1; continue
            if keep_size is None or mt.get("size") is None:
                print(f"PULA {nome}/{tid}: tamanho indisponível (Google-nativo?) — não confirmo duplicata"); skipped += 1; continue
            if mt.get("size") != keep_size:
                print(f"PULA {nome}/{tid}: tamanho {mt.get('size')} != canônica {keep_size} — NÃO é duplicata exata (ID stale?)"); skipped += 1; continue
            # confirmado: mesmo grupo, canônica viva, mesmo tamanho, não-lixeira
            if DRY_RUN:
                print(f"DRYRUN trash {nome}/{tid} (size {mt.get('size')}) — canônica preservada {keep}")
                trashed += 1; continue
            try:
                drive.files().update(fileId=tid, body={"trashed": True}, supportsAllDrives=True).execute()
                print(f"TRASHED {nome}/{tid} (size {mt.get('size')})"); trashed += 1
            except Exception as e:  # noqa: BLE001
                print(f"ERRO {nome}/{tid}: {type(e).__name__}: {str(e)[:140]}"); err += 1

    print(f"=== FIM === modo={'DRYRUN' if DRY_RUN else 'REAL'} "
          f"para_lixeira={trashed} pulados={skipped} erros={err}")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()

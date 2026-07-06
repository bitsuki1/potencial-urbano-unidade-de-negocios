#!/usr/bin/env python3
"""
arrumar_drive_sa.py — MOVE os arquivos da zona de despejo "01 — _entrada" para as pastas temáticas,
autenticando como a CONTA DE SERVIÇO do portfólio (o "robô" escritorio-do-mou@portfolio-do-mou),
dirigido pelo de-para AUDITADO `drive-arrumacao/de-para-COMPLETO-2026-07-04.csv`.

Por que existe (2026-07-05, PU 18): a via extensão+Apps Script provou-se frágil/insegura (um relatório
FABRICADO de "1360 movidos" quase autorizou um move real — o move NUNCA rodou, confirmado por leitura
independente do Drive). Este caminho roda no GitHub Actions e emite um LOG que o assistente lê direto
pela API — sem intermediário que possa fabricar números. A ACEITAÇÃO é a contagem da _entrada antes/depois,
não este log sozinho.

Segurança/doutrina:
- ENSAIO PRIMEIRO: DRY_RUN=true (padrão) não move nada, só planeja e conta.
- MOVE, não copia (evita duplicata, V-3). Idempotente: item já no destino = JA_OK (rodar 2x = mesmo estado).
- Multi-pai: se um arquivo tiver >1 pai, NÃO move (emite MULTI_PAI_MANUAL) — não arranca de pasta boa (A-09).
- Falha por item = ERRO logado, segue (não derruba o lote).
- Credencial: lida de os.environ['GOOGLE_SA_KEY'] (GitHub Secret, JSON). NUNCA no git.

Uso (local/CI):  DRY_RUN=true  GOOGLE_SA_KEY="$(cat sa.json)"  python3 scripts/arrumar_drive_sa.py
"""
import csv
import json
import os
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DE_PARA = RAIZ / "drive-arrumacao" / "de-para-COMPLETO-2026-07-04.csv"
DRY_RUN = os.environ.get("DRY_RUN", "true").strip().lower() != "false"   # fail-safe: só move com 'false' explícito


def _drive():
    raw = os.environ.get("GOOGLE_SA_KEY", "").strip()
    if not raw:
        print("ERRO: secret GOOGLE_SA_KEY ausente/vazio — não dá para autenticar como o robô.", file=sys.stderr)
        sys.exit(2)
    try:
        info = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERRO: GOOGLE_SA_KEY não é JSON válido ({e}).", file=sys.stderr)
        sys.exit(2)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"])
    print(f"autenticado como: {info.get('client_email')} (projeto {info.get('project_id')})")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def main():
    if not DE_PARA.exists():
        print(f"ERRO: de-para ausente: {DE_PARA}", file=sys.stderr)
        sys.exit(2)
    plano = list(csv.DictReader(DE_PARA.open(encoding="utf-8")))
    modo = "ENSAIO (DRY_RUN — nada será movido)" if DRY_RUN else "MOVENDO DE VERDADE"
    print(f"=== arrumar_drive_sa — {modo} — {len(plano)} itens no de-para ===")
    drive = _drive()

    moved = ja_ok = multi = err = 0
    for i, row in enumerate(plano, 1):
        fid = (row.get("drive_id") or "").strip()
        dest = (row.get("destino_folderId") or "").strip()
        if not fid or not dest:
            err += 1
            print(f"ERRO linha {i}: drive_id/destino_folderId vazio")
            continue
        try:
            meta = drive.files().get(fileId=fid, fields="id,parents,trashed",
                                     supportsAllDrives=True).execute()
            if meta.get("trashed"):
                err += 1
                print(f"SKIP {fid}: na lixeira")
                continue
            parents = meta.get("parents", []) or []
            if dest in parents:
                ja_ok += 1
                continue
            if len(parents) > 1:
                multi += 1
                print(f"MULTI_PAI_MANUAL {fid}: {len(parents)} pais {parents} — não movido (revisar à mão)")
                continue
            if DRY_RUN:
                moved += 1
                print(f"DRYRUN {fid} -> {dest} (de {parents or 'sem pai'})")
                continue
            drive.files().update(fileId=fid, addParents=dest,
                                 removeParents=",".join(parents) if parents else None,
                                 fields="id,parents", supportsAllDrives=True).execute()
            moved += 1
            print(f"MOVED {fid} -> {dest}")
        except Exception as e:  # noqa: BLE001 — um item ruim não pode derrubar o lote
            err += 1
            print(f"ERRO {fid}: {type(e).__name__}: {str(e)[:160]}")

    print(f"=== FIM === modo={'DRYRUN' if DRY_RUN else 'REAL'} "
          f"movidos={moved} ja_no_destino={ja_ok} multi_pai_manual={multi} erros={err} total={len(plano)}")
    # falha o job só em erro real de execução; multi_pai é ação manual esperada, não falha.
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()

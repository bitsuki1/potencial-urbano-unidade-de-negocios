#!/usr/bin/env python3
"""
selo_arrumacao_sa.py — PROVA (selo) da arrumação: lista via conta de serviço o TOPO real da pasta
POTENCIAL URBANO e reporta, para o gate do MOU:
  • as pastas de 1º nível + a contagem de FILHOS DIRETOS de cada uma (arquivo + subpasta);
  • os ARQUIVOS SOLTOS na raiz (órfãos — deve ser 0);
  • se as pastas de lixo legadas foram esvaziadas (fusão numa APAGAR só).
Read-only (não move nada). PU 19 · 2026-07-12.
"""
import os
import sys
import json
from collections import Counter

POTENCIAL_URBANO_ID = "1BrM6q36meTtn5guJoiGbqvCtZF11Uau3"
FOLDER = "application/vnd.google-apps.folder"


def _drive():
    raw = os.environ.get("GOOGLE_SA_KEY", "").strip()
    if not raw:
        print("ERRO: GOOGLE_SA_KEY ausente.", file=sys.stderr); sys.exit(2)
    info = json.loads(raw)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"])
    print(f"autenticado: {info.get('client_email')}")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def filhos(drive, parent_id):
    """(n_arquivos, n_subpastas) filhos diretos de parent_id (paginado)."""
    n_arq = n_pasta = 0
    token = None
    while True:
        r = drive.files().list(q=f"'{parent_id}' in parents and trashed = false",
                               fields="nextPageToken, files(id,mimeType)", pageSize=1000,
                               supportsAllDrives=True, includeItemsFromAllDrives=True,
                               pageToken=token).execute()
        for it in r.get("files", []):
            if it["mimeType"] == FOLDER:
                n_pasta += 1
            else:
                n_arq += 1
        token = r.get("nextPageToken")
        if not token:
            break
    return n_arq, n_pasta


def main():
    drive = _drive()
    # topo: separa pastas e arquivos soltos
    pastas, soltos = [], []
    token = None
    while True:
        r = drive.files().list(q=f"'{POTENCIAL_URBANO_ID}' in parents and trashed = false",
                               fields="nextPageToken, files(id,name,mimeType)", pageSize=1000,
                               supportsAllDrives=True, includeItemsFromAllDrives=True,
                               pageToken=token).execute()
        for it in r.get("files", []):
            (pastas if it["mimeType"] == FOLDER else soltos).append(it)
        token = r.get("nextPageToken")
        if not token:
            break

    print(f"\n=== SELO DA ARRUMAÇÃO — topo de POTENCIAL URBANO ===")
    print(f"pastas de 1º nível: {len(pastas)}  |  ARQUIVOS SOLTOS na raiz (órfãos): {len(soltos)}")
    if soltos:
        print("  ÓRFÃOS (não deveria haver):")
        for it in soltos[:30]:
            print(f"    - {it['name']}")
    print("\n== filhos diretos por pasta de topo ==")
    tot = 0
    for p in sorted(pastas, key=lambda x: x["name"]):
        na, ns = filhos(drive, p["id"])
        tot += na + ns
        flag = ""
        if "DUPLICATAS-A-EXCLUIR" in p["name"] and (na + ns) == 0:
            flag = "  ✓ VAZIA (fundida)"
        print(f"  {na:6d} arq + {ns:3d} subpasta  |  {p['name']}{flag}")
    print(f"\ntotal de filhos diretos no topo: {tot} (+ aninhados nas subpastas do 90)")
    print("SELO:", "OK — 0 órfão na raiz" if not soltos else f"ATENÇÃO — {len(soltos)} órfão(s) na raiz")


if __name__ == "__main__":
    sys.exit(main())

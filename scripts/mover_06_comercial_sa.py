#!/usr/bin/env python3
"""
mover_06_comercial_sa.py — MOVE as bases de ACHAR PROPRIETÁRIO (curadas na vistoria) para a pasta
"06 — Comercial" dentro de POTENCIAL URBANO, via conta de serviço (o robô). MOVE (não apaga) — reversível.
Fonte: inventario/drive-pu/DE-PARA-06-COMERCIAL.csv (drive_id). Idempotente. DRY_RUN ensaio primeiro. PU 19.
"""
import os
import sys
import csv
import json
import time
from pathlib import Path

POTENCIAL_URBANO_ID = "1BrM6q36meTtn5guJoiGbqvCtZF11Uau3"
DESTINO_NOME = "06 — Comercial"
DE_PARA = Path(__file__).resolve().parents[1] / "inventario" / "drive-pu" / "DE-PARA-06-COMERCIAL.csv"
DRY_RUN = os.environ.get("DRY_RUN", "true").strip().lower() != "false"


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


def achar_ou_criar(drive):
    q = (f"name = '{DESTINO_NOME}' and mimeType = 'application/vnd.google-apps.folder' "
         f"and '{POTENCIAL_URBANO_ID}' in parents and trashed = false")
    r = drive.files().list(q=q, fields="files(id,name)", supportsAllDrives=True,
                           includeItemsFromAllDrives=True).execute().get("files", [])
    if r:
        print(f"pasta '{DESTINO_NOME}' existente: {r[0]['id']}")
        return r[0]["id"]
    if DRY_RUN:
        print(f"[DRY_RUN] criaria a pasta '{DESTINO_NOME}'.")
        return None
    novo = drive.files().create(
        body={"name": DESTINO_NOME, "mimeType": "application/vnd.google-apps.folder",
              "parents": [POTENCIAL_URBANO_ID]},
        fields="id", supportsAllDrives=True).execute()
    print(f"pasta '{DESTINO_NOME}' criada: {novo['id']}")
    return novo["id"]


def carregar_ids():
    ids = []
    with open(DE_PARA, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did = (row.get("drive_id") or "").strip()
            if did:
                ids.append(did)
    vis, out = set(), []
    for d in ids:
        if d not in vis:
            vis.add(d); out.append(d)
    return out


def _mover(drive, fid, dest_id, tentativas=5):
    for i in range(tentativas):
        try:
            meta = drive.files().get(fileId=fid, fields="parents,trashed", supportsAllDrives=True).execute()
            if meta.get("trashed"):
                return "trashed"
            parents = meta.get("parents", [])
            if dest_id in parents:
                return "ja_la"
            drive.files().update(fileId=fid, addParents=dest_id,
                                 removeParents=",".join(parents) if parents else None,
                                 fields="id", supportsAllDrives=True).execute()
            return "movido"
        except Exception as e:
            code = getattr(getattr(e, "resp", None), "status", None)
            if code in (403, 429, 500, 503) and i < tentativas - 1:
                time.sleep(2 ** i); continue
            return f"erro:{code or type(e).__name__}"
    return "erro:retry"


def main():
    ids = carregar_ids()
    modo = "ENSAIO (DRY_RUN — nada move)" if DRY_RUN else "MOVENDO p/ 06 — Comercial"
    print(f"=== mover_06_comercial — {modo} — {len(ids)} bases no de-para ===")
    drive = _drive()
    dest = achar_ou_criar(drive)
    if DRY_RUN:
        print(f"[DRY_RUN] moveria {len(ids)} arquivos p/ '{DESTINO_NOME}'. Nada movido.")
        return 0
    movidos = ja = trashed = err = 0
    for n, fid in enumerate(ids, 1):
        r = _mover(drive, fid, dest)
        if r == "movido": movidos += 1
        elif r == "ja_la": ja += 1
        elif r == "trashed": trashed += 1
        else:
            err += 1
            if err <= 20:
                print(f"  ERRO {fid}: {r}")
    print(f"=== FIM === movidos={movidos} ja_la={ja} trashed={trashed} erros={err} total={len(ids)} pasta={dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

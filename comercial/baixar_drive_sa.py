#!/usr/bin/env python3
"""
baixar_drive_sa.py — baixa 1 arquivo do Drive (por id) para um caminho local, via conta de serviço
(GOOGLE_SA_KEY). Primitivo usado pela Action comercial-lista.yml. READ-ONLY no Drive. Chunked (aguenta grande).

Uso: python3 comercial/baixar_drive_sa.py <file_id> <caminho_saida>
"""
import io
import os
import sys
import json


def _drive():
    raw = os.environ.get("GOOGLE_SA_KEY", "").strip()
    if not raw:
        print("ERRO: GOOGLE_SA_KEY ausente.", file=sys.stderr); sys.exit(2)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    info = json.loads(raw)
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive.readonly"])
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def baixar(fid, saida):
    from googleapiclient.http import MediaIoBaseDownload
    drive = _drive()
    meta = drive.files().get(fileId=fid, fields="name,size,mimeType", supportsAllDrives=True).execute()
    req = drive.files().get_media(fileId=fid, supportsAllDrives=True)
    with open(saida, "wb") as fh:
        dl = MediaIoBaseDownload(fh, req, chunksize=8 * 1024 * 1024)
        done = False
        while not done:
            status, done = dl.next_chunk()
    print(f"OK: baixado {meta.get('name')} ({meta.get('size','?')} bytes) → {saida}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("uso: baixar_drive_sa.py <file_id> <caminho_saida>", file=sys.stderr); sys.exit(2)
    baixar(sys.argv[1], sys.argv[2])

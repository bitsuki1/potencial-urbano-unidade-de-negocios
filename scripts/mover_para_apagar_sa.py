#!/usr/bin/env python3
"""
mover_para_apagar_sa.py — MOVE os arquivos listados em inventario/drive-pu/APAGAR-DE-PARA.csv
para UMA pasta "APAGAR" dentro de POTENCIAL URBANO. Autentica como a conta de serviço (o robô).
PU 19 · 2026-07-12.

Por que MOVER (e não apagar): o robô (SA) é Editor — pode MOVER, mas NÃO pode mandar à lixeira
arquivo de outro dono (403). Consolida tudo numa pasta; depois o DONO abre e exclui. Nada é
apagado aqui — só reorganizado. REVERSÍVEL (o dono revisa antes de excluir).

Fonte da lista: inventario/drive-pu/APAGAR-DE-PARA.csv (coluna drive_id) — o de-para do catálogo
PU 19 (3.600 descarte + 5.378 duplicatas fortes, já com regra keep-canonical). Idempotente
(item já na pasta APAGAR = pula) e retomável (rode de novo se pausar/rate-limit).

Uso (CI):  DRY_RUN=true  GOOGLE_SA_KEY=...  python3 scripts/mover_para_apagar_sa.py
           DRY_RUN=false GOOGLE_SA_KEY=...  python3 scripts/mover_para_apagar_sa.py   # move de verdade
"""
import os
import sys
import csv
import time
from pathlib import Path

POTENCIAL_URBANO_ID = "1BrM6q36meTtn5guJoiGbqvCtZF11Uau3"   # onde criar a pasta APAGAR
APAGAR_NOME = "APAGAR — duplicados e descarte (PU 19 · 2026-07-12)"
DE_PARA = Path(__file__).resolve().parents[1] / "inventario" / "drive-pu" / "APAGAR-DE-PARA.csv"
DRY_RUN = os.environ.get("DRY_RUN", "true").strip().lower() != "false"


def _drive():
    import json
    raw = os.environ.get("GOOGLE_SA_KEY", "").strip()
    if not raw:
        print("ERRO: secret GOOGLE_SA_KEY ausente/vazio.", file=sys.stderr); sys.exit(2)
    info = json.loads(raw)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive"])
    print(f"autenticado como: {info.get('client_email')} (projeto {info.get('project_id')})")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def achar_ou_criar_apagar(drive):
    q = (f"name = '{APAGAR_NOME}' and mimeType = 'application/vnd.google-apps.folder' "
         f"and '{POTENCIAL_URBANO_ID}' in parents and trashed = false")
    r = drive.files().list(q=q, fields="files(id,name)", supportsAllDrives=True,
                           includeItemsFromAllDrives=True).execute().get("files", [])
    if r:
        print(f"pasta APAGAR existente: {r[0]['id']}")
        return r[0]["id"]
    if DRY_RUN:
        print("[DRY_RUN] criaria a pasta APAGAR (não criada agora).")
        return None
    novo = drive.files().create(
        body={"name": APAGAR_NOME, "mimeType": "application/vnd.google-apps.folder",
              "parents": [POTENCIAL_URBANO_ID]},
        fields="id", supportsAllDrives=True).execute()
    print(f"pasta APAGAR criada: {novo['id']}")
    return novo["id"]


def carregar_ids():
    ids = []
    with open(DE_PARA, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did = (row.get("drive_id") or "").strip()
            if did:
                ids.append(did)
    # dedup preservando ordem
    vistos, out = set(), []
    for d in ids:
        if d not in vistos:
            vistos.add(d); out.append(d)
    return out


def _mover_com_retry(drive, fid, apagar_id, tentativas=5):
    for i in range(tentativas):
        try:
            meta = drive.files().get(fileId=fid, fields="parents,trashed",
                                     supportsAllDrives=True).execute()
            if meta.get("trashed"):
                return "trashed"
            parents = meta.get("parents", [])
            if apagar_id in parents:
                return "ja_la"
            drive.files().update(
                fileId=fid, addParents=apagar_id,
                removeParents=",".join(parents) if parents else None,
                fields="id", supportsAllDrives=True).execute()
            return "movido"
        except Exception as e:
            code = getattr(getattr(e, "resp", None), "status", None)
            if code in (403, 429, 500, 503) and i < tentativas - 1:
                time.sleep(2 ** i)                    # backoff em rate-limit/erro transitório
                continue
            return f"erro:{code or type(e).__name__}"
    return "erro:retry"


def main():
    ids = carregar_ids()
    modo = "ENSAIO (DRY_RUN — nada será movido)" if DRY_RUN else "MOVENDO p/ APAGAR"
    print(f"=== mover_para_apagar — {modo} — {len(ids)} arquivos no de-para ===")
    drive = _drive()
    apagar_id = achar_ou_criar_apagar(drive)
    if DRY_RUN:
        print(f"[DRY_RUN] moveria {len(ids)} arquivos para a pasta APAGAR. Nada movido.")
        return 0
    movidos = ja = trashed = err = 0
    for n, fid in enumerate(ids, 1):
        r = _mover_com_retry(drive, fid, apagar_id)
        if r == "movido": movidos += 1
        elif r == "ja_la": ja += 1
        elif r == "trashed": trashed += 1
        else:
            err += 1
            if err <= 20:
                print(f"  ERRO {fid}: {r}")
        if n % 250 == 0:
            print(f"  ... {n}/{len(ids)}  movidos={movidos} ja_la={ja} trashed={trashed} erros={err}")
    print(f"=== FIM === modo=REAL movidos={movidos} ja_la={ja} trashed={trashed} erros={err} "
          f"total={len(ids)} pasta_APAGAR={apagar_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

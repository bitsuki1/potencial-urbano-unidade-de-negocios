#!/usr/bin/env python3
"""
mover_por_destino_sa.py — Executa a ARRUMAÇÃO do Drive PU: move cada arquivo de
`inventario/drive-pu/ARRUMAR-DE-PARA.csv` para a sua PASTA DESTINO canônica, dentro de POTENCIAL URBANO.
Autentica como a conta de serviço (o robô). MOVE (nunca apaga) — 100% reversível. PU 19 · 2026-07-12.

Destinos (roadmap `inventario/ROADMAP-ARRUMACAO-DRIVE-PU.md`): 00/02/03/04/05/06 canônicos, 90 material
bruto (só ideias), 99 APAGAR (pasta única — reaproveita a pasta APAGAR já criada na sessão anterior).

MODOS:
  DRY_RUN=true  (default) — ENSAIO: autentica, lista as pastas de topo REAIS, mapeia cada destino a
                 existente/ou-criaria, imprime o plano + contagem por destino. NÃO move, NÃO cria nada.
  DRY_RUN=false — REAL: cria as pastas destino que faltam (e renomeia a APAGAR legada → "99 — APAGAR"),
                 move cada arquivo (idempotente: já-no-destino = pula; retry com backoff em 403/429/5xx).

Uso (CI):  DRY_RUN=true|false  GOOGLE_SA_KEY=...  python3 scripts/mover_por_destino_sa.py
"""
import os
import sys
import csv
import json
import time
from pathlib import Path
from collections import Counter, defaultdict

POTENCIAL_URBANO_ID = "1BrM6q36meTtn5guJoiGbqvCtZF11Uau3"
DE_PARA = Path(__file__).resolve().parents[1] / "inventario" / "drive-pu" / "ARRUMAR-DE-PARA.csv"
DRY_RUN = os.environ.get("DRY_RUN", "true").strip().lower() != "false"
APAGAR_DESTINO = "99 — APAGAR (duplicados e descarte)"
# nome(s) legado(s) da pasta APAGAR já existente (sessão anterior) — reaproveitar, não criar 2ª.
APAGAR_LEGADOS = ("APAGAR — duplicados e descarte (PU 19 · 2026-07-12)", "APAGAR")


def _drive():
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


def listar_pastas_topo(drive):
    """{ nome_da_pasta: id } das subpastas diretas de POTENCIAL URBANO (paginado)."""
    pastas, token = {}, None
    q = (f"'{POTENCIAL_URBANO_ID}' in parents and mimeType = 'application/vnd.google-apps.folder' "
         f"and trashed = false")
    while True:
        r = drive.files().list(q=q, fields="nextPageToken, files(id,name)", pageSize=200,
                               supportsAllDrives=True, includeItemsFromAllDrives=True,
                               pageToken=token).execute()
        for it in r.get("files", []):
            pastas[it["name"]] = it["id"]
        token = r.get("nextPageToken")
        if not token:
            break
    return pastas


def resolver_destinos(drive, destinos, topo):
    """Mapeia cada nome-destino → id existente (ou None se precisaria criar). Trata a APAGAR legada."""
    mapa, criar = {}, []
    for d in sorted(destinos):
        if d in topo:
            mapa[d] = topo[d]
        elif d == APAGAR_DESTINO:
            leg = next((topo[n] for n in APAGAR_LEGADOS if n in topo), None)
            mapa[d] = leg          # reusa a APAGAR já existente (renomeia no real); None se não houver
            if leg is None:
                criar.append(d)
        else:
            mapa[d] = None; criar.append(d)
    return mapa, criar


def _criar_pasta(drive, nome):
    novo = drive.files().create(
        body={"name": nome, "mimeType": "application/vnd.google-apps.folder",
              "parents": [POTENCIAL_URBANO_ID]},
        fields="id", supportsAllDrives=True).execute()
    print(f"  criada: {nome} → {novo['id']}")
    return novo["id"]


def _mover(drive, fid, destino_id, tentativas=5):
    for i in range(tentativas):
        try:
            meta = drive.files().get(fileId=fid, fields="parents,trashed", supportsAllDrives=True).execute()
            if meta.get("trashed"):
                return "trashed"
            parents = meta.get("parents", [])
            if destino_id in parents:
                return "ja_la"
            drive.files().update(fileId=fid, addParents=destino_id,
                                 removeParents=",".join(parents) if parents else None,
                                 fields="id", supportsAllDrives=True).execute()
            return "movido"
        except Exception as e:
            code = getattr(getattr(e, "resp", None), "status", None)
            if code in (403, 429, 500, 503) and i < tentativas - 1:
                time.sleep(2 ** i); continue
            return f"erro:{code or type(e).__name__}"
    return "erro:retry"


def carregar_depara():
    linhas = []
    with open(DE_PARA, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did = (row.get("drive_id") or "").strip()
            dst = (row.get("destino") or "").strip()
            if did and dst:
                linhas.append((did, dst))
    # dedup por id (o conector Drive duplica; a última classificação vence)
    ult = {}
    for did, dst in linhas:
        ult[did] = dst
    return ult


def main():
    depara = carregar_depara()
    por_destino = Counter(v for v in depara.values())
    modo = "ENSAIO (DRY_RUN — nada move/cria)" if DRY_RUN else "ARRUMAÇÃO REAL"
    print(f"=== mover_por_destino — {modo} — {len(depara)} arquivos únicos no de-para ===")
    print("== contagem por destino (do de-para) ==")
    for d, n in por_destino.most_common():
        print(f"  {n:7d}  {d}")

    drive = _drive()
    topo = listar_pastas_topo(drive)
    print(f"== pastas de topo REAIS em POTENCIAL URBANO ({len(topo)}) ==")
    for n in sorted(topo):
        print(f"  • {n}")
    mapa, criar = resolver_destinos(drive, por_destino.keys(), topo)
    print("== resolução de destinos ==")
    for d in sorted(por_destino):
        est = f"existe ({mapa[d]})" if mapa[d] else "CRIARIA (não existe)"
        print(f"  [{por_destino[d]:6d}] {d}  →  {est}")

    if DRY_RUN:
        print("\n[DRY_RUN] Ensaio OK. Nada movido, nada criado.")
        print(f"[DRY_RUN] No REAL: criaria {len(criar)} pasta(s) {criar or '—'}, "
              f"renomearia a APAGAR legada → '{APAGAR_DESTINO}', e moveria até {len(depara)} arquivos "
              f"(idempotente: já-no-destino pula).")
        return 0

    # ---- REAL ----
    # 1) cria pastas destino que faltam; renomeia APAGAR legada → 99
    for d in criar:
        mapa[d] = _criar_pasta(drive, d)
    if mapa.get(APAGAR_DESTINO):
        try:
            atual = drive.files().get(fileId=mapa[APAGAR_DESTINO], fields="name", supportsAllDrives=True).execute()
            if atual.get("name") != APAGAR_DESTINO:
                drive.files().update(fileId=mapa[APAGAR_DESTINO], body={"name": APAGAR_DESTINO},
                                     fields="id", supportsAllDrives=True).execute()
                print(f"  APAGAR renomeada: '{atual.get('name')}' → '{APAGAR_DESTINO}'")
        except Exception as e:
            print(f"  aviso: não renomeou APAGAR: {e}")

    # 2) move arquivo a arquivo, agrupado por destino
    res = Counter(); erros = []
    porgrupo = defaultdict(list)
    for did, dst in depara.items():
        porgrupo[dst].append(did)
    total = len(depara); feito = 0
    for dst, ids in porgrupo.items():
        did_destino = mapa.get(dst)
        if not did_destino:
            print(f"  PULANDO grupo '{dst}' (sem pasta destino resolvida)"); continue
        for fid in ids:
            r = _mover(drive, fid, did_destino)
            res[r] += 1; feito += 1
            if r.startswith("erro") and len(erros) < 25:
                erros.append((fid, dst, r))
            if feito % 300 == 0:
                print(f"  ... {feito}/{total}  movido={res['movido']} ja_la={res['ja_la']} "
                      f"trashed={res['trashed']} erros={sum(v for k,v in res.items() if k.startswith('erro'))}")
    print(f"=== FIM REAL === movido={res['movido']} ja_la={res['ja_la']} trashed={res['trashed']} "
          f"erros={sum(v for k,v in res.items() if k.startswith('erro'))} total={total}")
    for fid, dst, r in erros:
        print(f"  ERRO {fid} → {dst}: {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

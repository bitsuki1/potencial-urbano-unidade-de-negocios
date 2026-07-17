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
BRUTO_DESTINO = "90 — Material bruto (só ideias)"
TODOS_TDC_NOME = "TODOS TDC"          # o DataLake vira o 90 (renomeado) — 22 mil SO_IDEIA já moram dentro dele
# nome(s) legado(s) da pasta APAGAR já existente — reaproveitar 1 e FUNDIR as outras (o MOU quer UMA só).
APAGAR_LEGADOS = ("APAGAR — duplicados e descarte (PU 19 · 2026-07-12)", "APAGAR")
APAGAR_FUNDIR = ("99 — DUPLICATAS-A-EXCLUIR",)   # 2ª pasta de lixo → esvaziar dentro da única APAGAR


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
    """Mapeia cada nome-destino → id existente (ou None se precisaria criar). Reaproveita:
      • 99 APAGAR → pasta APAGAR legada (renomeia no real p/ 99; funde a 2ª pasta de lixo);
      • 90 Material bruto → a pasta TODOS TDC RENOMEADA (o DataLake já guarda os 22 mil SO_IDEIA)."""
    mapa, criar = {}, []
    for d in sorted(destinos):
        if d in topo:
            mapa[d] = topo[d]
        elif d == APAGAR_DESTINO:
            leg = next((topo[n] for n in APAGAR_LEGADOS if n in topo), None)
            mapa[d] = leg
            if leg is None:
                criar.append(d)
        elif d == BRUTO_DESTINO:
            leg = topo.get(TODOS_TDC_NOME) or topo.get(BRUTO_DESTINO)
            mapa[d] = leg          # renomeia TODOS TDC → 90 no real; None só se nem TODOS TDC existir
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
    """{ drive_id: (destino, dentro_todos_tdc) } — dedup por id (a última classificação vence)."""
    ult = {}
    with open(DE_PARA, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did = (row.get("drive_id") or "").strip()
            dst = (row.get("destino") or "").strip()
            dentro = (row.get("dentro_todos_tdc") or "").strip().upper() == "SIM"
            if did and dst:
                ult[did] = (dst, dentro)
    return ult


def main():
    depara = carregar_depara()                       # {id: (destino, dentro)}
    por_destino = Counter(dst for dst, _ in depara.values())
    # OTIMIZAÇÃO: 90-bound que JÁ está dentro do TODOS TDC (=90 renomeado) não se move (fica aninhado).
    mover_ct = Counter()
    for dst, dentro in depara.values():
        if dst == BRUTO_DESTINO and dentro:
            continue                                 # fica onde está (dentro do 90 renomeado)
        mover_ct[dst] += 1
    a_mover = sum(mover_ct.values())
    modo = "ENSAIO (DRY_RUN — nada move/cria)" if DRY_RUN else "ARRUMAÇÃO REAL"
    print(f"=== mover_por_destino — {modo} — {len(depara)} arquivos únicos no de-para ===")
    print("== contagem por destino (do de-para) / a MOVER (após otimização TODOS TDC→90) ==")
    for d, n in por_destino.most_common():
        print(f"  destino={n:7d}  a_mover={mover_ct.get(d,0):7d}  {d}")
    print(f"  TOTAL a mover: {a_mover}  (economia: {len(depara)-a_mover} já-no-lugar dentro do 90)")

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
    fundir_ids = [topo[n] for n in APAGAR_FUNDIR if n in topo]
    if fundir_ids:
        print(f"  fusão de lixo: {list(APAGAR_FUNDIR)} → esvaziar dentro da única APAGAR")

    if DRY_RUN:
        print("\n[DRY_RUN] Ensaio OK. Nada movido, nada criado.")
        print(f"[DRY_RUN] No REAL: renomearia '{TODOS_TDC_NOME}'→'{BRUTO_DESTINO}' e a APAGAR legada→"
              f"'{APAGAR_DESTINO}', fundiria {len(fundir_ids)} pasta(s) de lixo, criaria {len(criar)} "
              f"pasta(s) {criar or '—'}, e moveria ~{a_mover} arquivos (idempotente).")
        return 0

    # ---- REAL ----
    for d in criar:
        mapa[d] = _criar_pasta(drive, d)
    # renomeia TODOS TDC → 90 e APAGAR legada → 99 (nomes canônicos; o MOU quer 1 de cada)
    for destino_nome, key in ((BRUTO_DESTINO, BRUTO_DESTINO), (APAGAR_DESTINO, APAGAR_DESTINO)):
        fid = mapa.get(key)
        if fid:
            try:
                atual = drive.files().get(fileId=fid, fields="name", supportsAllDrives=True).execute()
                if atual.get("name") != destino_nome:
                    drive.files().update(fileId=fid, body={"name": destino_nome}, fields="id",
                                         supportsAllDrives=True).execute()
                    print(f"  renomeada: '{atual.get('name')}' → '{destino_nome}'")
            except Exception as e:
                print(f"  aviso: não renomeou {destino_nome}: {e}")

    # move arquivo a arquivo (pulando os 90-já-dentro)
    res = Counter(); erros = []
    porgrupo = defaultdict(list)
    for did, (dst, dentro) in depara.items():
        if dst == BRUTO_DESTINO and dentro:
            res["fica_no_90"] += 1; continue
        porgrupo[dst].append(did)
    total = sum(len(v) for v in porgrupo.values()); feito = 0
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

    # funde a 2ª pasta de lixo: move seus filhos diretos p/ a única APAGAR
    apagar_id = mapa.get(APAGAR_DESTINO)
    for lid in fundir_ids:
        if not apagar_id:
            break
        token = None
        while True:
            r = drive.files().list(q=f"'{lid}' in parents and trashed = false",
                                   fields="nextPageToken, files(id)", pageSize=200,
                                   supportsAllDrives=True, includeItemsFromAllDrives=True,
                                   pageToken=token).execute()
            for it in r.get("files", []):
                rr = _mover(drive, it["id"], apagar_id); res[f"fusao_{rr}"] += 1
            token = r.get("nextPageToken")
            if not token:
                break

    print(f"=== FIM REAL === movido={res['movido']} ja_la={res['ja_la']} trashed={res['trashed']} "
          f"fica_no_90={res['fica_no_90']} erros={sum(v for k,v in res.items() if k.startswith('erro'))} total_movido={total}")
    print("  fusão lixo:", {k: v for k, v in res.items() if k.startswith('fusao_')})
    for fid, dst, r in erros:
        print(f"  ERRO {fid} → {dst}: {r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

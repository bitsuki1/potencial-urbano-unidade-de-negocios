#!/usr/bin/env python3
"""
dedup_quarentena_sa.py — MOVE as cópias duplicadas do Drive para UMA pasta de quarentena,
mantendo 1 canônica por grupo. Autentica como a conta de serviço (o robô). PU 18 · 2026-07-06.

Por que MOVER (e não apagar): o robô é Editor — pode MOVER (provado: 1.360 arquivos) mas NÃO
pode mandar para a lixeira arquivo de outro dono (403). Então consolida todas as duplicatas numa
pasta `99 — DUPLICATAS-A-EXCLUIR`; depois o DONO abre a pasta, seleciona tudo e exclui (ele é o
dono dos arquivos → funciona). Nada é apagado por este script — só reorganizado.

Critério (igual ao dedup_scan): grupos por (nome IDÊNTICO + tamanho IDÊNTICO), só ≥ SIZE_MIN.
Canônica mantida: a que está em "03 — Tabelas" (1v4H2Ys...) senão a mais antiga. Idempotente
(item já na quarentena = pula) e retomável (rode de novo se pausar).

Uso (CI):  DRY_RUN=true  GOOGLE_SA_KEY=...  python3 scripts/dedup_quarentena_sa.py
"""
import os
import sys
from collections import defaultdict

SIZE_MIN = 1_000_000
TABELAS_ID = "1v4H2YsIZSNDwNXiMtOAV1w1qy-5kOuvy"          # "03 — Tabelas & Engines" (canônicas)
POTENCIAL_URBANO_ID = "1BrM6q36meTtn5guJoiGbqvCtZF11Uau3"  # onde criar a pasta de quarentena
QUARENTENA_NOME = "99 — DUPLICATAS-A-EXCLUIR"
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


def _list_all(drive, q, fields):
    out, tok = [], None
    while True:
        resp = drive.files().list(
            q=q, spaces="drive", fields=f"nextPageToken, {fields}",
            pageSize=1000, pageToken=tok,
            includeItemsFromAllDrives=True, supportsAllDrives=True, corpora="allDrives").execute()
        out.extend(resp.get("files", []))
        tok = resp.get("nextPageToken")
        if not tok:
            break
    return out


def pastas_sob(drive, raiz):
    """Conjunto de IDs de pasta que são DESCENDENTES de `raiz` (inclui raiz). Enumera todas as
    pastas 1×, monta o mapa pai→filhos e faz BFS. Serve p/ ESCOPAR o dedup só à subárvore do
    Potencial Urbano — o robô enxerga o portfólio inteiro (todas as unidades), e não queremos
    mexer nas outras."""
    folders = _list_all(drive, "mimeType = 'application/vnd.google-apps.folder' and trashed = false",
                        "files(id,parents)")
    filhos = defaultdict(list)
    for f in folders:
        for p in (f.get("parents") or []):
            filhos[p].append(f["id"])
    sob, fila = {raiz}, [raiz]
    while fila:
        cur = fila.pop()
        for c in filhos.get(cur, []):
            if c not in sob:
                sob.add(c); fila.append(c)
    return sob


def enumerar(drive):
    """Arquivos (não-lixeira, não-pasta) DENTRO da subárvore do Potencial Urbano (escopo)."""
    sob = pastas_sob(drive, POTENCIAL_URBANO_ID)
    print(f"pastas na subárvore do Potencial Urbano: {len(sob)}")
    todos = _list_all(drive, "trashed = false and mimeType != 'application/vnd.google-apps.folder'",
                      "files(id,name,size,parents,createdTime)")
    files = [f for f in todos if any(p in sob for p in (f.get("parents") or []))]
    print(f"enumerados no portfólio: {len(todos)} · dentro do Potencial Urbano: {len(files)}")
    return files


def achar_ou_criar_quarentena(drive):
    q = (f"name = '{QUARENTENA_NOME}' and mimeType = 'application/vnd.google-apps.folder' "
         f"and '{POTENCIAL_URBANO_ID}' in parents and trashed = false")
    r = drive.files().list(q=q, fields="files(id,name)", supportsAllDrives=True,
                           includeItemsFromAllDrives=True).execute().get("files", [])
    if r:
        print(f"quarentena existente: {r[0]['id']}")
        return r[0]["id"]
    if DRY_RUN:
        print(f"[ENSAIO] criaria a pasta '{QUARENTENA_NOME}' em {POTENCIAL_URBANO_ID}")
        return "QUARENTENA_DRYRUN"
    novo = drive.files().create(
        body={"name": QUARENTENA_NOME, "mimeType": "application/vnd.google-apps.folder",
              "parents": [POTENCIAL_URBANO_ID]},
        fields="id", supportsAllDrives=True).execute()
    print(f"quarentena criada: {novo['id']}")
    return novo["id"]


def main():
    drive = _drive()
    files = enumerar(drive)

    grupos = defaultdict(list)
    for f in files:
        if f.get("size"):
            grupos[(f["name"], f["size"])].append(f)

    dups_por_grupo = []
    for (nome, sz), membros in grupos.items():
        if len(membros) < 2 or int(sz) < SIZE_MIN:
            continue
        na_tab = [m for m in membros if TABELAS_ID in (m.get("parents") or [])]
        keep = na_tab[0] if na_tab else sorted(membros, key=lambda m: m.get("createdTime", ""))[0]
        trash = [m for m in membros if m["id"] != keep["id"]]
        dups_por_grupo.append((nome, int(sz), trash))

    total = sum(len(t) for _, _, t in dups_por_grupo)
    gb = sum(sz * len(t) for _, sz, t in dups_por_grupo) / 1073741824
    modo = "ENSAIO (DRY_RUN — nada será movido)" if DRY_RUN else "MOVENDO p/ quarentena"
    print(f"=== dedup_quarentena — {modo} — {len(dups_por_grupo)} grupos, {total} duplicatas, ~{gb:.2f} GB ===")

    quar = achar_ou_criar_quarentena(drive)
    movidos = ja = err = 0
    for nome, sz, trash in dups_por_grupo:
        for m in trash:
            parents = m.get("parents", []) or []
            if quar in parents:
                ja += 1; continue
            if DRY_RUN:
                movidos += 1; continue
            try:
                drive.files().update(fileId=m["id"], addParents=quar,
                                     removeParents=",".join(parents) if parents else None,
                                     fields="id", supportsAllDrives=True).execute()
                movidos += 1
            except Exception as e:  # noqa: BLE001
                err += 1
                print(f"ERRO mover {m['id']} ({nome}): {type(e).__name__}: {str(e)[:120]}")

    print(f"=== FIM === modo={'DRYRUN' if DRY_RUN else 'REAL'} "
          f"para_quarentena={movidos} ja_la={ja} erros={err} "
          f"grupos={len(dups_por_grupo)} recuperavel_GB={gb:.2f}")


if __name__ == "__main__":
    main()

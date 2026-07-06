#!/usr/bin/env python3
"""
dedup_scan_sa.py — VARREDURA de duplicatas do Drive (SÓ RELATÓRIO — nunca apaga).
Autentica como a conta de serviço (o robô), enumera tudo que ela enxerga, agrupa por
(nome IDÊNTICO + tamanho IDÊNTICO) e reporta os grupos com ≥2 cópias: qual MANTER e quais
seriam duplicatas para excluir, + os GB recuperáveis. PU 18 · 2026-07-06.

Por que só relatório: o robô é Editor e NÃO pode mandar para a lixeira (403 — só o dono).
Então esta Action LISTA; o assistente lê o log e gera um `Trash-*.gs` que o DONO roda.

Escolha da canônica por grupo (determinística):
  1) se algum membro está na pasta "03 — Tabelas & Engines" (1v4H2Ys...), mantém esse;
  2) senão, mantém o de createdTime mais antigo.
Segurança:
  - name+size idênticos = duplicata de alta confiança (byte-idêntico p/ arquivos grandes).
  - AUTO-LISTA p/ exclusão só grupos com tamanho ≥ SIZE_MIN (1 MB) — os pequenos ficam
    só reportados p/ revisão manual (evita falso-positivo de arquivinho coincidente).
  - ignora pastas e arquivos Google-nativos (sem tamanho confiável).
"""
import os
import sys
from collections import defaultdict

SIZE_MIN = 1_000_000          # 1 MB — só auto-lista dup grande; menores = revisar à mão
TABELAS_ID = "1v4H2YsIZSNDwNXiMtOAV1w1qy-5kOuvy"   # "03 — Tabelas & Engines" (onde vivem as canônicas)


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


def enumerar(drive):
    files, tok = [], None
    q = "trashed = false and mimeType != 'application/vnd.google-apps.folder'"
    while True:
        resp = drive.files().list(
            q=q, spaces="drive",
            fields="nextPageToken, files(id,name,size,parents,createdTime,mimeType)",
            pageSize=1000, pageToken=tok,
            includeItemsFromAllDrives=True, supportsAllDrives=True, corpora="allDrives").execute()
        files.extend(resp.get("files", []))
        tok = resp.get("nextPageToken")
        if not tok:
            break
    return files


def main():
    drive = _drive()
    files = enumerar(drive)
    print(f"enumerados: {len(files)} arquivos (não-lixeira, não-pasta)")

    grupos = defaultdict(list)
    for f in files:
        sz = f.get("size")
        if not sz:                      # Google-nativo / sem tamanho -> ignora (não confia)
            continue
        grupos[(f["name"], sz)].append(f)

    dups = {k: v for k, v in grupos.items() if len(v) > 1}
    big, small = [], []
    total_bytes = 0
    for (nome, sz), membros in sorted(dups.items(), key=lambda kv: -int(kv[0][1]) * (len(kv[1]) - 1)):
        # canônica: preferir a que está em 03-Tabelas; senão a mais antiga
        na_tabela = [m for m in membros if TABELAS_ID in (m.get("parents") or [])]
        keep = (na_tabela[0] if na_tabela
                else sorted(membros, key=lambda m: m.get("createdTime", ""))[0])
        trash = [m for m in membros if m["id"] != keep["id"]]
        ganho = int(sz) * len(trash)
        rec = (nome, int(sz), keep, trash, ganho)
        if int(sz) >= SIZE_MIN:
            big.append(rec); total_bytes += ganho
        else:
            small.append(rec)

    print(f"\n=== GRUPOS DE DUPLICATA (nome+tamanho idênticos) ===")
    print(f"grandes (≥1MB, auto-listados): {len(big)} · pequenos (revisar à mão): {len(small)}")
    print(f"\n--- GRANDES (recuperável ~{total_bytes/1073741824:.2f} GB) ---")
    for nome, sz, keep, trash, ganho in big:
        print(f"\nGRUPO « {nome} » {sz} B × {len(trash)+1} cópias — recuperável {ganho/1073741824:.2f} GB")
        print(f"  KEEP  {keep['id']} (parent {(keep.get('parents') or ['?'])[0]}, criado {keep.get('createdTime','?')})")
        for m in trash:
            print(f"  TRASH {m['id']} (parent {(m.get('parents') or ['?'])[0]})")

    if small:
        print(f"\n--- PEQUENOS (<1MB) — revisar à mão, NÃO auto-listados ({len(small)} grupos) ---")
        for nome, sz, keep, trash, ganho in small[:40]:
            print(f"  « {nome} » {sz} B × {len(trash)+1} cópias")
        if len(small) > 40:
            print(f"  … +{len(small)-40} grupos pequenos")

    print(f"\n=== FIM === grupos_grandes={len(big)} dups_grandes={sum(len(t) for _,_,_,t,_ in big)} "
          f"recuperavel_GB={total_bytes/1073741824:.2f} grupos_pequenos={len(small)}")


if __name__ == "__main__":
    main()

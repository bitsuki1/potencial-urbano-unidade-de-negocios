#!/usr/bin/env python3
"""
confrontar_arrumacao_sa.py — CONFRONTAÇÃO REAL índice×Drive via conta de serviço (AUD-A08).

Percorre a árvore viva de POTENCIAL URBANO (BFS, read-only) e confronta cada drive_id do
INDICE-SEED com onde o arquivo ESTÁ de fato. Fecha o loop da arrumação sem depender do log
colado do GAS (o dono avisou 2026-08-05 que o Apps Script rodou; esta é a prova independente).

Saídas (consumidas pelo pipeline EXISTENTE — reconciliar_arrumacao.py + gate-arrumacao.py):
  • inventario/gas-log-<data>-confrontacao-sa.txt com:
      MOVE_LINHA did,folderId,md5,bytes,moved     ← vivo numa pasta-destino (md5 real da API)
      MOVE_LINHA did,folderId,,,nativo            ← Google-nativo (sem md5 por natureza, B-05)
      EXCLUIDO_LINHA did                          ← ausente da árvore = excluído físico
                                                    (D-DONO-2026-07-18: exclusão em massa 90/99)
  • inventario/confrontacao-drive.json (lido pelo C2 do gate; janela de 30 dias)

Read-only no Drive: nenhum arquivo é movido/criado/apagado. PU 20 · 2026-08-06.
"""
import json
import os
import sys
from datetime import date

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POTENCIAL_URBANO_ID = "1BrM6q36meTtn5guJoiGbqvCtZF11Uau3"
ENTRADA_ID = "1grhqYgttj7KnJmiu9U73z-lXFHnFthov"   # 01 — _entrada (ainda-aqui = NÃO movido)
FOLDER = "application/vnd.google-apps.folder"


def _drive():
    raw = os.environ.get("GOOGLE_SA_KEY", "").strip()
    if not raw:
        print("ERRO: GOOGLE_SA_KEY ausente.", file=sys.stderr)
        sys.exit(2)
    info = json.loads(raw)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive.readonly"])
    print(f"autenticado (read-only): {info.get('client_email')}")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def listar_filhos(drive, parent_id):
    """Filhos diretos (paginado)."""
    itens, token = [], None
    while True:
        r = drive.files().list(
            q=f"'{parent_id}' in parents and trashed = false",
            fields="nextPageToken, files(id,name,mimeType,md5Checksum,size)",
            pageSize=1000, supportsAllDrives=True, includeItemsFromAllDrives=True,
            pageToken=token).execute()
        itens.extend(r.get("files", []))
        token = r.get("nextPageToken")
        if not token:
            break
    return itens


def varrer_arvore(drive, raiz_id):
    """BFS da árvore inteira. Devolve {file_id: (parent_id, path, md5, bytes, mime)} só de ARQUIVOS,
    e o conjunto de folder_ids que estão sob a _entrada (para separar 'ainda não movido')."""
    vivos = {}
    fila = [(raiz_id, "")]
    sob_entrada = set()
    n_pastas = 0
    while fila:
        pid, path = fila.pop(0)
        if pid == ENTRADA_ID or pid in sob_entrada:
            marca_entrada = True
        else:
            marca_entrada = False
        for it in listar_filhos(drive, pid):
            if it["mimeType"] == FOLDER:
                n_pastas += 1
                if marca_entrada or it["id"] == ENTRADA_ID:
                    sob_entrada.add(it["id"])
                fila.append((it["id"], f"{path}/{it['name']}"))
            else:
                vivos[it["id"]] = (pid, f"{path}/{it['name']}",
                                   it.get("md5Checksum", ""), it.get("size", ""),
                                   it["mimeType"], marca_entrada)
    print(f"varredura: {len(vivos)} arquivos vivos em {n_pastas} pastas")
    return vivos


def main():
    import csv
    seed_path = os.path.join(RAIZ, "inventario", "INDICE-SEED.csv")
    with open(seed_path, encoding="utf-8") as f:
        seed_ids = [r["drive_id"] for r in csv.DictReader(f)]
    print(f"SEED: {len(seed_ids)} itens carimbados")

    drive = _drive()
    vivos = varrer_arvore(drive, POTENCIAL_URBANO_ID)

    hoje = date.today().isoformat()
    movidos, nativos, na_entrada, excluidos = [], [], [], []
    linhas_log = []
    for did in seed_ids:
        v = vivos.get(did)
        if v is None:
            excluidos.append(did)
            linhas_log.append(f"EXCLUIDO_LINHA {did}")
            continue
        pid, path, md5, byts, mime, em_entrada = v
        if em_entrada:
            na_entrada.append(did)          # ainda no despejo: NÃO movido (fica carimbado)
            continue
        if mime.startswith("application/vnd.google-apps"):
            nativos.append(did)
            linhas_log.append(f"MOVE_LINHA {did},{pid},,,nativo")
        else:
            movidos.append(did)
            linhas_log.append(f"MOVE_LINHA {did},{pid},{md5},{byts},moved")

    log_path = os.path.join(RAIZ, "inventario", f"gas-log-{hoje}-confrontacao-sa.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"# Confrontação SA read-only {hoje} — prova independente pós-Apps Script\n")
        f.write("\n".join(linhas_log) + "\n")

    resultado = {
        "versao": 2,
        "data_confrontacao": hoje,
        "metodo": "conta de serviço (read-only), varredura BFS completa da árvore POTENCIAL URBANO",
        "resultado": {
            "total_indice": len(seed_ids),
            "movidos_real": len(movidos) + len(nativos),
            "ainda_na_entrada": len(na_entrada),
            "excluidos_fisicos": len(excluidos),
            "status": "arrumacao_executada" if (len(movidos) + len(nativos)) > 0 else "arrumacao_nunca_rodou",
            "explicacao": (f"{len(movidos)} movidos c/ md5 + {len(nativos)} Google-nativos em pastas-destino; "
                           f"{len(na_entrada)} ainda na _entrada; {len(excluidos)} ausentes da árvore "
                           f"(exclusão física D-DONO-2026-07-18)."),
        },
        "prova": f"inventario/gas-log-{hoje}-confrontacao-sa.txt (gerado pela Action confrontar-arrumacao)",
        "nota": "Atualizado a cada confrontação real. O gate-arrumacao.py lê a data e reprova se > 30 dias.",
    }
    conf_path = os.path.join(RAIZ, "inventario", "confrontacao-drive.json")
    with open(conf_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\n=== CONFRONTAÇÃO {hoje} ===")
    print(f"  movidos (md5 real): {len(movidos)}")
    print(f"  Google-nativos:     {len(nativos)}")
    print(f"  ainda na _entrada:  {len(na_entrada)}")
    print(f"  excluídos físicos:  {len(excluidos)}")
    print(f"gravado: {log_path}\ngravado: {conf_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

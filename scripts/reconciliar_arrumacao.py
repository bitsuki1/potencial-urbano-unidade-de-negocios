#!/usr/bin/env python3
"""
reconciliar_arrumacao.py — FECHA O LOOP da arrumação (lente reconciliação R1/R2/R4/R5).

O seeder escreve o PLANO imutável `inventario/INDICE-SEED.csv` (status=carimbado). O Apps Script
roda no Drive e imprime no Log linhas prefixadas. O dono COLA o Log em `inventario/gas-log-*.txt`.
Este script LÊ o SEED + esses logs e ESCREVE `inventario/INDICE-MESTRE-DRIVE.csv` (o estado REAL:
status=moved/quarentena, hash_md5/bytes/mime preenchidos) + faz *append* na trilha durável
`inventario/arrumacao-log.csv` (uma linha por move — invariante §5.6, a prova mora no git, não no Log).

Só ASSIM o gate sai da fase 'plano' e a arrumação se PROVA feita.

Formatos aceitos nos `gas-log-*.txt` (o dono cola o Log inteiro; o parser pega só estas linhas):
  MOVE_LINHA drive_id,folderId,md5,bytes,status      (do Organizar-Entrada; status moved|jaLa|skip)
  CSV_LINHA  drive_id,md5,acao,canonico_id           (do Sanear-Lago; acao MANTER|QUARENTENA|MULTI_PAI_MANUAL)
Ignora *_DRYRUN (ensaio não move nada) — não muda status.

R4 — UPSERT: arquivo do lago que não está no SEED é INSERIDO. E BLOQUEIA se uma irmã OFICIAL for
mandada p/ quarentena enquanto a canônica é NOSSA (a regra "OFICIAL é citável" exige canônica de maior
oficialidade). R5 — a coluna é `hash_md5` (a única hash que o Drive entrega), não sha256.

Uso:  python3 scripts/reconciliar_arrumacao.py           # SEED (+ logs, se houver) -> MESTRE + trilha
      python3 scripts/reconciliar_arrumacao.py --check   # falha se MESTRE difere do reconciliado
"""
import csv
import glob
import re
import sys
from io import StringIO
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
INV = RAIZ / "inventario"
SEED = INV / "INDICE-SEED.csv"
MESTRE = INV / "INDICE-MESTRE-DRIVE.csv"
TRILHA = INV / "arrumacao-log.csv"

sys.path.insert(0, str(RAIZ / "scripts"))
import semear_indice_mestre as SEM  # noqa: E402  (reusa COLUNAS + serializar)

RE_MOVE = re.compile(r"MOVE_LINHA\s+([^,]+),([^,]*),([^,]*),([^,]*),(\w+)")
RE_CSV = re.compile(r"CSV_LINHA\s+([^,]+),([^,]*),(\w+),([^,\s]*)")
TRILHA_COLS = ["data_ref", "drive_id", "acao", "origem", "destino", "hash_md5"]


def _carregar_seed():
    if not SEED.exists():
        print("reconciliar: SEED ausente — rode semear_indice_mestre.py antes.", file=sys.stderr)
        return None
    linhas = list(csv.DictReader(open(SEED, encoding="utf-8")))
    return {r["drive_id"]: dict(r) for r in linhas}, [r["drive_id"] for r in linhas]


def _linha_vazia(drive_id):
    l = {c: "" for c in SEM.COLUNAS}
    l["drive_id"] = drive_id
    l["dominio"] = l["dominio_primario"] = l["tipo_artefato"] = SEM.PEND
    l["proveniencia"] = l["oficialidade"] = SEM.PEND
    l["status_arrumacao"] = "carimbado"
    return l


def reconciliar():
    carga = _carregar_seed()
    if carga is None:
        return None, None
    idx, ordem = carga
    trilha_novas = []
    bloqueios = []

    logs = sorted(glob.glob(str(INV / "gas-log-*.txt")))
    for lp in logs:
        data_ref = re.search(r"gas-log-(.+)\.txt", Path(lp).name)
        data_ref = data_ref.group(1) if data_ref else "?"
        texto = Path(lp).read_text(encoding="utf-8", errors="replace")

        # MOVE_LINHA (Organizar-Entrada): move p/ pasta-tipo.
        for m in RE_MOVE.finditer(texto):
            did, folder, md5, byts, status = (x.strip() for x in m.groups())
            if status.lower() in ("skip", "dryrun") or status.endswith("DRYRUN"):
                continue
            r = idx.get(did) or _linha_vazia(did)
            r["status_arrumacao"] = "moved"
            if md5:
                r["hash_md5"] = md5
            if byts:
                r["bytes"] = byts
            if folder:
                r["observacao"] = (r.get("observacao") or "") and r["observacao"] or f"folderId={folder}"
            idx[did] = r
            if did not in ordem:
                ordem.append(did)
            trilha_novas.append({"data_ref": data_ref, "drive_id": did, "acao": "moved",
                                 "origem": "_entrada", "destino": folder, "hash_md5": md5})

        # CSV_LINHA (Sanear-Lago): dedup por hash.
        canon_ofi = {}   # canonico_id -> oficialidade (p/ o check R4)
        for m in RE_CSV.finditer(texto):
            did, md5, acao, canon = (x.strip() for x in m.groups())
            if acao.endswith("DRYRUN"):
                continue
            if acao == "MANTER":
                r = idx.get(did) or _linha_vazia(did)
                r["status_arrumacao"] = "moved"
                if md5:
                    r["hash_md5"] = md5
                idx[did] = r
                if did not in ordem:
                    ordem.append(did)
                canon_ofi[did] = r.get("oficialidade", SEM.PEND)
            elif acao == "QUARENTENA":
                r = idx.get(did) or _linha_vazia(did)   # UPSERT: irmã do lago pode não estar no SEED
                r["status_arrumacao"] = "quarentena"
                r["destino_path"] = "98 — _LEGADO/_quarentena"
                r["substituido_por"] = canon
                if md5:
                    r["hash_md5"] = md5
                idx[did] = r
                if did not in ordem:
                    ordem.append(did)
                trilha_novas.append({"data_ref": data_ref, "drive_id": did, "acao": "quarentena",
                                     "origem": "TODOS TDC", "destino": "98/_quarentena", "hash_md5": md5})
                # R4 — canônica NÃO pode ser menos oficial que a irmã quarentenada.
                if r.get("oficialidade") == "OFICIAL" and canon_ofi.get(canon) == "NOSSO":
                    bloqueios.append(f"{did}: OFICIAL quarentenado sob canônica NOSSA {canon} (R4)")
            elif acao == "MULTI_PAI_MANUAL":
                r = idx.get(did) or _linha_vazia(did)
                r["status_arrumacao"] = "triagem"       # decisão humana (multi-pai) — não movido
                r["observacao"] = "multi-pai: decidir manualmente (99)"
                idx[did] = r
                if did not in ordem:
                    ordem.append(did)

    linhas = [idx[d] for d in ordem]
    return (linhas, trilha_novas, bloqueios), logs


def main(check_only):
    res, logs = reconciliar()
    if res is None:
        return 1
    linhas, trilha_novas, bloqueios = res
    if bloqueios:
        print("reconciliar: BLOQUEIO (R4) — canônica menos oficial que a irmã quarentenada:")
        for b in bloqueios:
            print(f"  ✗ {b}")
        return 2

    conteudo = SEM.serializar(linhas)
    if check_only:
        atual = MESTRE.read_text(encoding="utf-8") if MESTRE.exists() else ""
        if atual != conteudo:
            print("reconciliar --check: FALHA — MESTRE difere do reconciliado. Rode sem --check.")
            return 1
        print(f"reconciliar --check: OK — MESTRE em dia ({len(linhas)} linhas).")
        return 0

    MESTRE.write_text(conteudo, encoding="utf-8")
    # trilha durável (append-only): só cresce, é a prova versionada dos moves.
    novo_arquivo = not TRILHA.exists()
    if trilha_novas:
        buf = StringIO()
        w = csv.DictWriter(buf, fieldnames=TRILHA_COLS, lineterminator="\n")
        if novo_arquivo:
            w.writeheader()
        for t in trilha_novas:
            w.writerow(t)
        with open(TRILHA, "a", encoding="utf-8") as f:
            f.write(buf.getvalue())

    import collections
    st = collections.Counter(l["status_arrumacao"] for l in linhas)
    print(f"reconciliar: {len(linhas)} linhas -> {MESTRE.relative_to(RAIZ)} "
          f"({len(logs)} log(s) do GAS aplicados)")
    print(f"  status: {dict(st)}")
    if trilha_novas:
        print(f"  trilha: +{len(trilha_novas)} moves em {TRILHA.relative_to(RAIZ)}")
    else:
        print("  (nenhum log do GAS ainda — MESTRE == SEED; fase 'plano')")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))

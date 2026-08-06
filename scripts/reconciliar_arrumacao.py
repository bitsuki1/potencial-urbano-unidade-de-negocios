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
# Confrontação SA (2026-08-06): item do SEED AUSENTE da árvore viva = excluído físico (exclusão em
# massa 90/99 decidida pelo dono, D-DONO-2026-07-18). Estado TERMINAL deliberado (R11), não pendência.
RE_EXC = re.compile(r"EXCLUIDO_LINHA\s+(\S+)")
# R8: inventário do lago (nome entre aspas). Último campo = \S* (NÃO [^,]*, que casa \n e come a linha seguinte).
RE_INV = re.compile(r'INV_LINHA\s+(\S+),"([^"]*)",([^,]*),(\S*)')
TRILHA_COLS = ["data_ref", "drive_id", "acao", "origem", "destino", "hash_md5"]
CROSS = INV / "cross-tree-dups.csv"       # R9: duplicatas byte-idênticas entre árvores (p/ GAS de quarentena)
CROSS_COLS = ["hash_md5", "canonico_id", "dup_id", "dup_status", "motivo"]
OFI_RANK = {"OFICIAL": 3, "ADQUIRIDO": 2, "NOSSO": 1, "PENDENTE": 0, "": 0}


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

        # R8 — INV_LINHA (inventário do lago): UPSERT + CLASSIFICA cada arquivo do lago pelo NOME
        # (reusa SEM.classificar). Assim a canônica que fica no lago recebe tipo/domínio/destino e
        # deixa de ser órfã. Não muda status aqui (MANTER/QUARENTENA abaixo é que movem).
        for m in RE_INV.finditer(texto):
            did, nome, md5, byts = m.group(1).strip(), m.group(2).strip(), m.group(3).strip(), m.group(4).strip()
            r = idx.get(did)
            if r is None:                       # arquivo do lago fora do de-para → INSERE, classificado
                r = _linha_vazia(did)
                r["nome_origem"] = nome
                c = SEM.classificar(nome, "")
                for k, v in c.items():
                    r[k] = v
                r["observacao"] = "lago: TODOS TDC"
            if md5:
                r["hash_md5"] = md5
            if byts:
                r["bytes"] = byts
            idx[did] = r
            if did not in ordem:
                ordem.append(did)

        # MOVE_LINHA (Organizar-Entrada): move p/ pasta-tipo. status ∈ moved|nativo|jaLa|MULTI_PAI_MANUAL
        # (dryrun/*DRYRUN ignorados — B-06). nativo→terminal 'nativo_ignorado' (B-05, sem exigir hash);
        # multi-pai→'triagem' (A-09, não movido).
        for m in RE_MOVE.finditer(texto):
            did, folder, md5, byts, status = (x.strip() for x in m.groups())
            if status.lower() in ("skip", "dryrun") or status.endswith("DRYRUN"):
                continue
            novo = did not in idx
            r = idx.get(did) or _linha_vazia(did)
            if status == "MULTI_PAI_MANUAL":
                r["status_arrumacao"] = "triagem"
                r["observacao"] = "multi-pai: NÃO movido (arrancaria de outra pasta) — decidir em 99 (A-09)"
                acao = "triagem"
            elif status == "nativo":
                r["status_arrumacao"] = "nativo_ignorado"    # Google-nativo: sem md5 por natureza (B-05)
                acao = "nativo_ignorado"
            else:                                            # moved | jaLa
                r["status_arrumacao"] = "moved"
                acao = "moved"
            if md5:
                r["hash_md5"] = md5
            if byts:
                r["bytes"] = byts
            # B-05: upsert de id fora do SEED precisa de destino_path (senão C3 fica vermelho eterno).
            if folder and (novo or not (r.get("destino_path") or "").strip()):
                r["destino_path"] = f"movido→folderId={folder}"
                if not (r.get("destino_classe") or "").strip():
                    r["destino_classe"] = "movido"
            idx[did] = r
            if did not in ordem:
                ordem.append(did)
            trilha_novas.append({"data_ref": data_ref, "drive_id": did, "acao": acao,
                                 "origem": "_entrada", "destino": folder, "hash_md5": md5})

        # EXCLUIDO_LINHA (confrontação SA): ausente da árvore viva → terminal 'excluido' (R11 +
        # D-DONO-2026-07-18). Não exige hash (o arquivo não existe mais para ser hasheado).
        for m in RE_EXC.finditer(texto):
            did = m.group(1).strip()
            r = idx.get(did) or _linha_vazia(did)
            r["status_arrumacao"] = "excluido"
            r["observacao"] = "excluído físico no Drive (D-DONO-2026-07-18); ausente na confrontação SA"
            idx[did] = r
            if did not in ordem:
                ordem.append(did)
            trilha_novas.append({"data_ref": data_ref, "drive_id": did, "acao": "excluido",
                                 "origem": "arvore-PU", "destino": "", "hash_md5": ""})

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
    cross = _detectar_cross_tree(linhas)
    return (linhas, trilha_novas, bloqueios, cross), logs


def _detectar_cross_tree(linhas):
    """R9 — dedup GLOBAL: agrupa por hash_md5 os itens fisicamente COLOCADOS (moved/espelhado). Um hash
    com >1 colocado é duplicata byte-idêntica ENTRE árvores (_entrada × lago) que nenhum passe local vê.
    Elege a canônica (maior oficialidade; empate → primeira) e devolve as EXTRAS p/ quarentena posterior
    (via um GAS que consome `inventario/cross-tree-dups.csv`). Não muda o Drive — só SURFAÇA (não esconde)."""
    colocado = ("moved", "espelhado")
    por_hash = {}
    for r in linhas:
        h = (r.get("hash_md5") or "").strip()
        if h and h != SEM.PEND and (r.get("status_arrumacao") or "").strip() in colocado:
            por_hash.setdefault(h, []).append(r)
    extras = []
    for h, grupo in por_hash.items():
        if len(grupo) < 2:
            continue
        canon = max(grupo, key=lambda r: OFI_RANK.get((r.get("oficialidade") or "").strip(), 0))
        for r in grupo:
            if r is canon:
                continue
            extras.append({"hash_md5": h, "canonico_id": canon["drive_id"], "dup_id": r["drive_id"],
                           "dup_status": r.get("status_arrumacao", ""),
                           "motivo": f"byte-idêntico a {canon['drive_id']} ({canon.get('oficialidade')})"})
    return extras


def main(check_only):
    res, logs = reconciliar()
    if res is None:
        return 1
    linhas, trilha_novas, bloqueios, cross = res
    if bloqueios:
        print("reconciliar: BLOQUEIO (R4) — canônica menos oficial que a irmã quarentenada:")
        for b in bloqueios:
            print(f"  ✗ {b}")
        return 2

    conteudo = SEM.serializar(linhas)
    cross_conteudo = ""
    if cross:
        buf = StringIO()
        w = csv.DictWriter(buf, fieldnames=CROSS_COLS, lineterminator="\n")
        w.writeheader()
        for x in cross:
            w.writerow(x)
        cross_conteudo = buf.getvalue()

    if check_only:
        atual = MESTRE.read_text(encoding="utf-8") if MESTRE.exists() else ""
        atual_cross = CROSS.read_text(encoding="utf-8") if CROSS.exists() else ""
        if atual != conteudo or atual_cross != cross_conteudo:
            print("reconciliar --check: FALHA — MESTRE/cross-tree difere do reconciliado. Rode sem --check.")
            return 1
        print(f"reconciliar --check: OK — MESTRE em dia ({len(linhas)} linhas).")
        return 0

    # Trilha durável: REGENERADA dos logs a cada run (os gas-log-*.txt são a fonte, versionados no git),
    # NÃO append — senão rodar 2× DOBRA as linhas (idempotência quebrada). Regenerar é determinístico.
    trilha_conteudo = ""
    if trilha_novas:
        buf = StringIO()
        w = csv.DictWriter(buf, fieldnames=TRILHA_COLS, lineterminator="\n")
        w.writeheader()
        for t in trilha_novas:
            w.writerow(t)
        trilha_conteudo = buf.getvalue()

    MESTRE.write_text(conteudo, encoding="utf-8")
    if cross_conteudo:
        CROSS.write_text(cross_conteudo, encoding="utf-8")
    elif CROSS.exists():
        CROSS.unlink()      # sem cross-tree dups → sem arquivo (idempotência)
    if trilha_conteudo:
        TRILHA.write_text(trilha_conteudo, encoding="utf-8")
    elif TRILHA.exists():
        TRILHA.unlink()

    import collections
    st = collections.Counter(l["status_arrumacao"] for l in linhas)
    print(f"reconciliar: {len(linhas)} linhas -> {MESTRE.relative_to(RAIZ)} "
          f"({len(logs)} log(s) do GAS aplicados)")
    print(f"  status: {dict(st)}")
    if trilha_novas:
        print(f"  trilha: +{len(trilha_novas)} moves em {TRILHA.relative_to(RAIZ)}")
    else:
        print("  (nenhum log do GAS ainda — MESTRE == SEED; fase 'plano')")
    if cross:
        print(f"  R9 CROSS-TREE: {len(cross)} duplicata(s) byte-idêntica(s) entre árvores → "
              f"{CROSS.relative_to(RAIZ)} (rode o GAS de quarentena p/ removê-las).")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))

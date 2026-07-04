#!/usr/bin/env python3
"""
semear_indice_mestre.py — Semeia `inventario/INDICE-MESTRE-DRIVE.csv` (20 colunas do plano §5) a
partir do de-para já classificado (`drive-arrumacao/de-para-COMPLETO-2026-07-04.csv`, 1.360 arquivos).

DETERMINÍSTICO, não inventa: preenche só o que é derivável do de-para (drive_id, nome_origem,
tipo_artefato, dominio, proveniencia, destino_classe/path) e marca **PENDENTE** o que só a execução
no Drive/GAS pode preencher (hash_sha256, bytes, mime, vigência). `status_arrumacao=planejado` = o
índice é o PLANO; vira `moved`/`espelhado` quando o Apps Script rodar e a reconciliação reimportar.

Mapa de DOMÍNIO herdado da subpasta do de-para (a taxonomia de junho já separa domínio):
  2.1 Urbanística (PDE-LPUOS-COE) → compartilhado   2.2 TDC-Patrimônio-ZEPEC → tdc
  2.3 IPTU-Tributário            → iptu             2.6 Jurisprudência       → iptu
  2.4 Federal e Constituição     → compartilhado (matriz; não-perda)   demais → pendente
Onde a subpasta não decide o domínio, fica `pendente` (honesto) — uma lente/onda afina.

Uso:  python3 scripts/semear_indice_mestre.py            # gera/atualiza o índice
      python3 scripts/semear_indice_mestre.py --check    # falha se o de-para mudou e o índice não
"""
import csv
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DEPARA = RAIZ / "drive-arrumacao" / "de-para-COMPLETO-2026-07-04.csv"
SAIDA = RAIZ / "inventario" / "INDICE-MESTRE-DRIVE.csv"

COLUNAS = ["drive_id", "nome_origem", "nome_canonico", "tipo_artefato", "dominio", "dominio_primario",
           "proveniencia", "oficialidade", "confianca", "vigencia_inicio", "vigencia_fim",
           "substitui", "substituido_por", "destino_classe", "destino_path",
           "hash_sha256", "bytes", "mime", "id_pipeline", "status_arrumacao", "observacao"]

PEND = "PENDENTE"

# destino (do de-para) -> (tipo_artefato, dominio, proveniencia_default)
def classificar_destino(destino: str):
    d = destino or ""
    if d.startswith("00"):
        return "governanca", "compartilhado", "NOS"      # relatórios/oráculos NOSSOS + índices
    if "2.1" in d:
        return "lei", "compartilhado", "OFI"              # PDE/LPUOS/COE
    if "2.2" in d:
        return "lei", "tdc", "OFI"                        # TDC/Patrimônio/ZEPEC
    if "2.3" in d:
        return "lei", "iptu", "OFI"                       # IPTU-tributário municipal
    if "2.4" in d:
        return "lei", "compartilhado", "OFI"              # Federal e Constituição (matriz)
    if "2.5" in d:
        return "lei", PEND, "OFI"                         # infralegal (decretos/portarias — domínio varia)
    if "2.6" in d:
        return "jurisprudencia", "iptu", "OFI"            # acórdãos/súmulas (montados p/ tese IPTU)
    if "2.7" in d:
        return "doutrina", PEND, "ADQ"                    # doutrina/estudos/avaliação (adquirido)
    if d.startswith("03"):
        return "tabela", PEND, "OFI"                      # tabelas & engines (Quadros PDE/Q14)
    if d.startswith("05"):
        return "geo", PEND, "OFI"                         # geo/mapas (PESADO → Supabase)
    if d.startswith("99"):
        return PEND, PEND, PEND                           # inbox/triagem
    return PEND, PEND, PEND


# Sobrescreve proveniência p/ NOSSO quando o título grita "gerado por nós/IA" (não-confiável p/ número).
RE_NOSSO = re.compile(r"lote[_ ]?ia|or[áa]culo|rascunho|manifesto|relat[óo]rio|log[_ ]|extra[çc][ãa]o conclu|"
                      r"renderiz|p[áa]ginas? renderizaram", re.IGNORECASE)


def proveniencia(titulo: str, default: str) -> str:
    if RE_NOSSO.search(titulo or ""):
        return "NOS"
    return default


def linha_indice(r):
    destino = r.get("destino", "")
    tipo, dom, prov_def = classificar_destino(destino)
    prov = proveniencia(r.get("titulo", ""), prov_def)
    dom_prim = dom if dom in ("tdc", "iptu", "compartilhado") else PEND
    return {
        "drive_id": r.get("drive_id", "").strip(),
        "nome_origem": r.get("titulo", "").strip(),
        "nome_canonico": PEND,               # a carimbar na onda 2 (convenção [DOM][PROV] … {vig})
        "tipo_artefato": tipo,
        "dominio": dom,
        "dominio_primario": dom_prim,
        "proveniencia": prov,
        "oficialidade": ("OFICIAL" if prov == "OFI" else "ADQUIRIDO" if prov == "ADQ"
                         else "NOSSO" if prov == "NOS" else PEND),
        "confianca": PEND,
        "vigencia_inicio": PEND, "vigencia_fim": PEND,
        "substitui": "", "substituido_por": "",
        "destino_classe": (destino.split(" ")[0] if destino else PEND),
        "destino_path": destino,
        "hash_sha256": PEND,                 # só o GAS (md5Checksum do Drive) preenche
        "bytes": PEND, "mime": PEND,
        "id_pipeline": "",
        "status_arrumacao": "planejado",     # PLANO; vira moved/espelhado após execução+reconciliação
        "observacao": r.get("destino_folderId", "").strip() and f"folderId={r['destino_folderId'].strip()}" or "",
    }


def gerar():
    if not DEPARA.exists():
        print(f"semear: de-para ausente ({DEPARA}) — nada a semear.", file=sys.stderr)
        return None
    rows = list(csv.DictReader(open(DEPARA, encoding="utf-8")))
    return [linha_indice(r) for r in rows]


def main(check_only: bool):
    linhas = gerar()
    if linhas is None:
        return 1
    from io import StringIO
    buf = StringIO()
    # lineterminator="\n": casa com read_text/write_text (universal newlines) — --check idempotente.
    w = csv.DictWriter(buf, fieldnames=COLUNAS, lineterminator="\n")
    w.writeheader()
    for l in linhas:
        w.writerow(l)
    conteudo = buf.getvalue()

    if check_only:
        atual = SAIDA.read_text(encoding="utf-8") if SAIDA.exists() else ""
        if atual != conteudo:
            print("semear --check: FALHA — índice-mestre desatualizado vs de-para. Rode sem --check.")
            return 1
        print(f"semear --check: OK — índice-mestre em dia ({len(linhas)} linhas).")
        return 0

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(conteudo, encoding="utf-8")
    # relatório
    import collections
    dist_dom = collections.Counter(l["dominio"] for l in linhas)
    dist_tipo = collections.Counter(l["tipo_artefato"] for l in linhas)
    print(f"semear: {len(linhas)} linhas -> {SAIDA.relative_to(RAIZ)}")
    print(f"  domínio: {dict(dist_dom)}")
    print(f"  tipo:    {dict(dist_tipo)}")
    print(f"  PENDENTE de domínio: {dist_dom.get(PEND,0)} (afinar por lente/onda) · "
          f"hash/bytes/mime/vigência: PENDENTE em todas (só o GAS preenche)")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))

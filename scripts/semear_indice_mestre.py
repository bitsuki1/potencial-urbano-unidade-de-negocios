#!/usr/bin/env python3
"""
semear_indice_mestre.py — Semeia `inventario/INDICE-SEED.csv` (o PLANO imutável, 20 col do plano §5)
a partir do de-para classificado (`drive-arrumacao/de-para-COMPLETO-2026-07-04.csv`, 1.360 arquivos).

SEPARAÇÃO DE RESPONSABILIDADE (lente reconciliação R2): o SEEDER só escreve o SEED (o PLANO). Quem
escreve `INDICE-MESTRE-DRIVE.csv` (SEED + resultados reais do Apps Script) é `reconciliar_arrumacao.py`.
Assim o `--check` do seed nunca colide com a reconciliação (o seeder não sobrescreve status=moved).

DETERMINÍSTICO, não inventa. Classificação afinada pelas lentes de revisão (2026-07-04):
  · domínio: herdado da subpasta do de-para, com INFERÊNCIA por título p/ resolver PENDENTE e p/ NÃO
    contradizer o SSOT do git (carimbar_dominio.py). 2.4 Federal = iptu por padrão (maioria do SSOT),
    com override compartilhado p/ EC132/PDE/LPUOS/COE/registro/tombados (A1).
  · tipo: override por título — mapa/planta/shp → geo; quadro*final → tabela; Lei/Decreto em bucket de
    juris → lei; jurisprudência (stj/stf-tema/resp/súmula) presa em 2.7 → volta a jurisprudencia (A2/A3).
  · proveniência: NOSSO p/ e-SAJ/portal/captura/rascunho/IA (A4); OFI p/ lei/jurisprudência oficial.
Campos que só o Drive/GAS sabem ficam PENDENTE: `hash_md5`, `bytes`, `mime` (a coluna é md5, não sha256 — R5).
`vigencia_inicio` NÃO é PENDENTE quando o ano está no título (B3). `status_arrumacao=carimbado` (enum §5, B2).

Uso:  python3 scripts/semear_indice_mestre.py            # gera/atualiza o SEED
      python3 scripts/semear_indice_mestre.py --check    # falha se o de-para mudou e o SEED não
"""
import csv
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DEPARA = RAIZ / "drive-arrumacao" / "de-para-COMPLETO-2026-07-04.csv"
SAIDA = RAIZ / "inventario" / "INDICE-SEED.csv"

COLUNAS = ["drive_id", "nome_origem", "nome_canonico", "tipo_artefato", "dominio", "dominio_primario",
           "proveniencia", "oficialidade", "confianca", "vigencia_inicio", "vigencia_fim",
           "substitui", "substituido_por", "destino_classe", "destino_path",
           "hash_md5", "bytes", "mime", "id_pipeline", "status_arrumacao", "observacao"]
PEND = "PENDENTE"

# --- domínio-base por subpasta do de-para (a taxonomia de junho já separa domínio). ---
# 2.4 Federal = iptu por padrão (10 das 12 federais do SSOT são iptu); a inferência bumpa as 2 compart.
BASE_DOMINIO = {"2.1": "compartilhado", "2.2": "tdc", "2.3": "iptu", "2.4": "iptu",
                "2.5": PEND, "2.6": "iptu", "2.7": PEND}

# --- INFERÊNCIA de domínio por título (resolve PENDENTE e reconcilia com o SSOT do git). ---
# números de lei COMPARTILHADA (SSOT carimbar_dominio): PDE 16.050, LPUOS 16.402, COE 16.642,
# EC 132, registros 6.015, tombados 12.350. Casados com contexto p/ evitar falso-positivo.
RE_COMPART = re.compile(r"16[.\s]?050|16[.\s]?402|16[.\s]?642|"
                        r"(?:ec|emenda|reforma trib)\D{0,15}132|"
                        r"6[.\s]?015|registros? p[úu]blicos|12[.\s]?350|tombad", re.IGNORECASE)
RE_TDC = re.compile(r"zepec|tombament|conpresp|conspresp|outorga|potencial construtiv|"
                    r"transfer[êe]ncia do direito|solo criado|\bapt\b|\bapc\b", re.IGNORECASE)
RE_IPTU = re.compile(r"\biptu\b|surem|planta gen[ée]rica|valor venal|progressiv|imunidade|"
                     r"execu[çc][ãa]o fiscal|\bcat\b", re.IGNORECASE)


def inferir_dominio(titulo, base):
    t = titulo or ""
    if RE_COMPART.search(t):
        return "compartilhado"
    if RE_TDC.search(t):
        return "tdc"
    if RE_IPTU.search(t):
        return "iptu"
    return base


# --- tipo por título (override do tipo-base da subpasta). ---
# NÃO incluir "zoneamento" aqui: uma LEI de zoneamento é lei, não geo. Só sinais de arquivo geográfico.
RE_GEO = re.compile(r"\bmapa\b|\bplanta\b|\.shp\b|\.gpkg\b|\.kml\b|\.dwg\b|sirgas|shapefile|geosampa", re.IGNORECASE)
RE_TABELA = re.compile(r"quadro.*final|\bquadro\b.*\.(xlsx|csv|doc)", re.IGNORECASE)
RE_JURIS = re.compile(r"st[jf][-_ ]?tema|st[jf][-_ ]?resp|s[úu]mula|\bresp\b\s*\d|\bare\b\s*\d|\brextra\b", re.IGNORECASE)
RE_NORMA = re.compile(r"\b(lei|decreto|portaria|resolu[çc][ãa]o|instru[çc][ãa]o normativa)\b", re.IGNORECASE)


def tipo_por_titulo(titulo, base):
    t = titulo or ""
    if RE_GEO.search(t):
        return "geo"
    if RE_TABELA.search(t):
        return "tabela"
    if base in ("doutrina", "jurisprudencia", PEND) and RE_JURIS.search(t):
        return "jurisprudencia"     # jurisprudência oficial (A2) — vale mesmo sem destino (lago, base=PEND)
    if base in ("jurisprudencia", PEND) and RE_NORMA.search(t) and not RE_JURIS.search(t):
        return "lei"                # lei/infralegal fora do bucket de leis (A3; e lago sem destino)
    return base


# destino (do de-para) -> (tipo_base, dominio_base, proveniencia_base)
def base_destino(destino):
    d = destino or ""
    if d.startswith("00"):
        return "governanca", "compartilhado", "NOS"
    for chave in ("2.1", "2.2", "2.3", "2.4", "2.5"):
        if chave in d:
            return "lei", BASE_DOMINIO[chave], "OFI"
    if "2.6" in d:
        return "jurisprudencia", "iptu", "OFI"
    if "2.7" in d:
        return "doutrina", PEND, "ADQ"
    if d.startswith("03"):
        return "tabela", PEND, "OFI"
    if d.startswith("05"):
        return "geo", PEND, "OFI"
    if d.startswith("99"):
        return PEND, PEND, PEND
    return PEND, PEND, PEND


# proveniência NOSSO/captura (A4): e-SAJ, portal de serviços, dados de advogado, print, rascunho, IA.
RE_NOSSO = re.compile(r"lote[_ ]?ia|or[áa]culo|rascunho|manifesto|relat[óo]rio|log[_ ]|extra[çc][ãa]o conclu|"
                      r"renderiz|p[áa]ginas? renderizaram|e-?saj|portal de servi[çc]|dados de advogado|"
                      r"\bprint\b|captura", re.IGNORECASE)

RE_ANO = re.compile(r"\b(19\d{2}|20\d{2})\b")


def vigencia_do_titulo(titulo, tipo):
    """B3 — o ano da norma vem do TÍTULO, não do filesystem. Só p/ artefatos datáveis."""
    if tipo not in ("lei", "jurisprudencia", "doutrina"):
        return PEND
    anos = RE_ANO.findall(titulo or "")
    return f"{anos[-1]}-01-01" if anos else PEND   # último ano do título (ano da norma/alteração)


def proveniencia(titulo, base, tipo):
    if RE_NOSSO.search(titulo or ""):
        return "NOS"
    # Lei/norma e jurisprudência são OFICIAIS por natureza — vale MESMO sem destino (arquivo do lago):
    # sem isso, uma LEI do lago fica proveniência PENDENTE e o bloqueio R4 (OFICIAL≠quarentena) não pega.
    if tipo in ("lei", "jurisprudencia"):
        return "OFI"
    return base


# destino-tipo -> classe/pasta canônica da taxonomia de junho (p/ classificar arquivos SEM destino, ex.: lago).
TIPO_PARA_DESTINO = {
    "lei": "02 — Leis & Jurisprudência", "jurisprudencia": "02 — Leis & Jurisprudência/2.6 Jurisprudência",
    "doutrina": "02 — Leis & Jurisprudência/2.7 Doutrina-Estudos-Avaliação",
    "tabela": "03 — Tabelas & Engines", "geo": "05 — Geo / Mapas",
    "governanca": "00 — Governança & Índice",
}


def classificar(titulo, destino=""):
    """Deriva os campos de classificação de UM arquivo a partir do título (+ destino do de-para, se houver).
    Reutilizável: o reconciliador chama isto p/ classificar arquivos do LAGO, que não têm destino (R8)."""
    tipo_b, dom_b, prov_b = base_destino(destino)
    tipo = tipo_por_titulo(titulo, tipo_b)
    dom = inferir_dominio(titulo, dom_b)
    prov = proveniencia(titulo, prov_b, tipo)
    dom_prim = dom if dom in ("tdc", "iptu", "compartilhado") else PEND
    prefixo = f"[{dom_prim[:3].upper()}][{prov}] " if (dom_prim != PEND and prov != PEND) else ""
    dest_path = destino or (TIPO_PARA_DESTINO.get(tipo, "99 — Inbox / Triagem"))
    return {
        "nome_canonico": (prefixo + (titulo or "").strip()) if prefixo else PEND,
        "tipo_artefato": tipo,
        "dominio": dom,
        "dominio_primario": dom_prim,
        "proveniencia": prov,
        "oficialidade": {"OFI": "OFICIAL", "ADQ": "ADQUIRIDO", "NOS": "NOSSO"}.get(prov, PEND),
        "vigencia_inicio": vigencia_do_titulo(titulo, tipo),
        "destino_classe": (dest_path.split(" ")[0] if dest_path else PEND),
        "destino_path": dest_path,
    }


def linha_indice(r):
    destino = r.get("destino", "")
    titulo = r.get("titulo", "")
    c = classificar(titulo, destino)
    return {
        "drive_id": r.get("drive_id", "").strip(),
        "nome_origem": titulo.strip(),
        "nome_canonico": c["nome_canonico"],
        "tipo_artefato": c["tipo_artefato"],
        "dominio": c["dominio"],
        "dominio_primario": c["dominio_primario"],
        "proveniencia": c["proveniencia"],
        "oficialidade": c["oficialidade"],
        "confianca": PEND,
        "vigencia_inicio": c["vigencia_inicio"], "vigencia_fim": PEND,
        "substitui": "", "substituido_por": "",
        "destino_classe": c["destino_classe"],
        "destino_path": c["destino_path"],
        "hash_md5": PEND, "bytes": PEND, "mime": PEND,   # R5: é md5 do Drive, não sha256
        "id_pipeline": "",
        "status_arrumacao": "carimbado",                  # B2: enum §5 (não 'planejado')
        "observacao": (f"folderId={r['destino_folderId'].strip()}"
                       if r.get("destino_folderId", "").strip() else ""),
    }


def gerar():
    if not DEPARA.exists():
        print(f"semear: de-para ausente ({DEPARA}).", file=sys.stderr)
        return None
    return [linha_indice(r) for r in csv.DictReader(open(DEPARA, encoding="utf-8"))]


def serializar(linhas):
    from io import StringIO
    buf = StringIO()
    w = csv.DictWriter(buf, fieldnames=COLUNAS, lineterminator="\n")  # casa read_text/write_text
    w.writeheader()
    for l in linhas:
        w.writerow(l)
    return buf.getvalue()


def main(check_only):
    linhas = gerar()
    if linhas is None:
        return 1
    conteudo = serializar(linhas)
    if check_only:
        atual = SAIDA.read_text(encoding="utf-8") if SAIDA.exists() else ""
        if atual != conteudo:
            print("semear --check: FALHA — SEED desatualizado vs de-para. Rode sem --check.")
            return 1
        print(f"semear --check: OK — SEED em dia ({len(linhas)} linhas).")
        return 0
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    SAIDA.write_text(conteudo, encoding="utf-8")
    import collections
    dom = collections.Counter(l["dominio"] for l in linhas)
    tipo = collections.Counter(l["tipo_artefato"] for l in linhas)
    prov = collections.Counter(l["proveniencia"] for l in linhas)
    print(f"semear: {len(linhas)} linhas -> {SAIDA.relative_to(RAIZ)}")
    print(f"  domínio: {dict(dom)}")
    print(f"  tipo:    {dict(tipo)}")
    print(f"  prov:    {dict(prov)}")
    print(f"  PENDENTE domínio: {dom.get(PEND,0)} · vigência preenchida por título onde datável · "
          f"hash_md5/bytes/mime: PENDENTE (só o GAS).")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))

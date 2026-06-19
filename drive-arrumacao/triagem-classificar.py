#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pré-classificador da TRIAGEM (99) — Potencial Urbano (IPTU/TDC).

Lê o plano (de-para-final.csv), pega os itens que iriam pra "99 — Inbox /
Triagem" e SUGERE um destino temático pra cada um, com confiança e motivo.
Não altera o plano: gera 'triagem-sugestoes.csv' p/ você revisar. O que você
aprovar a gente dobra no plano (v6).

USO:  python3 triagem-classificar.py
"""
import csv, os, re, collections

BASE = os.path.dirname(os.path.abspath(__file__))

D_GOV   = "00 — Governança & Índice"
D_URB   = "02 — Leis & Jurisprudência/2.1 Urbanística (PDE-LPUOS-COE)"
D_TDC   = "02 — Leis & Jurisprudência/2.2 TDC-Patrimônio-ZEPEC"
D_IPTU  = "02 — Leis & Jurisprudência/2.3 IPTU-Tributário Municipal"
D_FED   = "02 — Leis & Jurisprudência/2.4 Federal e Constituição"
D_INFRA = "02 — Leis & Jurisprudência/2.5 Infralegal"
D_JURIS = "02 — Leis & Jurisprudência/2.6 Jurisprudência"
D_TAB   = "03 — Tabelas & Engines"
D_GEO   = "05 — Geo / Mapas"
D_99    = "99 — Inbox / Triagem"

# (regex no título minúsculo, destino, confiança, motivo). Primeira que casar vence.
REGRAS = [
    # --- descartável: logs/artefatos de download, sem valor documental ---
    (r"^(## |todas as \d|todos os |download\b|browse|filefetch|gateway(certifica)?pdf|gatewaypdf|nova_test|test-download|^s\.txt|^r que|puliccompletaport)",
     D_99, "baixa", "LIXO? log/artefato de download — candidato a descartar"),
    (r"(log_extracao|datalake_delta_load|manifesto_datalake)\b.*\.json",
     D_99, "baixa", "LIXO? log técnico .json — candidato a descartar"),

    # --- fora do escopo IPTU/TDC (outro projeto / empresa) ---
    (r"(keepee|bndes|smart factory|contrato de gest|guia de estrutura de pastas)",
     D_99, "media", "FORA DE ESCOPO? parece doc de empresa/outro projeto"),
    (r"balanco_financeiro_\d|fundurb_balanco",
     D_99, "media", "FINANCEIRO — confirmar se entra no acervo do projeto"),

    # --- base de conhecimento IA do projeto (.md de governança) ---
    (r"(conhecimento_mestre_ia|oraculo|hierarquia_de_fontes|estrutura_silver|manifesto_|master_ritos|motor_3_catalogo|relatorio_(duplicados|integridade)|rag pipeline|conclusao_fase_dados|documento_final_ia|^map[ae]_?\d* ?.*\.md)",
     D_GOV, "media", "base de conhecimento/IA do projeto -> Governança"),

    # --- geo / mapas / plantas / quadros ---
    (r"(^mapa|^mapas |^map[ae]_|plantas|^quadros?\b|quota ambiental|drenagem urbana|^plantas)",
     D_GEO, "media", "mapa/planta/quadro -> Geo"),

    # --- federal / constituição ---
    (r"(\bec-\d|emenda constitucional|^dl-57-1966|l6\.015|lei de registros|^lcp ?\d)",
     D_FED, "alta", "norma federal/EC/LC -> Federal e Constituição"),

    # --- jurisprudência / processos ---
    (r"(e-saj|cnj\.jus|acord|peca|downloadpeca|_teo_|_t_bairro|fisco n|advogad|jeronimo dix)",
     D_JURIS, "media", "acórdão/peça/processo/tese -> Jurisprudência"),

    # --- TDC / patrimônio / tombamento ---
    (r"(\btdc\b|tomba|patrim|fundurb|deuso|iphan|bens imateriais|selo de valor cultural|vilas operarias|memorial.*tdc|transfer.ncia do direito de construir)",
     D_TDC, "alta", "TDC/patrimônio/tombamento -> 2.2 TDC-Patrimônio"),

    # --- IPTU / tributário municipal ---
    (r"(iptu|anoref|q14|parcelamentos tribut|tribut|cnae|lista de servic|lista_servicos)",
     D_IPTU, "media", "IPTU/tributário municipal -> 2.3"),

    # --- urbanística (LPUOS / decreto 57.536 / PL / zonas) ---
    (r"(57[._]?536|pl[_ ]?586|zeup|zemp|zona de estrutur|projeto de interven|16768|complexo de saude|omiss.es da legisla)",
     D_URB, "media", "urbanística (LPUOS/zonas/PIU) -> 2.1"),

    # --- infralegal (portarias/regulamentações/anexos/manuais) ---
    (r"(portaria|regulament|^anexo|nota ?tecnica|manual de licenc|requerimento|reorganiza)",
     D_INFRA, "baixa", "portaria/regulamentação/anexo -> 2.5 Infralegal"),

    # --- planilhas soltas ---
    (r"\.(xlsx|csv|tgz)\b|controle de parcelamentos",
     D_TAB, "baixa", "planilha/tabela -> 03"),
]


def classificar(titulo):
    t = titulo.strip().lower()
    for rx, dest, conf, motivo in REGRAS:
        if re.search(rx, t):
            return dest, conf, motivo
    return D_99, "baixa", "sem regra clara -> revisar à mão"


def main():
    rows = [r for r in csv.DictReader(open(os.path.join(BASE, "de-para-final.csv"), encoding="utf-8"))
            if r["destino"].strip().startswith("99")]

    out = []
    for r in rows:
        dest, conf, motivo = classificar(r["titulo"])
        out.append({
            "drive_id": r["drive_id"], "titulo": r["titulo"],
            "sugestao_destino": dest, "confianca": conf, "motivo": motivo,
        })

    saida = os.path.join(BASE, "triagem-sugestoes.csv")
    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["drive_id", "titulo", "sugestao_destino", "confianca", "motivo"])
        w.writeheader(); w.writerows(out)

    # resumo
    by_dest = collections.Counter(o["sugestao_destino"] for o in out)
    by_conf = collections.Counter(o["confianca"] for o in out)
    realocados = sum(1 for o in out if o["sugestao_destino"] != D_99)

    W = 64
    print("=" * W)
    print(f" PRÉ-CLASSIFICAÇÃO DA TRIAGEM — {len(out)} itens")
    print("=" * W)
    print(f" Com sugestão de saída do 99 ..: {realocados}")
    print(f" Permanecem p/ decisão manual .: {len(out) - realocados}")
    print(" Confiança:", dict(by_conf))
    print("-" * W)
    print(" Destinos sugeridos:")
    for d, n in by_dest.most_common():
        print(f"   {n:4}  {d}")
    print("-" * W)
    print(f" CSV de revisão: {saida}")
    print("=" * W)


if __name__ == "__main__":
    main()

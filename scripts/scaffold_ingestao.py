#!/usr/bin/env python3
"""
scaffold_ingestao.py — INDUSTRIALIZA a ingestão de uma norma do portal oficial (braçal determinístico),
deixando o JULGAMENTO (domínio + nuance de vigência) para revisão humana. Faz, por norma:
  1. baixa o verbatim do portal (baixar_norma_portal) -> _entrada/misto/<id>.txt (sha256 da fonte)
  2. extrai deterministicamente do TEXTO REAL: numero, ano, ementa, data de publicacao/vigencia,
     remissoes (Lei/Decreto nº citados), dispositivos_chave (cabeçalho de cada Art. + 1a linha),
     tema (por palavras-chave), e SINAIS DE VIGENCIA (revogado / eficacia suspensa / ADI / revoga)
  3. escreve leis/.../<id>.json (revisado_por_humano=false) + stub .md
  4. promove a verbatim (promover_entrada) — carimba o hash do cru
NÃO registra dominio em carimbar_dominio (o orquestrador faz num lote) e NÃO fatia (lote no fim).
Imprime um RESUMO com os sinais de vigencia p/ o orquestrador revisar o que importa (1.6).

Uso: python3 scripts/scaffold_ingestao.py <slug-portal> <id-corpus> <dominio: tdc|iptu|compartilhado> ["Titulo H1"]
"""
import sys, re, json, subprocess
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import baixar_norma_portal as B

RAIZ = Path(__file__).resolve().parent.parent
MESES = {"janeiro":"01","fevereiro":"02","março":"03","marco":"03","abril":"04","maio":"05",
         "junho":"06","julho":"07","agosto":"08","setembro":"09","outubro":"10","novembro":"11","dezembro":"12"}

TEMAS = [
    ("outorga_onerosa", r'outorga onerosa'),
    ("transferencia_direito_construir", r'transfer[êe]ncia do direito de construir|potencial construtivo'),
    ("coeficiente_aproveitamento", r'coeficiente de aproveitamento'),
    ("plano_intervencao_urbana", r'plano de interven[çc][ãa]o urbana|\bPIU\b|AIU'),
    ("operacao_urbana", r'opera[çc][ãa]o urbana|CEPAC'),
    ("zoneamento", r'zoneamento|zona de uso|LPUOS'),
    ("uso_ocupacao_solo", r'uso e ocupa[çc][ãa]o do solo|parcelamento'),
    ("quota_ambiental", r'quota ambiental'),
    ("regularizacao", r'regulariza[çc][ãa]o'),
    ("itbi", r'\bITBI\b|transmiss[ãa]o.*inter vivos'),
    ("planta_generica_valores", r'planta gen[ée]rica de valores|valor venal'),
    ("habitacao_interesse_social", r'habita[çc][ãa]o de interesse social|\bHIS\b|\bHMP\b'),
]


def det(texto):
    d = {}
    mnum = re.search(r'N[ºo°]\s*([\d.]+)', texto)
    d["numero"] = mnum.group(1) if mnum else ""
    mdata = re.search(r'DE\s+(\d{1,2})\s+DE\s+(\w+)\s+DE\s+(\d{4})', texto, re.I)
    if mdata:
        dia = mdata.group(1).zfill(2); mes = MESES.get(mdata.group(2).lower().replace("ç","c"), "01"); ano = mdata.group(3)
        d["ano"] = int(ano); d["data_pub"] = f"{ano}-{mes}-{dia}"
    else:
        d["ano"] = None; d["data_pub"] = None
    # vigencia: "entra em vigor em DATA" (futura) senao data de publicacao
    mvig = re.search(r'entrar[áa]?\s+em\s+vigor\s+em\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', texto, re.I)
    if mvig:
        dia = mvig.group(1).zfill(2); mes = MESES.get(mvig.group(2).lower().replace("ç","c"), "01")
        d["vig_inicio"] = f"{mvig.group(3)}-{mes}-{dia}"
    else:
        d["vig_inicio"] = d["data_pub"]
    # ementa: 1o paragrafo longo antes do fecho "RICARDO/JOAO ... Prefeito" ou "D E C R E T A"/"faz saber"
    corte = re.split(r'[A-ZÀ-Ú ]+,\s*Prefeit|D\s?E\s?C\s?R\s?E\s?T\s?A|faz saber', texto)[0]
    paras = [p.strip() for p in corte.split("\n") if len(p.strip()) > 60]
    d["ementa"] = paras[-1] if paras else ""
    # remissoes citadas
    rem = sorted(set(re.findall(r'(Lei(?:\s+Federal|\s+Complementar)?\s+n[ºo°]?\s*[\d.]+(?:/\d{2,4}|,\s*de\s+\d{4})?|Decreto\s+n[ºo°]?\s*[\d.]+)', texto, re.I)))
    d["remissoes"] = rem[:20]
    # dispositivos: cabecalho de cada artigo + 1a linha
    disp = []
    for m in re.finditer(r'(?m)^(Art\.?\s*\d+[ºo°A-Z\-]*)\s*(.{0,120})', texto):
        disp.append((m.group(1).strip() + " " + m.group(2).strip()).strip())
    d["dispositivos"] = disp[:25]
    # temas
    d["tema"] = [k for k, rx in TEMAS if re.search(rx, texto, re.I)]
    # SINAIS DE VIGENCIA (1.6) — o que o orquestrador revisa
    d["flag_revogado"] = bool(re.search(r'\(\s*Revogad[oa]', texto))
    d["flag_suspenso"] = bool(re.search(r'efic[áa]cia suspensa|suspens[ãa]o.*efic|liminar', texto, re.I))
    d["flag_adi"] = bool(re.search(r'\bADI\b|a[çc][ãa]o direta de inconstitucionalidade', texto, re.I))
    d["flag_revoga"] = bool(re.search(r'\brevoga(?:d[ao]s?|m|r)?\b', texto, re.I))
    return d


def main():
    if len(sys.argv) < 4:
        print(__doc__); return 2
    slug, cid, dominio = sys.argv[1], sys.argv[2], sys.argv[3]
    titulo = sys.argv[4] if len(sys.argv) > 4 else None
    raw, final = B.baixar(slug)
    texto, err = B.extrair_texto(raw)
    if err or not texto:
        print(f"FALHA {cid}: {err or 'sem texto'} (slug={slug})"); return 1
    import hashlib
    sha = hashlib.sha256(raw).hexdigest()
    ENTRADA = RAIZ / "_entrada" / "misto"; ENTRADA.mkdir(parents=True, exist_ok=True)
    (ENTRADA / f"{cid}.txt").write_text(
        f"FONTE: {final}\nCAPTURA: portal oficial legislacao.prefeitura.sp.gov.br (container texto_compilado)\nID: {cid}\n\n" + texto + "\n",
        encoding="utf-8")
    d = det(texto)
    tipo = "decreto" if cid.startswith("decreto") else ("lei_complementar" if "-lc-" in cid else "lei_ordinaria")
    meta = {
        "id": cid, "tipo_norma": tipo, "esfera": "municipal", "jurisdicao": "São Paulo/SP",
        "numero": d["numero"], "ano": d["ano"], "ementa": d["ementa"],
        "tema": d["tema"] or ["uso_ocupacao_solo"],
        "dispositivos_chave": d["dispositivos"],
        "vigencia": {"inicio": d["vig_inicio"], "fim": None, "em_vigor": True,
                     "altera": [], "alterada_por": [], "revogada_por": None,
                     "observacao": f"Scaffold deterministico (revisao pendente). Sinais: revogado={d['flag_revogado']} "
                                   f"suspenso={d['flag_suspenso']} ADI={d['flag_adi']} revoga={d['flag_revoga']}."},
        "remissoes": [{"norma": r, "relacao": "citada no texto (detectada automaticamente)"} for r in d["remissoes"]],
        "jurisprudencia_relacionada": [],
        "tem_tabela": bool(re.search(r'\bQuadro\b|\bTabela\b|\bAnexo\b', texto)),
        "tabelas_extraidas": [], "tem_formula": False, "formulas_referenciadas": [],
        "fonte": {"origem": "Portal oficial (legislacao.prefeitura.sp.gov.br)",
                  "path": f"_entrada/misto/{cid}.txt", "url": final,
                  "hash": f"sha256:{sha}", "hash_nota_fonte": "sha256 do HTML bruto do portal capturado 2026-07-13",
                  "ocr": False, "metodo": "captura do portal via scaffold_ingestao.py (verbatim)",
                  "hash_alvo": f"leis/municipal-sp/{cid}.md"},
        "status_pipeline": "bruto", "confianca_extracao": "alta", "revisado_por_humano": False,
        "dominio_primario": dominio, "dominio": [dominio],
    }
    jpath = RAIZ / "leis" / "municipal-sp" / f"{cid}.json"
    jpath.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    mdpath = jpath.with_suffix(".md")
    h1 = titulo or f"{tipo.upper()} Nº {d['numero']} DE {d['ano']}"
    mdpath.write_text(f"# {h1}\n", encoding="utf-8")
    subprocess.run([sys.executable, "scripts/promover_entrada.py", cid], cwd=str(RAIZ), check=True)
    flags = "".join(f" {k[5:].upper()}" for k in ("flag_revogado","flag_suspenso","flag_adi") if d[k])
    print(f"  scaffold {cid} [{dominio}] arts={len(d['dispositivos'])} rem={len(d['remissoes'])} vig={d['vig_inicio']}"
          f"{'  ⚠REVISAR:'+flags if flags else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
consolidar.py — Regenera MANIFESTO.json a partir dos .json individuais de corpus.

Princípio 1.5/2.3 do CLAUDE.md: o MANIFESTO é GERADO (nunca editado à mão); a
consolidação é determinística e roda a cada push (.github/workflows/consolidar.yml),
de modo que o Git nunca dá conflito. Este script é a "Action" referida nos docs.

Lê:  leis/**/<id>.json  e  jurisprudencia/<id>.json   (ignora _capturas/)
Escreve: MANIFESTO.json  (fonte da verdade do status_pipeline de cada item)

Vocabulário canônico de status_pipeline (CLAUDE.md Parte 2.3):
    bruto -> fatiado -> tagueado -> validado -> indexado

Trazido pela Auditoria triplo-limpo do Escritório do MOU — 2026-06-19.
"""
import json
import sys
import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VOCAB = ["bruto", "fatiado", "tagueado", "validado", "indexado"]
# Itens preservados no corpus mas fora do escopo IPTU/TDC (D24: nada se descarta,
# mas não contam como corpus ativo). Ponto cego declarado, aguardando decisão do MOU.
FORA_DE_ESCOPO = {
    "stf-tema-1020": "Tema de ISS, não IPTU (verbatim confirma) — realocar p/ corpus ISS",
    "stj-resp-1658054": "Previdenciário confirmado pela captura (REsp 1.658.054/RS, DJe 29/06/2017, contribuições s/ verbas trabalhistas) — fora do escopo IPTU/TDC; arquivar",
}


def coletar(diretorio: Path):
    itens = []
    for jpath in sorted(diretorio.rglob("*.json")):
        if "_capturas" in jpath.parts:
            continue
        if jpath.name == "MANIFESTO.json":
            continue
        try:
            d = json.loads(jpath.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"ERRO JSON malformado: {jpath} -> {e}", file=sys.stderr)
            sys.exit(1)
        _id = d.get("id") or jpath.stem
        md = jpath.with_suffix(".md")
        status = d.get("status_pipeline")
        item = {
            "id": _id,
            "tipo": d.get("tipo_norma") or d.get("tipo"),
            "caminho_md": str(md.relative_to(RAIZ)) if md.exists() else None,
            "caminho_json": str(jpath.relative_to(RAIZ)),
            "status_pipeline": status,
            "status_valido": status in VOCAB,
            "confianca_extracao": d.get("confianca_extracao"),
            "revisado_por_humano": d.get("revisado_por_humano", False),
            "fora_de_escopo": _id in FORA_DE_ESCOPO,
            "fora_de_escopo_motivo": FORA_DE_ESCOPO.get(_id),
            "fonte_url": (d.get("fonte") or {}).get("url"),
        }
        itens.append(item)
    return itens


def enumerar_nao_corpus():
    """D24-do-git (achado AUD-09/ID-06): os 4 artefatos do projeto (1.1) não são só Lei.
    Engine/Tabela/Tese não entram no corpus (leis/juris) mas PRECISAM aparecer no SSOT — senão
    viram valor preso (D23). Enumera contagem + estado coarse, sem fingir que estão prontos."""
    def _versionavel(p):
        # ignora cache de build (.pyc/__pycache__) — não é artefato e não é determinístico
        # (existe só depois que um .py roda; senão o MANIFESTO deixa de ser idempotente).
        return (p.is_file() and p.suffix not in (".gitkeep", ".pyc")
                and p.name != ".gitkeep" and "__pycache__" not in p.parts)

    def conta(rel):
        d = RAIZ / rel
        return sum(1 for p in d.rglob("*") if _versionavel(p)) if d.exists() else 0
    engines_py = sorted(str(p.relative_to(RAIZ)) for p in (RAIZ / "engines").rglob("*.py")
                        if "__pycache__" not in p.parts)
    return {
        "_nota": "Estado dos artefatos NÃO-corpus (1.1: Tabela/Engine/Tese). Fechamento do D24-do-git (AUD-09).",
        "engines": {"arquivos": conta("engines"), "executavel_py": engines_py,
                    "status": "engine OODC/TDC executável (engines/tdc/oodc.py); demais são prosa/conhecimento"},
        "tabelas": {"arquivos": conta("tabelas"),
                    "status": "VAZIO — Q14/Quadro 3 ainda no Drive, não ingeridos (AUD-04: combustível do engine)"},
        "tese_iptu": {"arquivos": conta("tese/iptu"), "status": "vazio"},
        "tese_tdc": {"arquivos": conta("tese/tdc"), "status": "vazio"},
        "extracao_gems": {"arquivos": conta("extracao/gems"),
                          "status": "material de gens (prosa); material IRRF/Tema 1130 removido em 2026-06-20 (AUD-04)"},
    }


def lei_ids_realmente_indexados():
    """NV-1 (auditoria 2026-06-27): a verdade do 'indexado' é o ÍNDICE + os chunks,
    NÃO o rótulo do .json. Retorna o conjunto de lei_ids que têm chunk em rag/chunks/
    E entrada em rag/index/metadados.json. Sem isso, 'indexado' no .json é falso-verde
    (B-15: 4 leis IPTU diziam 'indexado' com 0 chunks)."""
    idx = RAIZ / "rag" / "index" / "metadados.json"
    no_indice = set()
    if idx.exists():
        try:
            meta = json.loads(idx.read_text(encoding="utf-8"))
            no_indice = {c.get("lei_id") for c in (meta if isinstance(meta, list)
                          else meta.get("chunks", meta.values() if isinstance(meta, dict) else []))
                         if isinstance(c, dict)}
        except (json.JSONDecodeError, OSError, AttributeError):
            no_indice = set()
    com_chunks = {p.name for p in (RAIZ / "rag" / "chunks").glob("*") if p.is_dir() and any(p.iterdir())}
    return no_indice & com_chunks


def main():
    leis = coletar(RAIZ / "leis")
    juris = coletar(RAIZ / "jurisprudencia")
    todos = leis + juris

    ativos = [i for i in todos if not i["fora_de_escopo"]]
    # NV-1: rótulo 'indexado' que NÃO tem chunk no índice = divergência (falso-verde no corpus).
    indexados_reais = lei_ids_realmente_indexados()
    divergencia_indexado = sorted(
        i["id"] for i in todos
        if i["status_pipeline"] == "indexado" and i["id"] not in indexados_reais
    )
    por_status = {}
    for i in ativos:
        por_status[i["status_pipeline"]] = por_status.get(i["status_pipeline"], 0) + 1
    status_ilegais = sorted({i["status_pipeline"] for i in todos if not i["status_valido"]})
    nao_verbatim = [i["id"] for i in ativos if i["confianca_extracao"] in ("baixa", "media")]

    manifesto = {
        "_doc": (
            "Fonte da verdade do status_pipeline de cada item. GERADO por "
            "scripts/consolidar.py a partir dos .json individuais — NAO editar a mao "
            "(Principio 1.5/2.3 do CLAUDE.md). Roda a cada push via "
            ".github/workflows/consolidar.yml."
        ),
        "gerado_em": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "vocabulario_status": VOCAB,
        "resumo": {
            "total_itens": len(todos),
            "leis": len(leis),
            "jurisprudencia": len(juris),
            "ativos_no_escopo": len(ativos),
            "fora_de_escopo": len(todos) - len(ativos),
            "_nota": "por_status_pipeline conta SÓ os ativos_no_escopo; os 2 fora-de-escopo (ambos tagueado) não entram aqui. Soma = ativos_no_escopo, não total_itens.",
            "por_status_pipeline_ativos": por_status,
            "status_ilegais_encontrados": status_ilegais,
            "confianca_baixa_ou_media": len(nao_verbatim),
            "_nota_verbatim": "confianca e flag de extracao, nao prova de verbatim. CORRIGIDO na auditoria profunda 2026-06-20 (AUD-01): 13 leis JA estao em verbatim integral e indexadas (12 federais re-ingeridas de _entrada/misto/ + a 7228/1968 municipal) — supera a narrativa antiga 'planalto deu 403, NENHUMA e verbatim', que confundia 'o .md e resumo' com 'o verbatim nao existe'. Faltam 14 municipais (so resumo WebSearch) — re-ingestao verbatim delas e o que resta do pre-requisito do RAG. As 32 juris (curtas) sao verbatim.",
        },
        "alertas": {
            "status_fora_do_vocabulario": status_ilegais,
            "itens_confianca_baixa_ou_media_a_revisar": nao_verbatim,
            "itens_fora_de_escopo": [i["id"] for i in todos if i["fora_de_escopo"]],
            "indexado_sem_chunks_no_indice": divergencia_indexado,
            "_nota_divergencia": "NV-1 (2026-06-27): ids que dizem status_pipeline=indexado mas NAO tem chunk no rag/index = FALSO-VERDE; o gate (fechar-instancia.py / gate-fechamento.sh) FALHA se esta lista nao for vazia. Vazia = todo 'indexado' e provado pelo indice.",
        },
        "artefatos_nao_corpus": enumerar_nao_corpus(),
        "itens": sorted(todos, key=lambda i: (i["caminho_json"])),
    }

    # Idempotência: só bumpa `gerado_em` se o CONTEÚDO mudou (senão a Action
    # commitaria a cada push só pelo timestamp — ruído infinito).
    out = RAIZ / "MANIFESTO.json"
    if out.exists():
        try:
            antigo = json.loads(out.read_text(encoding="utf-8"))
            a = {k: v for k, v in antigo.items() if k != "gerado_em"}
            b = {k: v for k, v in manifesto.items() if k != "gerado_em"}
            if a == b:
                manifesto["gerado_em"] = antigo.get("gerado_em")
        except (json.JSONDecodeError, OSError):
            pass
    out.write_text(json.dumps(manifesto, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    r = manifesto["resumo"]
    print(f"MANIFESTO.json regenerado: {r['total_itens']} itens "
          f"({r['leis']} leis + {r['jurisprudencia']} juris), "
          f"{r['ativos_no_escopo']} no escopo, {r['fora_de_escopo']} fora.")
    if status_ilegais:
        print(f"  ALERTA status ilegais: {status_ilegais}")
    if divergencia_indexado:
        print(f"  ALERTA NV-1 'indexado' SEM chunk no indice (falso-verde): {divergencia_indexado}")
    print(f"  por status: {por_status}")


if __name__ == "__main__":
    main()

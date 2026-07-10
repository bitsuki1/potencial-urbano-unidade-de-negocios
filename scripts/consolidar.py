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
import hashlib
import json
import sys
import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VOCAB = ["bruto", "fatiado", "tagueado", "validado", "indexado"]
# Itens fora do escopo IPTU/TDC. DECISÃO DO DONO (2026-07-05): os 2 que aguardavam decisão
# (stf-tema-1020 = ISS; stj-resp-1658054 = previdenciário) foram ARQUIVADOS — removidos do
# working tree via `git rm` (recuperáveis pelo histórico git; "nada se apaga do histórico").
# O dict fica como mecanismo: se um item voltar/entrar fora de escopo, registre aqui.
FORA_DE_ESCOPO = {}


def _verifica_hash(d, jpath, hash_nulo, hash_divergente):
    """AUD-A10 — o Gate 1 do pipeline ('hash confere', Parte 3) DE VERDADE: recomputa o sha256
    do alvo declarado (fonte.hash_alvo) e compara com fonte.hash. Nulo ou divergente = gate
    VERMELHO (consolidar sai 1). Backfill inicial: scripts/backfill_hash.py."""
    fonte = d.get("fonte") or {}
    h, alvo = fonte.get("hash"), fonte.get("hash_alvo")
    if not h:
        hash_nulo.append(jpath.stem)
        return
    p = RAIZ / alvo if alvo else None
    if p is None or not p.exists():
        hash_divergente.append(f"{jpath.stem} (alvo ausente: {alvo})")
        return
    atual = "sha256:" + hashlib.sha256(p.read_bytes()).hexdigest()
    if atual != h:
        hash_divergente.append(f"{jpath.stem} ({alvo})")


def coletar(diretorio: Path, hash_nulo, hash_divergente):
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
        _verifica_hash(d, jpath, hash_nulo, hash_divergente)
        _id = d.get("id") or jpath.stem
        md = jpath.with_suffix(".md")
        status = d.get("status_pipeline")
        # B-7/AUD-17: `verbatim_integral` é DERIVADO do marcador do .md ('## Texto integral
        # (verbatim)'), não declarado à mão — prova mecânica de que o .md carrega o articulado
        # integral, não um resumo. (confianca_extracao é flag de extração, NÃO prova de verbatim.)
        verbatim = bool(md.exists() and "## Texto integral (verbatim)" in md.read_text(encoding="utf-8"))
        # B-7 (1.6): vigência DATADA — inicio da vigência, se o .json a declarar (senão None).
        vig = d.get("vigencia") or {}
        vigencia_inicio = vig.get("inicio")
        item = {
            "id": _id,
            "tipo": d.get("tipo_norma") or d.get("tipo"),
            "caminho_md": str(md.relative_to(RAIZ)) if md.exists() else None,
            "caminho_json": str(jpath.relative_to(RAIZ)),
            "status_pipeline": status,
            "status_valido": status in VOCAB,
            "confianca_extracao": d.get("confianca_extracao"),
            "verbatim_integral": verbatim,
            "vigencia_inicio": vigencia_inicio,
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
                    "status": ("VAZIO — nenhuma tabela ingerida (AUD-04: combustível do engine)"
                               if conta("tabelas") == 0 else
                               f"{conta('tabelas')} tabela(s) no git (Q14 valor-terreno, Quadro 3 CA/zona, "
                               "Quadro 5 Fs, Quadro 7 parques, Fi-área LPUOS Art.24) — combustível do engine "
                               "PRESENTE; derivado dos arquivos, não hardcoded")},
        "tese_iptu": {"arquivos": conta("tese/iptu"), "status": "vazio"},
        "tese_tdc": {"arquivos": conta("tese/tdc"), "status": "vazio"},
        "extracao_gems": {"arquivos": conta("extracao/gems"),
                          "status": "material de gens (prosa); material IRRF/Tema 1130 removido em 2026-06-20 (AUD-04)"},
    }


def tabelas_vintage():
    """E2c: vintage + hash de cada tabelas/*.csv git-tracked. Lê data_base de tabelas/METADATA.json."""
    tab_dir = RAIZ / "tabelas"
    meta_path = tab_dir / "METADATA.json"
    meta = {}
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8")).get("tabelas", {})
        except (json.JSONDecodeError, OSError):
            pass
    itens = []
    sem_vintage = []
    for csv_path in sorted(tab_dir.glob("*.csv")):
        nome = csv_path.name
        sha = "sha256:" + hashlib.sha256(csv_path.read_bytes()).hexdigest()
        info = meta.get(nome, {})
        data_base = info.get("data_base")
        if not data_base:
            sem_vintage.append(nome)
        itens.append({
            "arquivo": f"tabelas/{nome}",
            "sha256": sha,
            "data_base": data_base,
            "fonte_legal": info.get("fonte_legal"),
        })
    return itens, sem_vintage


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
    hash_nulo, hash_divergente = [], []
    leis = coletar(RAIZ / "leis", hash_nulo, hash_divergente)
    juris = coletar(RAIZ / "jurisprudencia", hash_nulo, hash_divergente)
    todos = leis + juris

    tab_itens, tab_sem_vintage = tabelas_vintage()

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
    # B-7: contagens DERIVADAS (prova mecânica, não declaração).
    verbatim_integral_n = sum(1 for i in ativos if i["verbatim_integral"])
    # Verbatim indexado que ainda NÃO tem vigência DATADA (1.6) — gap honesto, não escondido.
    indexado_verbatim_sem_vigencia = sorted(
        i["id"] for i in ativos
        if i["verbatim_integral"] and i["status_pipeline"] == "indexado" and not i["vigencia_inicio"]
    )

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
            "_nota": "por_status_pipeline conta SÓ os ativos_no_escopo. Os 2 fora-de-escopo históricos (stf-tema-1020/ISS, stj-resp-1658054/previdenciário) foram ARQUIVADOS por decisão do dono em 2026-07-05 (git rm; recuperáveis pelo histórico).",
            "por_status_pipeline_ativos": por_status,
            "status_ilegais_encontrados": status_ilegais,
            "verbatim_integral_ativos": verbatim_integral_n,
            "_nota_verbatim_integral": "B-7/AUD-17: verbatim_integral e DERIVADO do marcador '## Texto integral (verbatim)' no .md (prova mecanica, nao declaracao). Difere de confianca_extracao (flag do extrator).",
            "confianca_baixa_ou_media": len(nao_verbatim),
            "_nota_verbatim": "confianca e flag de extracao, nao prova de verbatim. CORRIGIDO na auditoria profunda 2026-06-20 (AUD-01): 13 leis JA estao em verbatim integral e indexadas (12 federais re-ingeridas de _entrada/misto/ + a 7228/1968 municipal) — supera a narrativa antiga 'planalto deu 403, NENHUMA e verbatim', que confundia 'o .md e resumo' com 'o verbatim nao existe'. Faltam 12 municipais (so resumo WebSearch) — re-ingestao verbatim delas e o que resta do pre-requisito do RAG. As juris (curtas) sao verbatim.",
        },
        "alertas": {
            "status_fora_do_vocabulario": status_ilegais,
            "itens_confianca_baixa_ou_media_a_revisar": nao_verbatim,
            "itens_fora_de_escopo": [i["id"] for i in todos if i["fora_de_escopo"]],
            "indexado_sem_chunks_no_indice": divergencia_indexado,
            "_nota_divergencia": "NV-1 (2026-06-27): ids que dizem status_pipeline=indexado mas NAO tem chunk no rag/index = FALSO-VERDE; o gate (fechar-instancia.py / gate-fechamento.sh) FALHA se esta lista nao for vazia. Vazia = todo 'indexado' e provado pelo indice.",
            "indexado_verbatim_sem_vigencia_datada": indexado_verbatim_sem_vigencia,
            "_nota_vigencia": "B-7 (1.6): leis verbatim/indexadas que ainda nao tem vigencia.inicio datada. Gap declarado (nao bloqueia o gate) — a datacao das 13 municipais bruto depende do verbatim do Drive (B-4).",
            "fonte_hash_nulo": sorted(hash_nulo),
            "fonte_hash_divergente": sorted(hash_divergente),
            "_nota_hash": "AUD-A10: Gate 1 'hash confere' (Parte 3) — fonte.hash recomputado do fonte.hash_alvo a cada consolidacao; nulo/divergente = consolidar sai 1 (gate VERMELHO). Backfill: scripts/backfill_hash.py.",
        },
        "artefatos_nao_corpus": enumerar_nao_corpus(),
        "tabelas_vintage": tab_itens,
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
    print(f"  tabelas vintage: {len(tab_itens)} CSV(s) rastreadas, {len(tab_sem_vintage)} sem data_base")
    if tab_sem_vintage:
        print(f"  ALERTA E2c: tabelas sem vintage em METADATA.json: {tab_sem_vintage}")
    # AUD-A10 — Gate 1 'hash confere': nulo ou divergente DERRUBA a consolidação (exit 1).
    if hash_nulo or hash_divergente:
        if hash_nulo:
            print(f"  GATE VERMELHO fonte.hash NULO ({len(hash_nulo)}): {hash_nulo[:8]}{'...' if len(hash_nulo) > 8 else ''}",
                  file=sys.stderr)
        if hash_divergente:
            print(f"  GATE VERMELHO fonte.hash DIVERGENTE ({len(hash_divergente)}): {hash_divergente[:8]}",
                  file=sys.stderr)
        print("  (backfill inicial: python3 scripts/backfill_hash.py; divergência = alvo mudou sem re-carimbo intencional)",
              file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

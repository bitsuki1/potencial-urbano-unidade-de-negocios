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
    "stj-resp-1658054": "Matéria previdenciária; nº do REsp não verificado — confirmar ou arquivar",
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


def main():
    leis = coletar(RAIZ / "leis")
    juris = coletar(RAIZ / "jurisprudencia")
    todos = leis + juris

    ativos = [i for i in todos if not i["fora_de_escopo"]]
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
            "_nota_verbatim": "confianca baixa/media NAO e o mesmo que nao-verbatim: os 8 federais + 3 juris com confianca media sao VERBATIM (texto real); os 15 municipais-SP e que sao resumos nao-verbatim (marcador no .md) a re-ingerir.",
        },
        "alertas": {
            "status_fora_do_vocabulario": status_ilegais,
            "itens_confianca_baixa_ou_media_a_revisar": nao_verbatim,
            "itens_fora_de_escopo": [i["id"] for i in todos if i["fora_de_escopo"]],
        },
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
    print(f"  por status: {por_status}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
rodar-evals.py — Roda o ground-truth contra o RAG (CLAUDE.md Parte 3: gate = CITAÇÃO CORRETA).

Para cada item de `evals/ground-truth/*.json`, chama scripts/consultar.py e verifica:
  - fundamentada == esperado (gate 1.7: pergunta fora do corpus DEVE ser NÃO-FUNDAMENTADA);
  - se fundamentada: a citação do TOPO bate no `lei_id` e `dispositivo_topo` esperados,
    e o texto citado contém o trecho `texto_contem` (a resposta cita o dispositivo certo, verbatim).

Arquivos de ground-truth com `"status": "aguardando_verbatim"` são REPORTADOS mas não falham
o build (o corpus-alvo ainda não foi re-ingerido verbatim — é dívida declarada, não bug).

Uso:  python3 evals/rodar-evals.py            # roda tudo; exit !=0 se algum ATIVO falhar
Trazido pela instância orquestradora do Potencial Urbano — 2026-06-20.
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "scripts"))
import consultar as C  # noqa: E402

GT_DIR = RAIZ / "evals" / "ground-truth"


def checar_item(item):
    esp = item.get("espera", {})
    r = C.consultar(item["pergunta"], lei=esp.get("lei_id"), tema=esp.get("tema"),
                    jurisdicao=esp.get("jurisdicao"), top=esp.get("top", 3))
    esperado_fund = esp.get("fundamentada", True)
    if r["fundamentada"] != esperado_fund:
        return False, (f"fundamentada={r['fundamentada']} (esperado {esperado_fund}) "
                       f"| veredito: {r['veredito']}")
    if not esperado_fund:
        return True, "NÃO-FUNDAMENTADA como esperado (gate 1.7 ok)"

    topo = r["resultados"][0]
    cit = topo.get("citacao") or {}
    falhas = []
    if esp.get("lei_id") and topo["chunk_id"].split("::")[0] != esp["lei_id"]:
        falhas.append(f"lei_id topo={topo['chunk_id'].split('::')[0]} != {esp['lei_id']}")
    if esp.get("dispositivo_topo") and esp["dispositivo_topo"].lower() not in (topo.get("rotulo") or "").lower():
        falhas.append(f"dispositivo topo={topo.get('rotulo')!r} != {esp['dispositivo_topo']!r}")
    if esp.get("texto_contem") and esp["texto_contem"].lower() not in (topo.get("texto") or "").lower():
        falhas.append(f"texto do topo não contém {esp['texto_contem']!r}")
    if falhas:
        return False, " ; ".join(falhas)
    return True, (f"topo {topo.get('rotulo')} (cobertura {topo['cobertura']:.0%}) — "
                  f"cita {cit.get('dispositivo')}")


def main():
    arquivos = sorted(GT_DIR.glob("*.json"))
    if not arquivos:
        print("Nenhum ground-truth em evals/ground-truth/.", file=sys.stderr)
        sys.exit(1)

    # PISO DE COBERTURA (achado F-1/F-2 da auditoria 2026-06-20): o gate de evals NÃO pode
    # passar verde sem casos ATIVOS de fato executados. Sem este piso, deletar o único ground-truth
    # ativo OU rebaixá-lo a 'aguardando_verbatim' deixava o gate verde com o RAG destruído.
    MIN_ITENS_ATIVOS = 4

    total = ok = falhou = 0
    falhas_ativas = itens_ativos = 0
    for arq in arquivos:
        gt = json.loads(arq.read_text(encoding="utf-8"))
        aguardando = gt.get("status") == "aguardando_verbatim"
        marca = "  [AGUARDANDO VERBATIM — não bloqueia build]" if aguardando else ""
        print(f"\n=== {arq.name} (domínio {gt.get('dominio','?')}){marca} ===")
        for item in gt.get("itens", []):
            total += 1
            if not aguardando:
                itens_ativos += 1
            passou, detalhe = checar_item(item)
            status = "PASS" if passou else "FALHA"
            if passou:
                ok += 1
            else:
                falhou += 1
                if not aguardando:
                    falhas_ativas += 1
            print(f"  [{status}] {item['id']}: {detalhe}")

    print(f"\nRESUMO: {ok}/{total} PASS, {falhou} falhas "
          f"({falhas_ativas} em ground-truth ATIVO; {itens_ativos} itens ativos executados).")
    if itens_ativos < MIN_ITENS_ATIVOS:
        print(f"GATE VERMELHO: só {itens_ativos} itens ATIVOS (< {MIN_ITENS_ATIVOS}). "
              f"Suíte sem cobertura ativa = evals provam NADA (F-1/F-2). Restaure os ground-truth ATIVOS.",
              file=sys.stderr)
        sys.exit(1)
    sys.exit(1 if falhas_ativas else 0)


if __name__ == "__main__":
    main()

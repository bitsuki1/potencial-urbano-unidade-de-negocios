#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Auditor do relatório da arrumação — Potencial Urbano (IPTU/TDC).

Confere o CSV de saída do Apps Script (arrumarDrive) contra o plano
oficial (de-para-final.csv) e diz, em segundos, se "temos todos os
documentos": o que faltou processar, o que deu ERRO, o que foi pra
destino diferente do planejado e o que ficou na Triagem (99) p/ revisar.

USO:
    python3 auditar-relatorio.py <relatorio.csv> [de-para-final.csv]

Funciona tanto no ENSAIO (status PLANEJADO) quanto na execução real
(MOVIDO / PASTA_MOVIDA / JA_OK).
"""
import csv, sys, os, collections

OK_MOVE = {"MOVIDO", "PASTA_MOVIDA", "JA_OK"}  # "chegou no lugar"
OK_DRY  = {"PLANEJADO", "JA_OK"}               # "vai chegar" (ensaio)


def ler_plano(caminho):
    plano = {}
    with open(caminho, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            plano[r["drive_id"].strip()] = {
                "titulo": r["titulo"].strip(),
                "destino": r["destino"].strip(),
                "tipo": r["tipo"].strip(),
            }
    return plano


def ler_relatorio(caminho):
    """Devolve (linhas_validas, tem_fim, run_headers)."""
    linhas, run_headers, tem_fim = [], [], False
    with open(caminho, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            tipo = (r.get("tipo") or "").strip()
            if tipo.startswith("--- RUN"):
                run_headers.append(tipo)
                continue
            if tipo.startswith("=== FIM") or "FIM." in tipo:
                tem_fim = True
                continue
            if tipo not in ("arquivo", "pasta"):
                continue  # linha de marcador / vazia
            linhas.append({
                "tipo": tipo,
                "id": (r.get("id") or "").strip(),
                "nome": (r.get("nome") or "").strip(),
                "destino": (r.get("destino") or "").strip(),
                "status": (r.get("status") or "").strip(),
                "obs": (r.get("obs") or "").strip(),
            })
    return linhas, tem_fim, run_headers


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    rel_path = sys.argv[1]
    base = os.path.dirname(os.path.abspath(__file__))
    plano_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(base, "de-para-final.csv")

    plano = ler_plano(plano_path)
    linhas, tem_fim, runs = ler_relatorio(rel_path)

    vistos = collections.Counter(l["id"] for l in linhas)
    por_id = {l["id"]: l for l in linhas}  # último vence (idempotência)
    status_ct = collections.Counter(l["status"] for l in linhas)

    ids_plano = set(plano)
    ids_vistos = set(vistos)

    faltando   = ids_plano - ids_vistos                 # nunca processados
    inesperado = ids_vistos - ids_plano                 # no relatório, fora do plano
    duplicados = {i: n for i, n in vistos.items() if n > 1}
    erros      = [l for l in linhas if l["status"] == "ERRO"]

    # destino divergente do planejado
    divergentes = []
    for i, l in por_id.items():
        if i in plano and l["destino"] and l["destino"] != plano[i]["destino"]:
            divergentes.append((l["nome"], l["destino"], plano[i]["destino"]))

    triagem = [l for l in linhas if l["destino"].startswith("99")]

    modo = "REAL (movendo)" if (status_ct.get("MOVIDO") or status_ct.get("PASTA_MOVIDA")) else "ENSAIO (dry-run)"
    ok_set = OK_MOVE if "REAL" in modo else OK_DRY
    no_lugar = sum(v for k, v in status_ct.items() if k in ok_set)

    W = 64
    p = print
    p("=" * W)
    p(" AUDITORIA DA ARRUMAÇÃO — POTENCIAL URBANO")
    p("=" * W)
    for h in runs:
        p(" " + h.replace("---", "").strip())
    p(f" Modo detectado .......: {modo}")
    p(f" Plano (de-para) ......: {len(ids_plano)} itens")
    p(f" Processados (relat.) .: {len(ids_vistos)} itens únicos ({len(linhas)} linhas)")
    p(f" 'No lugar certo' .....: {no_lugar}")
    p(f" Terminou (=== FIM ===): {'SIM' if tem_fim else 'NÃO — rodou parcial / em andamento'}")
    p("-" * W)
    p(" STATUS:")
    for k, v in status_ct.most_common():
        p(f"   {v:5}  {k or '(vazio)'}")
    p("-" * W)

    # Veredito
    completo = not faltando and not erros and tem_fim
    p(" VEREDITO:")
    if completo:
        p(f"   ✅ COMPLETO. Todos os {len(ids_plano)} itens do plano estão")
        p(f"      contemplados, 0 erro, relatório fechado com FIM.")
    else:
        p("   ⚠️  AINDA NÃO está 100%. Pendências abaixo.")
    p("=" * W)

    def bloco(titulo, itens, fmt, limite=40):
        p(f"\n▼ {titulo}: {len(itens)}")
        for x in list(itens)[:limite]:
            p("   - " + fmt(x))
        if len(itens) > limite:
            p(f"   ... (+{len(itens) - limite})")

    if faltando:
        bloco("FALTAM processar (no plano, ausentes no relatório)",
              sorted(faltando), lambda i: f"{plano[i]['titulo'][:55]}  [{plano[i]['destino']}]")
    if erros:
        bloco("ERROS", erros, lambda l: f"{l['nome'][:50]} | {l['obs'][:60]}")
    if divergentes:
        bloco("DESTINO diferente do planejado", divergentes,
              lambda t: f"{t[0][:45]}  foi p/ {t[1]}  (plano: {t[2]})")
    if duplicados:
        bloco("DUPLICADOS no relatório", duplicados.items(),
              lambda kv: f"{por_id[kv[0]]['nome'][:50]}  ({kv[1]}x)")
    if inesperado:
        bloco("INESPERADOS (no relatório, fora do plano)", sorted(inesperado),
              lambda i: f"{por_id[i]['nome'][:50]}  ({i})")

    p(f"\n▼ Na TRIAGEM (99) p/ revisar manualmente depois: {len(triagem)}")
    p("   (esperado 10 — itens ambíguos; ver DECISOES.md AF-11)")

    p("\n" + "=" * W)
    sys.exit(0 if completo else 2)


if __name__ == "__main__":
    main()

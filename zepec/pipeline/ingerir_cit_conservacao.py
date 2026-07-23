#!/usr/bin/env python3
"""
ingerir_cit_conservacao.py — casa o CIT (Cadastro de Imóveis Tombados, consulta oficial da Prefeitura
de SP) por SQL na camada de CONSERVAÇÃO dos cedentes ZEPEC, produzindo a base OFICIAL do tombamento
que fundamenta o Art. 129 do PDE (TDC de imóvel tombado/de interesse de preservação).

FONTE (1.3/1.7): `zepec/oficial/cit-tombamento.csv` — resultado VERBATIM da consulta CIT por SQL, rodada
no runner `brasil` (IP-BR) via `portfolio-automacoes` Action `cit-batch` (4.292 SQLs, 0 erro). Cada linha
traz o NÍVEL de preservação oficial + os ATOS de tombamento (Resoluções CONPRESP/CONDEPHAAT), que são a
CITAÇÃO da base legal do tombamento.

REGRA (1.8): a coluna `nivel_preservacao` do CIT é a FONTE PRIMÁRIA. Ela NÃO sobrescreve o `tipo_zepec`
já existente (que veio de outra origem) — a saída RECONCILIA os dois e SURFAÇA a divergência (nunca
esconde). `SEM_DADO` do CIT fica `SEM_DADO` (nada inventado).

Saída: `zepec/oficial/conservacao_cedentes.csv` — por sql_mestre:
  sql_mestre, cit_nivel_preservacao, cit_atos_tombamento, cit_situacao, cit_denominacao,
  tipo_zepec_atual, reconciliacao  (CONFIRMA | DIVERGE | SEM_DADO | SEM_CIT)

Uso:  python3 zepec/pipeline/ingerir_cit_conservacao.py
"""
import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
CIT = RAIZ / "zepec" / "oficial" / "cit-tombamento.csv"
CEDENTES = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes.csv"
SAIDA = RAIZ / "zepec" / "oficial" / "conservacao_cedentes.csv"

# níveis do CIT que caracterizam tombamento/proteção (para reconciliar com o nosso 'tombado')
NIVEIS_PROTEGIDO = {
    "TOMBADO", "TOMBADO - PRESERVAÇÃO TOTAL", "TOMBADO - PRESERVAÇÃO DE FACHADAS E VOLUMETRIA",
    "TOMBADO - PRESERVAÇÃO VOLUMÉTRICA", "TOMBADO SÓ IPHAN", "EM PROCESSO DE TOMBAMENTO",
    "ENVOLTORIA DE IMÓVEL TOMBADO", "ENVOLTÓRIA SÓ CONPRESP", "ENVOLTÓRIA SÓ CONDEPHAAT", "AMBIENTAL",
}


def main():
    cit = {r["sql"]: r for r in csv.DictReader(open(CIT, encoding="utf-8"))}
    cedentes = list(csv.DictReader(open(CEDENTES, encoding="utf-8")))

    stats = {"CONFIRMA": 0, "DIVERGE": 0, "SEM_DADO": 0, "SEM_CIT": 0}
    linhas = []
    for c in cedentes:
        sql = c["sql_mestre"]
        r = cit.get(sql)
        tipo = c.get("tipo_zepec") or ""
        nosso_protegido = "tombado" in tipo or "BIR" in tipo or "APC" in tipo
        if not r:
            recon = "SEM_CIT"
            linhas.append((sql, "", "", "", "", tipo, recon))
        else:
            nivel = r["nivel_preservacao"]
            if nivel == "SEM_DADO":
                recon = "SEM_DADO"
            elif nivel == "NAO TOMBADO/NAO CONSTA":
                recon = "CONFIRMA" if not nosso_protegido else "DIVERGE"
            else:
                cit_protegido = nivel in NIVEIS_PROTEGIDO
                recon = "CONFIRMA" if cit_protegido == nosso_protegido else "DIVERGE"
            linhas.append((sql, nivel, r.get("atos_tombamento", ""), r.get("situacao", ""),
                           r.get("denominacao", ""), tipo, recon))
        stats[recon] = stats.get(recon, 0) + 1

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SAIDA, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sql_mestre", "cit_nivel_preservacao", "cit_atos_tombamento", "cit_situacao",
                    "cit_denominacao", "tipo_zepec_atual", "reconciliacao"])
        for ln in linhas:
            w.writerow(ln)

    tot = len(cedentes)
    print(f"OK: {tot} cedentes -> {SAIDA}")
    print(f"  CONFIRMA (CIT bate tipo_zepec): {stats['CONFIRMA']}")
    print(f"  DIVERGE  (CIT × tipo_zepec)    : {stats['DIVERGE']}  <- revisar (CIT é primário, 1.8)")
    print(f"  SEM_DADO (CIT sem retorno)     : {stats['SEM_DADO']}  <- fica SEM_DADO, nada inventado")
    print(f"  SEM_CIT  (SQL fora do lote)    : {stats['SEM_CIT']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

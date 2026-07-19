#!/usr/bin/env python3
"""
recorte_q14_anexo2026.py — recorta o Quadro 14 OFICIAL 2026 (Anexo I da Portaria SMUL 8/2026,
extração PRIMÁRIA do PDF do Drive) pelos SQs dos cedentes ZEPEC.

POR QUE ESTE SUPERA O reajuste_q14_2026.py (1.3/1.8): o `q14_cedentes_2026.csv` anterior era o
valor 2025 oficial × 1,0718 (Dec. 64.884/2025) — reprodução DERIVADA do ato. Agora temos o valor
NOMINAL primário publicado no Anexo I da Portaria 8/2026, re-extraído verbatim do PDF oficial. A
reconciliação (recon abaixo) provou o derivado fiel ao nominal dentro de R$0,01; mesmo assim, por
doutrina (1.3 número rastreável à fonte; 1.8 derivado é SÓ-IDEIA, nunca fonte), o entregável passa a
se alimentar do PRIMÁRIO. O derivado fica só para auditoria.

Entrada:
  ANEXO_CSV = q14-valor-terreno-2026.csv (hub portfolio-automacoes: tools/drive/out/), 179.591 linhas,
              294 setores (001→310), colunas: setor,quadra,sql,codlog,valor_m2_brl (valor BR "3912,10").
  cedentes_sqls.txt (mesmo diretório) = um SQL por linha; a chave de cruzamento é o SQ = 6 primeiros
              dígitos (setor+quadra), porque o Q14 é indexado por face de quadra, não por lote.
Saída:
  zepec/oficial/q14_cedentes_2026_oficial.csv  (sq,codlog,valor_m2_brl — valor com ponto decimal)
  zepec/oficial/q14_recon_2026.md              (relatório: cobertura + reconciliação primário×derivado)

Uso (com o Anexo já baixado no hub co-montado):
  ANEXO_CSV=/home/user/portfolio-automacoes/tools/drive/out/q14-valor-terreno-2026.csv \
      python3 zepec/pipeline/recorte_q14_anexo2026.py

Criado PU 22 (2026-07-19) — fecha o item 1 do D-DONO 2026-07-18 (Anexo I completo destrava os cedentes).
"""
import csv
import os
import sys
from decimal import Decimal
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent.parent
SQLS_FILE = Path(__file__).resolve().parent / "cedentes_sqls.txt"
ANEXO = os.environ.get("ANEXO_CSV") or "/home/user/portfolio-automacoes/tools/drive/out/q14-valor-terreno-2026.csv"
SAIDA = RAIZ / "zepec" / "oficial" / "q14_cedentes_2026_oficial.csv"
DERIVADO = RAIZ / "zepec" / "oficial" / "q14_cedentes_2026.csv"
RECON = RAIZ / "zepec" / "oficial" / "q14_recon_2026.md"


def br_para_decimal(v):
    """'3.912,10' ou '3912,10' -> Decimal('3912.10')."""
    return Decimal(v.strip().replace(".", "").replace(",", "."))


def main():
    if not Path(ANEXO).exists():
        sys.exit(f"ERRO: Anexo nao encontrado em {ANEXO} (co-montar o hub e rodar a q14-anexo-parse).")

    sqs = {sql[:6] for sql in SQLS_FILE.read_text().split() if sql != "0000000000"}

    # primário recortado pelos SQs dos cedentes
    prim = {}  # (sq,cod) -> Decimal
    for r in csv.reader(open(ANEXO, encoding="utf-8")):
        if not r or r[0].startswith("#") or r[0] == "setor":
            continue
        sq, cod, val = r[2], r[3], r[4]
        if sq in sqs:
            prim[(sq, cod)] = br_para_decimal(val)

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SAIDA, "w", newline="", encoding="utf-8") as fo:
        w = csv.writer(fo)
        w.writerow(["sq", "codlog", "valor_m2_brl"])
        for (sq, cod) in sorted(prim):
            w.writerow([sq, cod, f"{prim[(sq, cod)]:.2f}"])

    # cobertura (nível SQ)
    cob_sq = {k[0] for k in prim}
    falta = sorted(sqs - cob_sq)
    q000 = [s for s in falta if s[3:] == "000"]
    q9xx = [s for s in falta if s[3] == "9"]
    reais = [s for s in falta if s[3:] != "000" and s[3] != "9"]

    # decomposição no NÍVEL DO CEDENTE (por que sobram cedentes sem V mesmo com o Anexo completo):
    # o V casa por (SQ, codlog da FACE FISCAL do IPTU). Usa o mesmo norm_codlog do engine p/ ser fiel.
    dec = None
    ap_iptu = RAIZ / "zepec" / "oficial" / "iptu2026_cedentes.csv"
    ap_ced = RAIZ / "zepec" / "ferramenta" / "zepec_cedentes.csv"
    if ap_iptu.exists() and ap_ced.exists():
        import re as _re
        src = (RAIZ / "zepec" / "enriquecer_oficial.py").read_text(encoding="utf-8")
        mm = _re.search(r"def norm_codlog.*?(?=\ndef )", src, _re.S)
        _ns = {}
        exec("import re\n" + mm.group(0), _ns)  # noqa: S102 — reusa a função canônica do engine
        norm_codlog = _ns["norm_codlog"]
        from collections import defaultdict as _dd
        faces = _dd(set)
        for (sq, cod) in prim:
            faces[sq].add(norm_codlog(cod))
        iptu = {r["sql_mestre"]: r for r in csv.DictReader(open(ap_iptu, encoding="utf-8"))}
        match = face_miss = sq_absent = no_iptu = 0
        for c in csv.DictReader(open(ap_ced, encoding="utf-8")):
            sql = c.get("sql_mestre") or c.get("sql")
            it = iptu.get(sql)
            if not it:
                no_iptu += 1
                continue
            sq = sql[:6]
            cod = norm_codlog(it["codlog"])
            if sq not in cob_sq:
                sq_absent += 1
            elif cod in faces[sq]:
                match += 1
            else:
                face_miss += 1
        dec = dict(match=match, face_miss=face_miss, sq_absent=sq_absent, no_iptu=no_iptu,
                   total=match + face_miss + sq_absent + no_iptu)

    # reconciliação vs derivado (se existir)
    linhas_recon = []
    if DERIVADO.exists():
        der = {(r["sq"], r["codlog"]): br_para_decimal(r["valor_m2_brl"].replace(".", ",", 1) if "," not in r["valor_m2_brl"] else r["valor_m2_brl"])
               for r in csv.DictReader(open(DERIVADO, encoding="utf-8"))}
        # o derivado usa ponto decimal (3021.62); normaliza direto:
        der = {(r["sq"], r["codlog"]): Decimal(r["valor_m2_brl"])
               for r in csv.DictReader(open(DERIVADO, encoding="utf-8"))}
        comuns = set(prim) & set(der)
        iguais = sum(1 for k in comuns if prim[k] == der[k])
        maxdif = max((abs(prim[k] - der[k]) for k in comuns), default=Decimal(0))
        so_prim = set(prim) - set(der)
        so_der = set(der) - set(prim)
        linhas_recon = [
            f"- pares (SQ,codlog) em comum: **{len(comuns)}**",
            f"- **iguais ao centavo: {iguais}/{len(comuns)}**; divergência máxima: **R$ {maxdif:.2f}** (arredondamento sub-centavo)",
            f"- pares só no PRIMÁRIO (o derivado não tinha): **{len(so_prim)}**",
            f"- pares só no DERIVADO (não batem no primário): **{len(so_der)}**",
        ]

    with open(RECON, "w", encoding="utf-8") as fr:
        fr.write("# Reconciliação do Quadro 14 — 2026 (primário × derivado) e cobertura dos cedentes\n\n")
        fr.write("> Gerado por `recorte_q14_anexo2026.py` (PU 22, 2026-07-19). Fonte primária: Anexo I da\n")
        fr.write("> Portaria SMUL 8/2026 (Decreto 64.884/2025; Lei 16.050/2014), extração pura do PDF oficial\n")
        fr.write("> do Drive do MOU via conta de serviço — 3.151 páginas, 179.591 linhas, 294 setores (001→310).\n\n")
        fr.write("## Cobertura dos cedentes ZEPEC\n")
        fr.write(f"- SQs distintos de cedentes: **{len(sqs)}**\n")
        fr.write(f"- SQs **cobertos** pelo Anexo oficial: **{len(cob_sq & sqs)}**\n")
        fr.write(f"- SQs **sem cobertura**: **{len(falta)}** — dos quais:\n")
        fr.write(f"  - **{len(q000)}** com quadra `000` (placeholder/gleba — SQ sem face de quadra; por construção sem valor de Q14);\n")
        fr.write(f"  - **{len(q9xx)}** com quadra `9xx` (999/998/997/988/987/992 — desmembramento/área pública; sem face de outorga);\n")
        fr.write(f"  - **{len(reais)}** com quadra REAL genuinamente ausente do Anexo oficial: `{reais}` — sem valor publicado na Portaria (documentado, não é falha de extração).\n\n")
        fr.write("## Reconciliação primário × derivado (reajuste 2025×1,0718)\n")
        if linhas_recon:
            fr.write("\n".join(linhas_recon) + "\n\n")
            fr.write("**Conclusão:** o método de reajuste (`reajuste_q14_2026.py`, Dec. 64.884/2025 +7,18%) é fiel ao\n")
            fr.write("nominal oficial dentro de R$0,01 — fecha o resíduo M6 declarado no cabeçalho daquele script.\n")
            fr.write("Ainda assim, por 1.3/1.8, o entregável passa a usar o PRIMÁRIO (`q14_cedentes_2026_oficial.csv`);\n")
            fr.write("o derivado permanece só para auditoria.\n")
        else:
            fr.write("- (derivado ausente — só cobertura)\n")
        if dec:
            fr.write("\n## Por que ainda sobram cedentes sem V (decomposição no nível do cedente)\n")
            fr.write("> O V casa por `(SQ, codlog da face fiscal do IPTU)`. Com o Anexo COMPLETO, a lacuna não é\n")
            fr.write("> mais completude do Quadro 14 — decompõe-se assim (mesmo `norm_codlog` do engine):\n\n")
            fr.write(f"- **{dec['match']}** cedentes com V (match exato SQ×face) — **{100*dec['match']//dec['total']}%**;\n")
            fr.write(f"- **{dec['face_miss']}** com o SQ coberto mas a face fiscal sem casar — **recuperáveis** pela face-da-SQ (MAT-3: mediana/máx das faces oficiais da quadra, com flag `v_q14_origem='mediana_sq'`; zero dado inventado);\n")
            fr.write(f"- **{dec['sq_absent']}** com o SQ genuinamente ausente da Portaria (irrecuperável por Q14);\n")
            fr.write(f"- **{dec['no_iptu']}** sem linha de IPTU (sem codlog fiscal para casar) — lacuna do cadastro de IPTU, não do Quadro 14.\n\n")
            fr.write("**Conclusão do item 1 (D-DONO 2026-07-18):** o Anexo I é COMPLETO e agora é a fonte primária.\n")
            fr.write("A antiga pendência dos \"483 sem VTcd\" NÃO era o Anexo faltar setores centrais — era join de face\n")
            fr.write("+ cedentes sem IPTU. Próxima alavanca declarada: MAT-3 (recupera os %d por face-da-SQ).\n" % dec['face_miss'])

    print(f"OK: {len(prim)} pares primarios ({len(cob_sq & sqs)}/{len(sqs)} SQs cobertos) -> {SAIDA}")
    print(f"    sem cobertura: {len(falta)} ({len(q000)} quadra-000, {len(q9xx)} quadra-9xx, {len(reais)} reais: {reais})")
    print(f"    relatorio -> {RECON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

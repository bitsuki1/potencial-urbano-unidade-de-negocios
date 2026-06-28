#!/usr/bin/env python3
"""
extrair_quadros.py — Extração PURA (1.2) das TABELAS do PDE (Quadros anexos à Lei 16.050/2014)
para `tabelas/*.csv` = combustível determinístico do engine (1.1/1.3; destrava B-1 e B-3).

NÃO interpreta, NÃO calcula: só recorta o verbatim cru de `_entrada/tdc/pde2013-subst2-quadro-*.txt`
em linhas de dado rastreáveis. Cada CSV carrega a proveniência (fileId/quadro) no cabeçalho-comentário.

- Quadro 14 (Cadastro de Valor de Terreno) -> tabelas/q14-valor-terreno.csv  [V por SQ — entrada do OODC]
- Quadro 5  (Fator de interesse social Fs)  -> tabelas/quadro5-fator-social-fs.csv  [Fs]

VERIFICA: valida que SQ == setor+quadra em cada registro do Q14 (RO-04: número exato, não fabricado);
reporta total e descartados. Idempotente.

Uso: python3 scripts/extrair_quadros.py
Trazido pelo orquestrador do PU — 2026-06-24 (destrave H1: tabela do engine).
"""
import re, csv, sys
from pathlib import Path
RAIZ = Path(__file__).resolve().parent.parent
ENT = RAIZ / "_entrada" / "tdc"

# Registro Q14: SSS QQQ SSSQQQ CCCCCC  9.999,99   (valor BR: ponto=milhar, virgula=decimal)
RE_Q14 = re.compile(r"\b(\d{3})\s+(\d{3})\s+(\d{6})\s+(\d{6})\s+(\d{1,3}(?:\.\d{3})*,\d{2})")

def fonte_id(p):
    m = re.search(r"fileId=(\S+)", Path(p).read_text(encoding="utf-8")); return m.group(1) if m else "?"

def extrair_q14():
    p = ENT / "pde2013-subst2-quadro-14-cadastro.txt"
    if not p.exists(): return print("  FALTA Quadro 14")
    txt = p.read_text(encoding="utf-8")
    regs, descart = [], 0
    for setor, quadra, sq, codlog, valor in RE_Q14.findall(txt):
        if sq != setor + quadra:          # integridade: SQ tem que ser setor+quadra
            descart += 1; continue
        regs.append((setor, quadra, sq, codlog, valor))
    # dedup exata
    vis, uniq = set(), []
    for r in regs:
        if r not in vis: vis.add(r); uniq.append(r)
    out = RAIZ / "tabelas" / "q14-valor-terreno.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        f.write(f"# Quadro 14 (Cadastro de Valor de Terreno) — Anexo da Lei 16.050/2014 (PDE-SP). "
                f"Fonte: Google Drive fileId={fonte_id(p)}, extração pura 2026-06-24. V = valor do m2 de terreno por SQL (R$).\n")
        w = csv.writer(f); w.writerow(["setor","quadra","sql","codlog","valor_m2_brl"])
        for r in uniq: w.writerow(r)
    print(f"  OK  Quadro 14 -> {out.relative_to(RAIZ)} : {len(uniq)} SQLs (descartados por SQ!=setor+quadra: {descart})")
    return uniq

def extrair_q5():
    p = ENT / "pde2013-subst2-quadro-5-fator-interesse-social-fs.txt"
    if not p.exists(): return print("  FALTA Quadro 5")
    txt = p.read_text(encoding="utf-8")
    # pares "<rótulo textual> <valor 0,0..1,0>" — captura cada categoria com seu Fs
    pares = re.findall(r"([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ /–\-\.]+?)\s+([01],\d)", txt)
    out = RAIZ / "tabelas" / "quadro5-fator-social-fs.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        f.write(f"# Quadro 5 (Fator de interesse social Fs) — Anexo Lei 16.050/2014. "
                f"Fonte: Drive fileId={fonte_id(p)}, extração pura 2026-06-24. Fs por categoria de uso.\n")
        w = csv.writer(f); w.writerow(["categoria_uso","fs"])
        for rot, val in pares:
            w.writerow([rot.strip(), val])
    print(f"  OK  Quadro 5  -> {out.relative_to(RAIZ)} : {len(pares)} categorias de Fs")
    return pares

def _strip_nota(v):
    """'2 (d)'->'2' ; '2,5 (f)'->'2,5' ; '(k)'->'NA' ; 'NA'->'NA'."""
    v = re.sub(r"\s*\([a-z]\)\s*", "", v).strip()
    return "NA" if (not v or v.startswith("(")) else v

def _nota(v):
    """Retorna a letra de nota de rodapé do valor, ou '' . '2,5 (f)' -> 'f' ; '4 (g)' -> 'g'."""
    m = re.search(r"\(([a-z])\)", v); return m.group(1) if m else ""

def extrair_q3():
    """Quadro 3 LPUOS (CA por ZONA) -> tabelas/quadro3-ca-por-zona.csv. Fonte ';'-delimitada;
    zona=col2, CA_min=col3, CA_bas=col5, CA_max=col6 (índices base-0). PRESERVA a nota condicional
    do CA_max (achado A-080: nota (d)(f)(g)... condiciona o valor; jogá-la fora vira número errado)."""
    p = ENT / "quadro3-ca-por-zona-lpuos.csv"
    if not p.exists(): return print("  FALTA Quadro 3")
    linhas = [l for l in p.read_text(encoding="utf-8").splitlines() if not l.startswith("#")]
    RE_ZONA = re.compile(r"^[A-Z]{1,5}(-[A-Z0-9]+)*[a-z]?$")   # ZEU, ZC, ZEIS-1, ZCOR-2, AVP-1, AIa...
    regs = []
    for ln in linhas:
        c = ln.split(";")
        if len(c) < 7: continue
        zona = re.sub(r"\s*\([a-z]\)\s*", "", c[2]).strip()
        if zona in ("ZONA","TIPO","CA"): continue          # linhas de cabeçalho
        if not RE_ZONA.match(zona): continue
        cmin, cbas, cmax = _strip_nota(c[3]), _strip_nota(c[5]), _strip_nota(c[6])
        nota = _nota(c[6])                                  # nota do CA_max (condicional)
        regs.append((zona, cmin, cbas, cmax, nota))
    out = RAIZ / "tabelas" / "quadro3-ca-por-zona.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        f.write(f"# Quadro 3 (CA por ZONA) — LPUOS Lei 16.402/2016. Fonte: Google Drive fileId={fonte_id(p)}, "
                f"extração pura 2026-06-24. CA_max = coef. de aproveitamento máximo por zona (entrada do OODC).\n")
        f.write("# ca_max_nota: letra da nota de rodapé do PDF que CONDICIONA o CA_max (A-080). "
                "Legenda NÃO veio no cru — capturar do PDF antes de usar em produção (ex.: ZEIS (f)(g)(h) = condição por tipo de HIS). "
                "Engine: oodc_por_imovel avisa quando ca_max_nota != ''.\n")
        w = csv.writer(f); w.writerow(["zona","ca_min","ca_basico","ca_max","ca_max_nota"])
        for r in regs: w.writerow(r)
    cond = sum(1 for r in regs if r[4])
    print(f"  OK  Quadro 3  -> {out.relative_to(RAIZ)} : {len(regs)} zonas ({cond} com CA_max CONDICIONAL — nota preservada)")
    return regs

def main():
    print("Extração de quadros (combustível do engine):")
    q14 = extrair_q14() or []
    extrair_q5()
    extrair_q3()
    if q14:
        vals = [float(r[4].replace(".","").replace(",",".")) for r in q14]
        print(f"\n  Sanidade Q14: V min=R${min(vals):,.2f} max=R${max(vals):,.2f} (n={len(vals)}). "
              f"Exemplo: SQL {q14[0][2]} -> R${q14[0][4]}/m2.")
    print("\nextrair_quadros: feito. Próximo: ligar tabelas/ ao oodc.py (B-1) — V por SQL, CA_max por zona.")

if __name__ == "__main__":
    main()

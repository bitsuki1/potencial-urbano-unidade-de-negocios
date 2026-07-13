#!/usr/bin/env python3
"""
gerar_placar_vistoria.py — FECHAMENTO da vistoria de proveniência por conteúdo.
Junta os PROVENIENCIA-shard*.csv (dedup por drive_id) → PROVENIENCIA-DE-PARA.csv, gera o PLACAR-VISTORIA.md
(placar + matrizes + amostra de auditoria) e o DE-PARA-06-COMERCIAL.csv (o que serve p/ achar proprietário).
Tudo local (git/Bash). READ-ONLY no Drive. PU 19 · 2026-07-13.
"""
import csv
import glob
import collections
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DIR = RAIZ / "inventario" / "drive-pu"
COLS = ["drive_id", "nome", "mime", "ext", "bytes", "classe", "comercial", "metodo",
        "confianca", "evidencia_conteudo", "sha256_lido", "n_chars", "path_contexto"]


def carregar():
    """Junta todos os shards, dedup por drive_id (última classificação vence)."""
    por_id = {}
    for fn in sorted(glob.glob(str(DIR / "PROVENIENCIA-shard*.csv"))):
        with open(fn, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                did = (r.get("drive_id") or "").strip()
                if did:
                    por_id[did] = r
    return list(por_id.values())


def main():
    linhas = carregar()
    total = len(linhas)

    # de-para consolidado
    with open(DIR / "PROVENIENCIA-DE-PARA.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in sorted(linhas, key=lambda x: (x.get("classe", ""), x.get("nome", ""))):
            w.writerow({k: r.get(k, "") for k in COLS})

    classe = collections.Counter(r.get("classe", "?") for r in linhas)
    comercial = sum(1 for r in linhas if (r.get("comercial") or "").strip() == "sim")
    conf = collections.Counter((r.get("confianca") or "?").strip() for r in linhas)
    cxm = collections.defaultdict(collections.Counter)   # classe × metodo
    for r in linhas:
        cxm[r.get("classe", "?")][(r.get("metodo") or "?").split("+")[0]] += 1
    ileg_ext = collections.Counter((r.get("ext") or "?").lower() for r in linhas if r.get("classe") == "ILEGIVEL")

    def top_nomes(cl, n=10):
        vis, out = set(), []
        for r in linhas:
            if r.get("classe") != cl:
                continue
            nome = (r.get("nome") or "").strip()
            key = nome.lower()
            if key in vis:
                continue
            vis.add(key); out.append(nome)
            if len(out) >= n:
                break
        return out

    def amostra(cl, n=5):
        out = []
        for r in linhas:
            if r.get("classe") == cl and (r.get("evidencia_conteudo") or "").strip():
                out.append((r.get("nome", "")[:45], (r.get("evidencia_conteudo") or "")[:90]))
                if len(out) >= n:
                    break
        return out

    L = []
    L.append("# PLACAR — Vistoria de proveniência por CONTEÚDO do Drive PU · 2026-07-13")
    L.append("> Cada arquivo foi ABERTO (SA), o texto real extraído (PDF/OCR/planilha/shape/header) e classificado")
    L.append("> pela EVIDÊNCIA do conteúdo — nunca por nome/pasta/tag. Regra de ouro: nenhuma classe sem evidência.")
    L.append(f"> De-para completo: `inventario/drive-pu/PROVENIENCIA-DE-PARA.csv` ({total} arquivos únicos).\n")
    L.append(f"## Placar — {total} arquivos abertos e classificados")
    L.append("| Classe | Qtd | % | O que é / destino |")
    L.append("|---|---:|---:|---|")
    destino = {"OFICIAL": "fonte oficial auditável → corpus (02/03/05)",
               "NAO_OFICIAL_EXTERNO": "base de terceiro (externa) → usável no comercial (06) / apoio",
               "CRIADO": "gerado/derivado por nós → só ideia (90), NÃO usar como fonte",
               "ILEGIVEL": "aberto, sem conteúdo legível (majoritariamente imagem nossa) → material-bruto (90)",
               "PENDENTE": "ambíguo não resolvido → revisar"}
    for cl, q in classe.most_common():
        L.append(f"| **{cl}** | {q} | {q/total*100:.1f}% | {destino.get(cl,'')} |")
    L.append(f"\n**Comercial (serve p/ achar proprietário): {comercial}** · Confiança: " +
             " · ".join(f"{k}={v}" for k, v in conf.most_common()))

    L.append("\n## Como cada classe foi decidida (classe × método de extração)")
    L.append("| Classe | " + " | ".join(sorted({m for c in cxm.values() for m in c})) + " |")
    metodos = sorted({m for c in cxm.values() for m in c})
    L.append("|---|" + "|".join("---:" for _ in metodos) + "|")
    for cl, _ in classe.most_common():
        L.append(f"| {cl} | " + " | ".join(str(cxm[cl].get(m, 0)) for m in metodos) + " |")

    L.append("\n## ILEGÍVEL por extensão (prova: é dominado por imagem = extração nossa, não fonte perdida)")
    L.append("| ext | qtd |\n|---|---:|")
    for e, q in ileg_ext.most_common(12):
        L.append(f"| {e or '(sem)'} | {q} |")

    for cl in ("OFICIAL", "NAO_OFICIAL_EXTERNO", "CRIADO"):
        L.append(f"\n## Top nomes — {cl}")
        for nm in top_nomes(cl):
            L.append(f"- {nm}")

    L.append("\n## Amostra de auditoria (o trecho real que decidiu — reabra qualquer linha no CSV)")
    for cl in ("OFICIAL", "NAO_OFICIAL_EXTERNO", "CRIADO", "ILEGIVEL"):
        L.append(f"\n**{cl}:**")
        for nm, ev in amostra(cl):
            L.append(f"- `{nm}` → {ev}")

    (RAIZ / "inventario" / "PLACAR-VISTORIA.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # de-para do 06 — Comercial
    com = [r for r in linhas if (r.get("comercial") or "").strip() == "sim"]
    with open(DIR / "DE-PARA-06-COMERCIAL.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["drive_id", "nome", "classe", "ext", "bytes", "evidencia_conteudo", "destino"])
        w.writeheader()
        for r in sorted(com, key=lambda x: -int(x.get("bytes") or 0)):
            w.writerow({"drive_id": r.get("drive_id", ""), "nome": r.get("nome", ""), "classe": r.get("classe", ""),
                        "ext": r.get("ext", ""), "bytes": r.get("bytes", ""),
                        "evidencia_conteudo": (r.get("evidencia_conteudo") or "")[:150], "destino": "06 — Comercial"})

    print(f"total={total}  classe={dict(classe)}  comercial={len(com)}")
    print(f"ILEGIVEL por ext (top): {dict(ileg_ext.most_common(6))}")
    print("gerado: PROVENIENCIA-DE-PARA.csv · PLACAR-VISTORIA.md · DE-PARA-06-COMERCIAL.csv")


if __name__ == "__main__":
    main()

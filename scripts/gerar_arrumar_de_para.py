#!/usr/bin/env python3
"""
gerar_arrumar_de_para.py — Gera o DE-PARA completo da arrumação do Drive PU (roadmap
`inventario/ROADMAP-ARRUMACAO-DRIVE-PU.md`): cada arquivo do catálogo → sua PASTA DESTINO canônica.

Entrada:  inventario/CATALOGO-DRIVE-PU-2026-07-12.csv  (33.138 arquivos tagueados)
          inventario/drive-pu/RESGATE-CANDIDATOS.csv    (396 oficiais mal-tagueados → forçar canônico)
Saída:    inventario/drive-pu/ARRUMAR-DE-PARA.csv        (drive_id, nome, destino, motivo, dentro_todos_tdc)

Regra de destino (na ordem — a 1ª que casa vence):
  1. RESGATE (id na lista)                → canônico por tema/tipo (2ª-olhada do MOU: nada oficial pro lixo)
  2. duplicata forte / descarte (lixo)    → 99 — APAGAR (pasta única; mantém 1 canônica por grupo)
  3. KEEPER (oficial não-dup / USAR / COMERCIAL) → canônico por tema/tipo
  4. SO_IDEIA (fragmento/chunk/SILVER)    → 90 — Material bruto (só ideias)
  5. resto (desconhecido não-dup)         → 90 (material bruto; o MOU revisa 1-a-1, NUNCA lixo às cegas)

Doutrina: nada órfão (todo arquivo recebe destino), nada oficial pro lixo sem resgate (correção do MOU
2026-07-12: "TODOS TDC não é só não-auditável"), uma pasta APAGAR só. PU 19.
"""
import csv
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CATALOGO = RAIZ / "inventario" / "CATALOGO-DRIVE-PU-2026-07-12.csv"
RESGATE = RAIZ / "inventario" / "drive-pu" / "RESGATE-CANDIDATOS.csv"
SAIDA = RAIZ / "inventario" / "drive-pu" / "ARRUMAR-DE-PARA.csv"

# Nomes EXATOS das pastas canônicas (casam com as já existentes na raiz POTENCIAL URBANO; o mover reusa).
D_GOV = "00 — Governança & Índice"
D_LEIS = "02 — Leis & Jurisprudência"
D_TAB = "03 — Tabelas & Engines"
D_TESE = "04 — Tese (Antítese/Vacina)"
D_GEO = "05 — Geo / Mapas"
D_COM = "06 — Comercial"
D_BRUTO = "90 — Material bruto (só ideias)"
D_APAGAR = "99 — APAGAR (duplicados e descarte)"

LAKE_PREFIXES = ("02_SILVER", "01A_BRONZE", "01_BRONZE", "01C_BRONZE", "04_ORIGINAIS",
                 "06_CRIADOS", "03_GOLD", "00_ADMIN", "99_LIXEIRA", "99_QUARENTENA", "99_")


def canonico_por_tema_tipo(tema, tipo):
    """Roteia um keeper/resgatado para a pasta canônica por tema+tipo (o 'devido lugar')."""
    tema = (tema or "").upper(); tipo = (tipo or "").upper()
    if tema == "COMERCIAL":
        return D_COM
    if tema == "GEO" or tipo == "GEO_SHP":
        return D_GEO
    if tipo in ("TABELA_DADO", "PLANILHA"):
        return D_TAB
    if tema == "GOVERNANCA":
        return D_GOV
    if tema in ("JURIDICO", "TDC", "IPTU") or tipo in ("LEI", "DECRETO", "PORTARIA", "JURISPRUDENCIA", "PDF", "DOC_GOOGLE"):
        return D_LEIS
    # keeper de tema OUTRO sem sinal forte: vai p/ Leis (é doc oficial) — canônico, nunca bruto/lixo.
    return D_LEIS


def main():
    resgate_ids = set()
    if RESGATE.exists():
        with open(RESGATE, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                did = (row.get("drive_id") or "").strip()
                if did:
                    resgate_ids.add(did)

    from collections import Counter
    dest_n = Counter(); motivo_n = Counter()
    linhas = []
    with open(CATALOGO, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did = (row.get("drive_id") or "").strip()
            if not did:
                continue
            nome = (row.get("nome") or "").strip()
            tema = (row.get("tema") or "").strip()
            tipo = (row.get("tipo_artefato") or "").strip()
            ofi = (row.get("oficialidade") or "").strip().upper()
            uso = (row.get("uso") or "").strip().upper()
            dup = (row.get("dup_forte") or "").strip().upper() == "SIM"
            desc = (row.get("descarte") or "").strip().upper() == "SIM"
            path = (row.get("path") or "").strip()
            top = path.split("/")[0] if path else ""
            dentro = "SIM" if top.startswith(LAKE_PREFIXES) else "NAO"

            keeper = (ofi == "OFICIAL") or (uso in ("USAR", "COMERCIAL"))
            # PROTEÇÃO (correção do MOU): norma oficial NÃO-duplicada nunca vai pro lixo, mesmo com flag
            # descarte (o tagueador às vezes marcou descarte por engano). Só cópia-forte (dup) de norma vai.
            juridico_oficial = keeper and (tema.upper() in ("JURIDICO", "TDC", "IPTU")
                                           or tipo.upper() in ("LEI", "DECRETO", "PORTARIA", "JURISPRUDENCIA"))

            if did in resgate_ids:                              # 1. RESGATE
                destino = canonico_por_tema_tipo(tema, tipo); motivo = "resgate"
            elif juridico_oficial and not dup:                  # 1b. norma oficial não-dup: PROTEGIDA do lixo
                destino = canonico_por_tema_tipo(tema, tipo); motivo = "keeper_protegido"
            elif dup or desc:                                    # 2. duplicata/lixo
                destino = D_APAGAR; motivo = "duplicata" if dup else "descarte"
            elif keeper:                                         # 3. keeper oficial
                destino = canonico_por_tema_tipo(tema, tipo); motivo = "keeper_oficial"
            elif uso == "SO_IDEIA":                              # 4. só ideia
                destino = D_BRUTO; motivo = "so_ideia"
            else:                                                # 5. resto → bruto (revisão do dono)
                destino = D_BRUTO; motivo = "residuo_revisar"

            dest_n[destino] += 1; motivo_n[motivo] += 1
            linhas.append({"drive_id": did, "nome": nome, "destino": destino,
                           "motivo": motivo, "tema": tema, "tipo": tipo, "dentro_todos_tdc": dentro})

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with open(SAIDA, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["drive_id", "nome", "destino", "motivo", "tema", "tipo", "dentro_todos_tdc"])
        w.writeheader(); w.writerows(linhas)

    print(f"ARRUMAR-DE-PARA.csv: {len(linhas)} arquivos")
    print("== por DESTINO ==")
    for d, n in dest_n.most_common():
        print(f"  {n:7d}  {d}")
    print("== por MOTIVO ==")
    for m, n in motivo_n.most_common():
        print(f"  {n:7d}  {m}")


if __name__ == "__main__":
    main()

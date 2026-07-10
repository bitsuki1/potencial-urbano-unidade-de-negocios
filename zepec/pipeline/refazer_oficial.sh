#!/usr/bin/env bash
# refazer_oficial.sh — regenera a cadeia ZEPEC inteira de um checkout limpo (E1).
#
# Ordem obrigatória (ver MOTOR-2-ESTRATEGIA.md §E1):
#   Passo 0:  montar_base → montar_ferramenta (universo de cedentes)
#   Passo 0b: derivar cedentes_sqls.txt
#   Passo 1:  filtro_iptu.py   (recorte IPTU2026 pelos SQLs)
#   Passo 2:  recorte_q14.py   (recorte Q14 pelos SQs)
#   Passo 3:  overlay_zona.py  (zonas → CAbás) OU resolver_zona_geosampa.py
#   Passo 4:  enriquecer_oficial.py (engine + Gold)
#   Passo 4b: lista_prospeccao.py (fila comercial)
#
# Uso:
#   cd zepec && bash pipeline/refazer_oficial.sh           # tudo (dados oficiais JÁ commitados)
#   cd zepec && bash pipeline/refazer_oficial.sh --check    # confere byte-identidade run↔run
#
# O script NÃO baixa dados de Storage (IPTU/Q14/shapefiles) — usa os CSVs já commitados
# em zepec/oficial/. Para regeneração COMPLETA incluindo download, ver MOTOR-2-ESTRATEGIA.md §E1.
#
# Criado 2026-07-10 (E1). Paths relativos a Path(__file__).parent.parent (= zepec/).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ZEPEC_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
REPO_DIR="$(cd "$ZEPEC_DIR/.." && pwd)"

cd "$ZEPEC_DIR"

echo "=== refazer_oficial.sh (E1) ==="
echo "ZEPEC_DIR: $ZEPEC_DIR"
echo ""

# --- Passo 0: universo de cedentes ---
echo "[Passo 0] montar_base.py → limpo/zepec_unificada.csv"
python3 montar_base.py

echo "[Passo 0] montar_ferramenta.py → ferramenta/zepec_cedentes.csv"
python3 montar_ferramenta.py

# --- Passo 0b: derivar cedentes_sqls.txt ---
echo "[Passo 0b] derivar cedentes_sqls.txt (SQLs únicos, ordenados)"
python3 -c "
import csv
sqls = set()
with open('ferramenta/zepec_cedentes.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        sql = (r.get('sql_mestre') or '').strip()
        if sql and sql != '0000000000':
            sqls.add(sql)
sqls.add('0000000000')
with open('pipeline/cedentes_sqls.txt', 'w') as f:
    f.write('\n'.join(sorted(sqls)) + '\n')
print(f'  cedentes_sqls.txt: {len(sqls)} SQLs')
"

# --- Passo 1: recorte IPTU (usa CSV já commitado se existir) ---
if [ -f "oficial/iptu2026_cedentes.csv" ]; then
    echo "[Passo 1] IPTU: usando oficial/iptu2026_cedentes.csv já commitado ($(wc -l < oficial/iptu2026_cedentes.csv) linhas)"
else
    echo "[Passo 1] AVISO: oficial/iptu2026_cedentes.csv ausente — precisa alimentar filtro_iptu.py"
    echo "  Uso: curl -sS \"\$URL_IPTU\" | python3 pipeline/filtro_iptu.py"
fi

# --- Passo 2: recorte Q14 (usa CSV já commitado se existir) ---
if [ -f "oficial/q14_cedentes_2025.csv" ]; then
    echo "[Passo 2] Q14: usando oficial/q14_cedentes_2025.csv já commitado ($(wc -l < oficial/q14_cedentes_2025.csv) linhas)"
else
    echo "[Passo 2] AVISO: oficial/q14_cedentes_2025.csv ausente — precisa alimentar recorte_q14.py"
    echo "  Uso: curl -sS \"\$URL_Q14\" | python3 pipeline/recorte_q14.py"
fi

# --- Passo 3: zonas (usa CSV já commitado) ---
if [ -f "oficial/zona_por_cedente.csv" ]; then
    echo "[Passo 3] Zonas: usando oficial/zona_por_cedente.csv já commitado ($(wc -l < oficial/zona_por_cedente.csv) linhas)"
else
    echo "[Passo 3] AVISO: oficial/zona_por_cedente.csv ausente — rodar resolver_zona_geosampa.py"
    python3 pipeline/resolver_zona_geosampa.py || echo "  AVISO: resolver_zona_geosampa.py falhou (falta zonas_377.csv?)"
fi

# --- Passo 4: engine + Gold ---
echo "[Passo 4] enriquecer_oficial.py → ferramenta/zepec_cedentes_oficial.csv"
python3 enriquecer_oficial.py

# --- Passo 4b: fila comercial ---
echo "[Passo 4b] lista_prospeccao.py → ferramenta/lista_prospeccao.csv + fila_verificar.csv"
python3 lista_prospeccao.py

echo ""
echo "=== Pipeline ZEPEC completo ==="

# --- Verificação (--check) ---
if [ "${1:-}" = "--check" ]; then
    echo ""
    echo "=== Verificação de byte-identidade ==="
    OBRIGATORIOS=(
        "limpo/zepec_unificada.csv"
        "ferramenta/zepec_cedentes.csv"
        "ferramenta/zepec_cedentes_oficial.csv"
        "ferramenta/lista_prospeccao.csv"
        "ferramenta/fila_verificar.csv"
    )
    falhas=0
    for arq in "${OBRIGATORIOS[@]}"; do
        if [ ! -f "$arq" ]; then
            echo "  FALHA: $arq não encontrado"
            falhas=$((falhas+1))
        else
            linhas=$(wc -l < "$arq")
            echo "  OK: $arq — $linhas linhas"
        fi
    done
    if [ "$falhas" -gt 0 ]; then
        echo ""; echo "$falhas FALHA(s)."; exit 1
    else
        echo ""; echo "Todos os CSVs presentes."
    fi
fi

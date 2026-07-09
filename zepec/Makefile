# Makefile — Orquestrador mínimo do pipeline ZEPEC (Motor de Dados / Potencial Urbano).
#
# Ordem obrigatória (cada etapa depende da saída da anterior):
#   1. montar_base.py          → limpo/zepec_unificada.csv
#   2. donos.py + fundurb.py   (paralelo, opcional — enriquecem com titularidade e FUNDURB)
#   3. montar_ferramenta.py    → ferramenta/zepec_cedentes.csv
#   4. enriquecer_oficial.py   → ferramenta/zepec_cedentes_oficial.csv
#   5. lista_prospeccao.py     → ferramenta/lista_prospeccao.csv + ferramenta/fila_verificar.csv
#
# Uso:
#   make pipeline      — roda tudo na ordem certa
#   make check         — verifica se todos os CSVs existem e têm linhas
#   make limpar        — remove os CSVs gerados (para forçar re-execução)
#
# Princípio 1.3: número nasce no engine; este Makefile só orquestra, não calcula.

PYTHON ?= python3

# --- Alvos intermediários (saídas de cada etapa) ---
BASE       := limpo/zepec_unificada.csv
DONOS      := limpo/donos_encontrados.csv
FUNDURB    := limpo/fundurb_processos.csv
CEDENTES   := ferramenta/zepec_cedentes.csv
OFICIAL    := ferramenta/zepec_cedentes_oficial.csv
PROSPECCAO := ferramenta/lista_prospeccao.csv
FILA       := ferramenta/fila_verificar.csv

# --- Fontes (para dependência de Make) ---
RAW_DECL   := raw/lista_declaracoes_ZEPEC-BIR_agosto-2025.csv
RAW_CERT   := raw/lista_certidao_ZEPEC-BIR_agosto-2025.csv
RAW_TOMB   := raw/SIRGAS_SHP_benstombados1.csv
RAW_APC    := raw/SIRGAS_SHP_ZEPEC1_apc.csv

.PHONY: pipeline check limpar etapa1 etapa2 etapa3 etapa4 etapa5

# === PIPELINE COMPLETO ===
pipeline: etapa1 etapa2 etapa3 etapa4 etapa5
	@echo ""
	@echo "Pipeline ZEPEC completo."

# === ETAPA 1 — Base unificada ===
etapa1: $(BASE)

$(BASE): montar_base.py $(RAW_DECL) $(RAW_CERT) $(RAW_TOMB) $(RAW_APC)
	$(PYTHON) montar_base.py

# === ETAPA 2 — Donos + FUNDURB (paralelo, opcional) ===
# Nota: donos.py e fundurb.py são independentes e podem rodar em paralelo (make -j2 etapa2).
# Se os arquivos-fonte não existirem, a etapa é silenciosamente pulada.
etapa2: $(DONOS) $(FUNDURB)

$(DONOS): donos.py $(CEDENTES)
	@if [ -d raw/externo ]; then $(PYTHON) donos.py; else echo "AVISO: raw/externo/ ausente — donos.py pulado."; fi

$(FUNDURB): fundurb.py
	@if [ -f raw/externo/fundurb_fila_tdc_5pct_dez2025.csv ]; then $(PYTHON) fundurb.py; else echo "AVISO: fonte FUNDURB ausente — fundurb.py pulado."; fi

# === ETAPA 3 — Ferramenta (1 linha/imóvel) ===
etapa3: $(CEDENTES)

$(CEDENTES): montar_ferramenta.py $(BASE)
	$(PYTHON) montar_ferramenta.py

# === ETAPA 4 — Enriquecimento oficial (IPTU + Q14 + Zona) ===
etapa4: $(OFICIAL)

$(OFICIAL): enriquecer_oficial.py $(CEDENTES)
	$(PYTHON) enriquecer_oficial.py

# === ETAPA 5 — Listas de prospecção ===
etapa5: $(PROSPECCAO)

$(PROSPECCAO) $(FILA): lista_prospeccao.py $(OFICIAL)
	$(PYTHON) lista_prospeccao.py

# === VERIFICAÇÃO — confere que todos os CSVs existem e têm linhas ===
check:
	@falhas=0; \
	for arq in $(BASE) $(CEDENTES) $(OFICIAL) $(PROSPECCAO) $(FILA); do \
	  if [ ! -f "$$arq" ]; then \
	    echo "FALHA: $$arq não encontrado."; falhas=$$((falhas+1)); \
	  else \
	    linhas=$$(wc -l < "$$arq"); \
	    if [ "$$linhas" -le 1 ]; then \
	      echo "FALHA: $$arq tem $$linhas linha(s) (esperado > 1)."; falhas=$$((falhas+1)); \
	    else \
	      echo "OK: $$arq — $$linhas linhas."; \
	    fi; \
	  fi; \
	done; \
	for arq in $(DONOS) $(FUNDURB); do \
	  if [ -f "$$arq" ]; then \
	    linhas=$$(wc -l < "$$arq"); \
	    echo "OK (opcional): $$arq — $$linhas linhas."; \
	  else \
	    echo "INFO: $$arq ausente (etapa opcional)."; \
	  fi; \
	done; \
	if [ "$$falhas" -gt 0 ]; then echo ""; echo "$$falhas FALHA(s) encontrada(s)."; exit 1; \
	else echo ""; echo "Todos os CSVs obrigatórios presentes e com dados."; fi

# === LIMPAR — remove saídas geradas (força re-execução) ===
limpar:
	rm -f $(BASE) $(DONOS) $(FUNDURB) $(CEDENTES) $(OFICIAL) $(PROSPECCAO) $(FILA)
	@echo "CSVs gerados removidos."

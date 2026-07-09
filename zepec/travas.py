#!/usr/bin/env python3
"""travas.py — REGISTRO CENTRAL de todas as travas (constraints/guards) do pipeline ZEPEC.

Fachada: cada trava permanece implementada no módulo de origem (princípio da responsabilidade
única); este módulo importa e re-exporta todas, servindo como ponto de consulta único.
Nenhuma lógica duplicada — só ponteiros.

Travas registradas:
  1. cessao_vedada()              — montar_base.py
     Art. 124 §2º, Lei 16.050/2014: categorias AUE (Área de Urbanização Especial) e
     APPa (Área de Proteção Paisagística) são VEDADAS à cessão de PCpt.

  2. elegibilidade_conservacao()  — montar_base.py
     Art. 129, Lei 16.050/2014 (red. Lei 17.975/2023): gate de conservação.
     3 estados: ELEGIVEL (Atestado), PENDENTE_CONSERVACAO (Termo de Compromisso),
     SEM_ATESTADO (sem evidência / resolução de tombamento ≠ conservação).

  3. negociabilidade()            — montar_ferramenta.py
     Regra composta: esgotado (certidão) > vedado por lei (AUE/APPa) > prova de
     negociação (declarou/vendeu) > sinais de suspeita (bem público, área, OU, sem lote).
     Devolve (negociavel, motivo, sinais_revisar).
     NOTA: import lazy — montar_ferramenta.py tem código de nível de módulo com efeitos
     colaterais (lê CSVs e grava saída); importar diretamente re-executaria o pipeline.

  4. regime_pcpt()                — enriquecer_oficial.py
     Art. 24 caput LPUOS × Art. 125 §1º I PDE: separa JÁ_DECLARADO (PCpt da Declaração,
     não do escalonado) de PROSPECCAO_NOVA (escalonado é o estimador lícito).

Uso:
    from travas import cessao_vedada, elegibilidade_conservacao, negociabilidade, regime_pcpt
"""

# --- 1. cessao_vedada (Art. 124 §2º) ---
from montar_base import cessao_vedada

# --- 2. elegibilidade_conservacao (Art. 129, Lei 16.050/2014) ---
from montar_base import elegibilidade_conservacao

# --- 3. negociabilidade (regra composta: esgotado > vedado > prova > sinais) ---
# Import lazy: montar_ferramenta.py executa o pipeline inteiro a nível de módulo (sem guard
# __name__=="__main__"). Importar diretamente causaria re-execução e re-gravação dos CSVs.
# A função é exposta via wrapper que importa sob demanda, preservando a assinatura original.
def negociabilidade(nome, tem_decl, tem_cert, vedado, esg, sem_lote, ouc):
    """Wrapper lazy para montar_ferramenta.negociabilidade (evita efeito colateral de módulo).
    Assinatura e retorno idênticos ao original."""
    from montar_ferramenta import negociabilidade as _neg
    return _neg(nome, tem_decl, tem_cert, vedado, esg, sem_lote, ouc)

# --- 4. regime_pcpt (Art. 24 caput LPUOS × Art. 125 §1º I PDE) ---
from enriquecer_oficial import regime_pcpt

__all__ = [
    "cessao_vedada",
    "elegibilidade_conservacao",
    "negociabilidade",
    "regime_pcpt",
]

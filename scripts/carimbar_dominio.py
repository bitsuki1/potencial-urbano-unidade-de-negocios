#!/usr/bin/env python3
"""
carimbar_dominio.py — Carimba o DOMÍNIO (tdc | iptu | compartilhado) em cada norma e acórdão.

Constituição da separação TDC×IPTU (plano `docs/PLANO-ARRUMACAO-DRIVE-2026-07-04.md`):
- O domínio é METADADO, não pasta (uma norma pode servir aos dois). `leis/` segue por ESFERA.
- Vocabulário FECHADO: tdc · iptu · compartilhado. `compartilhado` = lar único que ENTRA nas
  consultas dos DOIS domínios (consultar.py: `alvo ∈ dominio OR "compartilhado" ∈ dominio`) — por
  construção NÃO perde nada (decisão do dono 2026-07-04: "não quero correr o risco de perder nada").
- Regra de fronteira do EFEITO JURÍDICO (plano §4): potencial construtivo→tdc; tributo IPTU→iptu;
  os dois / matriz-geral→compartilhado. Na dúvida → compartilhado (viés de não-perda).
- Anti-padrão eliminado: `tema[]` NÃO carrega mais 'IPTU'/'TDC' (domínio saiu do lugar errado —
  hoje 28× IPTU e 3× TDC enterrados em tema[]; ver leis/federal/lei-federal-9514-1997.json).

Grava (idempotente) em cada `leis/**/*.json` e `jurisprudencia/*.json`:
  "dominio_primario": "<tdc|iptu|compartilhado>",   # 1 valor: efeito jurídico dominante do DOCUMENTO
  "dominio": ["<...>"]                                 # array (vocab fechado) p/ o filtro pré-busca (2.6)
e remove os tokens 'IPTU'/'TDC' de `tema[]`.

Este arquivo É o registro auditável da classificação (cada compartilhado traz a RAZÃO). O dono pode
estreitar depois: mover um id de COMPARTILHADO para IPTU/TDC aqui e re-rodar (idempotente).

Uso:  python3 scripts/carimbar_dominio.py            # aplica
      python3 scripts/carimbar_dominio.py --check    # só verifica (não escreve; exit≠0 se faltar)
"""
import json
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
VOCAB = {"tdc", "iptu", "compartilhado"}

# --- COMPARTILHADO: serve aos DOIS domínios (lar único, incluído nas consultas de ambos). ---
# Chave = stem do arquivo (basename sem .json). Cada um com a RAZÃO (efeito jurídico duplo / matriz).
COMPARTILHADO = {
    "ec-132-2023":
        "Reforma tributária (STN): toca o IPTU E o financiamento urbano/outorga — matriz (P4).",
    "lei-federal-6015-1973":
        "Registros públicos / matrícula / titularidade: base do registro da CERTIDÃO de transferência "
        "de potencial (TDC) E da titularidade para o IPTU (P3).",
    "lei-municipal-saopaulo-12350-1997":
        "Incentivo fiscal a imóveis TOMBADOS (restauro de fachada): universo ZEPEC/tombamento (TDC) E "
        "incentivo de IPTU (P3) — a prospecção TDC de tombados precisa alcançá-la.",
    "lei-municipal-saopaulo-16050-2014":
        "PDE — Plano Diretor Estratégico: arts. 122-133 são TDC/outorga E há parâmetros que afetam a "
        "base de cálculo do IPTU (P3). dominio_primario=compartilhado; quebra por-dispositivo é onda futura.",
    "lei-municipal-saopaulo-16402-2016":
        "LPUOS — zoneamento: alimenta o CAbás do PCpt (TDC) E os parâmetros urbanísticos que refletem no "
        "IPTU (P3).",
    "lei-municipal-saopaulo-16642-2017":
        "COE — Código de Obras e Edificações: define a área construída, que alimenta o potencial (TDC) E "
        "a base de cálculo do IPTU (P3).",
    "lei-municipal-saopaulo-17975-2023":
        "Revisão intermediária do PDE (Lei 16.050/2014): arts. 47-52 são TDC (potencial construtivo "
        "transferível, renovação de declarações) E há parâmetros urbanísticos que afetam o IPTU. "
        "Mesma lógica do PDE (compartilhado).",
    "lei-municipal-saopaulo-18081-2024":
        "Revisão parcial da LPUOS (Lei 16.402/2016): arts. 43-52 são TDC (equivalência, potencial "
        "construtivo) E parâmetros de zoneamento/CA/TO que refletem no IPTU. "
        "Mesma lógica da LPUOS (compartilhado).",
    "lei-municipal-saopaulo-17202-2019":
        "Regularização de edificações: Art. 13 fórmula outorga onerosa C=(At/Ac)×V×Fs×Fp×Fr "
        "(potencial construtivo — TDC) E Art. 5/26 referem isenção/remissão IPTU (P3).",
    "lei-municipal-saopaulo-17577-2021":
        "Requalifica Centro: Art. 11 ZEPEC-BIR pode requisitar TDC E Art. 16 remissão/isenção IPTU "
        "progressiva (3+5 anos). Serve aos dois domínios (P3).",
    "lei-federal-10257-2001":
        "Estatuto da Cidade (regulamenta arts. 182/183 da CF) — base FEDERAL dos instrumentos: OODC "
        "(arts. 28-31) e TDC (art. 35) DO lado urbanístico E IPTU progressivo no tempo (art. 7) DO lado "
        "tributário. Serve aos DOIS domínios (compartilhado). Ingerido do Planalto 2026-07-13.",
    # --- Lote Etapa D ingerido do portal 2026-07-19 (PU 22): normas gerais/duais — nenhuma é potencial
    #     puro nem tributo IPTU puro; na dúvida → compartilhado (viés de não-perda, plano §4). ---
    "decreto-saopaulo-57521-2016":
        "Regulamenta a LPUOS (Lei 16.402/2016) — ocupação do solo e instalação dos usos; toca potencial "
        "construtivo adicional/coeficientes (TDC) E parâmetros urbanísticos que refletem no IPTU (P3). "
        "Segue a lógica compartilhada da própria LPUOS; arts. revogados por 63.504/2024 e 63.884/2024 (vigência per-artigo no verbatim).",
    "decreto-saopaulo-57776-2017":
        "Regulamenta o COE (Lei 16.642/2017) e a CEUSO — define área construída/edificação, que alimenta o "
        "potencial (TDC) E a base de cálculo do IPTU (P3). Mesma lógica compartilhada do COE.",
    "decreto-saopaulo-57770-2017":
        "Regulamenta o SIG-SP (Sistema de Informações Geográficas) — infraestrutura de dado cadastral/espacial "
        "que serve tanto ao Mapa do TDC quanto ao cadastro do IPTU. Matriz-geral → compartilhado.",
    "decreto-saopaulo-57299-2016":
        "Procedimento eletrônico de abertura/registro/alteração de empresas — norma administrativa geral, "
        "não é potencial construtivo nem tributo IPTU; na dúvida → compartilhado (viés de não-perda).",
    "lei-municipal-saopaulo-15150-2010":
        "Polo Gerador de Tráfego — aprovação de projetos e obras de mitigação de impacto viário; parâmetro "
        "urbanístico de licenciamento que toca uso/ocupação (dois domínios). Compartilhado (viés de não-perda).",
    "lei-municipal-saopaulo-14094-2005":
        "CADIN Municipal (cadastro de inadimplentes) — registro fiscal que alcança débitos de IPTU (P3) E "
        "pendências gerais; serve aos dois domínios. Compartilhado.",
}
# --- TDC puro: efeito exclusivo de potencial construtivo. Hoje VAZIO em leis/ — a massa normativa TDC
# (Decreto 57.536/2016, decretos ZEPEC/CONPRESP) ainda não foi ingerida; entrará marcada 'tdc'. ---
TDC = {
    # A-05 (auditoria 2026-07-05): a Lei 17.844/2022 é a lei-NÚCLEO da Transferência do Direito de
    # Construir (menciona TDC/potencial construtivo 77×). Estava mistagueada `iptu` → `--dominio tdc`
    # a excluía silenciosamente (a lei mais on-point do projeto sumia da consulta TDC).
    "lei-municipal-saopaulo-17844-2022":
        "Lei da Transferência do Direito de Construir (TDC) — potencial construtivo passível de "
        "transferência; efeito jurídico é TDC puro (não tributo IPTU).",
    "decreto-saopaulo-57536-2016":
        "Decreto que REGULAMENTA a TDC sem doação (arts. 124/125 do PDE) — núcleo normativo do rito "
        "cedente (etapas, DPC, extrato de transferência). Efeito jurídico é TDC puro. Ingerido 2026-07-05 (AUD-A11).",
    "decreto-saopaulo-58289-2018":
        "Decreto que REGULAMENTA a TDC COM doação (arts. 123/126/127/128/130/131 do PDE) — par do "
        "57.536/2016; revoga o 57.535/2016. Efeito jurídico é TDC puro. Capturado do portal oficial "
        "2026-07-10 (fecha AUD-A11: o corpo do 58.289 era o que restava).",
    "lei-municipal-saopaulo-18222-2024":
        "PIU Arco Pinheiros — cria AIU-ACP com potencial construtivo adicional de 1.150.000 m² (Art. 23), "
        "CA máximo 6,0, transferência de potencial construtivo (Arts. 42-43). Efeito dominante é TDC/potencial.",
    "lei-municipal-saopaulo-18298-2025":
        "Revisão da Lei 18.222/2024 (PIU/AIU Arco Pinheiros) para a ZOE-Butantan — parâmetros urbanísticos "
        "(CA, TO, gabarito, potencial), mapas e Quadro 3A do PIU. Segue o domínio da lei-mãe 18.222 (TDC). "
        "Arts. 3-5 (multas/posturas da LPUOS) com eficácia suspensa por ADI. Ingerida do portal 2026-07-13 (gap).",
    "decreto-saopaulo-63999-2024":
        "Atualiza o Quadro 14 (Cadastro de Valor de Terreno p/ Outorga Onerosa, anexo à Lei 16.050/2014) em "
        "+4,5% (art. 118 do PDE) e o valor de referência do incentivo de TDC para parques (art. 127) para "
        "R$ 2.194,50/m². Fonte-norma da série de reajuste do engine (art128/oodc). Efeito TDC/outorga. Portal 2026-07-13.",
    "decreto-saopaulo-58176-2018":
        "Altera o § 1º do art. 20 do Decreto 57.536/2016 (regulamento da TDC sem doação) e disciplina a "
        "transferência de potencial construtivo sob o art. 15 §1 da LPUOS. TDC puro. Ingerido do portal 2026-07-13.",
    # --- Lote TDC ingerido do portal 2026-07-13 (11 normas urbanísticas; scaffold + revisão de vigência). ---
    "decreto-saopaulo-58955-2019": "Decreto APROVA RÁPIDO (licenciamento urbanístico) — potencial/CA no rito de aprovação. Efeito urbanístico/TDC.",
    "decreto-saopaulo-57565-2016": "Regulamenta a aplicação da Quota Ambiental (LPUOS 16.402/2016) — parâmetro de ocupação/potencial. TDC/urbanístico.",
    "decreto-saopaulo-59164-2019": "Regulamenta a Lei 17.202/2019 (regularização) — fórmula de outorga/potencial construtivo. Efeito dominante TDC.",
    "decreto-saopaulo-59886-2020": "Consolida a disciplina de uso e ocupação do solo p/ empreendimentos — parâmetros urbanísticos/potencial. TDC.",
    "decreto-saopaulo-58028-2017": "Decreto APROVA RÁPIDO (licenciamento) — rito de aprovação com potencial/CA. Efeito urbanístico/TDC.",
    "decreto-saopaulo-63437-2024": "Equivalência entre subcategorias de uso das leis de zoneamento (LPUOS) — parâmetro de uso. TDC/urbanístico.",
    "decreto-saopaulo-64018-2025": "Regulamenta a Lei 18.079/2024 (Projeto de Intervenção Urbana) — PIU/potencial construtivo. Efeito TDC.",
    "lei-municipal-saopaulo-17217-2019": "Revoga parcialmente planos de melhoramentos viários — afeta perímetros/zoneamento urbanístico. TDC/urbanístico.",
    "lei-municipal-saopaulo-17734-2022": "Regulamenta procedimentos urbanísticos (uso/ocupação/potencial) no Município. Efeito TDC/urbanístico.",
    "lei-municipal-saopaulo-18209-2024": "Altera o mapa 2 (art. 383 da LPUOS 16.402/2016) — zoneamento/potencial. Efeito TDC/urbanístico.",
    "decreto-saopaulo-63728-2024": "Estabelece disciplina de parcelamento, uso e ocupação do solo — parâmetros urbanísticos/potencial. TDC.",
    "decreto-saopaulo-63504-2024": "Regime GERAL da Outorga Onerosa do Direito de Construir (OODC) — regulamenta o art. 117 do PDE; fonte-norma da fórmula C=(At/Ac)·V·Fp·Fs dos engines. TDC puro.",
    "decreto-saopaulo-64884-2025": "Atualiza o Quadro 14 (+7,18%, exercício 2026) e o incentivo de TDC p/ parques (R$ 2.352,06/m²). Fecha a série vintage do engine. TDC/outorga.",
    "lei-municipal-saopaulo-18177-2024": "Lei urbanística municipal (uso/ocupação/potencial) ingerida do portal 2026-07-13. Efeito TDC/urbanístico.",
    # (mais massa normativa TDC — decretos ZEPEC/CONPRESP — entra quando ingerida; ver A-11)
    # --- Jurisprudência de TDC ingerida 2026-07-11 (B-21): efeito dominante é TDC (tombamento ×
    #     potencial construtivo; natureza compensatória; direito de protocolo; base do "solo criado"),
    #     NÃO tributo IPTU — o carimbo default 'iptu' de jurisprudencia/ as excluía da consulta TDC. ---
    "tjsp-ai-2126162-35-2025": "TJSP: CONPRESP × potencial construtivo em tombamento (efeito TDC).",
    "tjsp-ai-2257458-20-2024": "TJSP: TDC como compensação pela limitação de propriedade (tombamento).",
    "tjsp-ai-2324382-13-2024": "TJSP: (im)penhorabilidade do potencial construtivo — finalidade TDC.",
    "tjsp-apciv-0000175-39-2017": "TJSP: vedação do Art. 124 §2º PDE à TDC de imóvel tombado.",
    "tjsp-apciv-0000177-09-2017": "TJSP: tombamento provisório = definitivo; vedação da TDC.",
    "tjsp-apciv-1070175-76-2019": "TJSP: direito de protocolo/ultratividade na declaração de PCT (TDC).",
    "stj-agrg-aresp-179340-sp": "STJ: TDC do art. 35 do Estatuto da Cidade em desapropriação de tombado.",
    "stf-re-387047-sc": "STF: 'solo criado'/outorga onerosa não é tributo (base constitucional do TDC).",
    "stf-re-226942-sc": "STF: parcela do solo criado é compensação, não tributo (base do TDC).",
}
# Todo o resto → iptu (o corpus de leis/ e TODA a jurisprudencia/ foram montados p/ a tese IPTU).

TOKENS_DOMINIO_EM_TEMA = {"iptu", "tdc"}  # a remover de tema[] (domínio saiu do lugar errado)


def classificar(stem: str) -> str:
    if stem in COMPARTILHADO:
        return "compartilhado"
    if stem in TDC:
        return "tdc"
    return "iptu"


def alvos():
    for p in sorted((RAIZ / "leis").rglob("*.json")):
        yield p
    for p in sorted((RAIZ / "jurisprudencia").glob("*.json")):
        yield p


def main(check_only: bool):
    dist = {"tdc": 0, "iptu": 0, "compartilhado": 0}
    faltando, mudados = [], []
    for p in alvos():
        try:
            meta = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"  ERRO {p.name}: JSON inválido ({e}) — pulado", file=sys.stderr)
            faltando.append(p.name)
            continue
        stem = p.stem
        dom = classificar(stem)
        dist[dom] += 1

        # tema[] sem os tokens de domínio (preserva os temas materiais, remove só IPTU/TDC)
        tema_novo = [t for t in (meta.get("tema") or [])
                     if str(t).strip().lower() not in TOKENS_DOMINIO_EM_TEMA]

        precisa = (meta.get("dominio_primario") != dom
                   or meta.get("dominio") != [dom]
                   or tema_novo != (meta.get("tema") or []))
        if check_only:
            if meta.get("dominio_primario") not in VOCAB or meta.get("dominio") != [dom]:
                faltando.append(p.name)
            continue
        if precisa:
            meta["dominio_primario"] = dom
            meta["dominio"] = [dom]
            meta["tema"] = tema_novo
            p.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            mudados.append(p.name)

    if check_only:
        if faltando:
            print(f"carimbar_dominio --check: FALHA — {len(faltando)} sem domínio válido: "
                  f"{', '.join(faltando[:8])}{'…' if len(faltando) > 8 else ''}")
            return 1
        print("carimbar_dominio --check: OK — toda norma/acórdão tem dominio ∈ {tdc,iptu,compartilhado}.")
        return 0

    print(f"carimbar_dominio: distribuição → compartilhado={dist['compartilhado']} "
          f"iptu={dist['iptu']} tdc={dist['tdc']} ({sum(dist.values())} itens).")
    print(f"  carimbados/atualizados: {len(mudados)}")
    print("  COMPARTILHADO (lar único, entra nas consultas dos dois):")
    for k in sorted(COMPARTILHADO):
        print(f"    · {k}")
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))

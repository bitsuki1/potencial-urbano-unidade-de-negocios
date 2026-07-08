# Coletor de Gabaritos TDC — extensão do Diário Oficial (Chrome/Edge)

Extensão que roda **no seu navegador** (sua sessão, seu IP — sem bloqueio anti-robô) e coleta,
do **Diário Oficial da Cidade de São Paulo**, os **Termos de Compromisso (CONPRESP)** e as
**Declarações de Potencial Construtivo (SMUL/DEUSO)** — extraindo **m² transferível, SQL, zona,
processo, declaração** para os gabaritos do TDC (`evals/ground-truth/gabaritos/`).

## Por que uma extensão (e não o robô da VPS)
Decisão do dono (2026-07-08). A extensão vive na **sua** sessão de navegador: passa naturalmente
por qualquer barreira (login/CAPTCHA/anti-robô) porque é uma pessoa navegando. A extração do número
é a mesma qualidade em qualquer lugar — o ganho da extensão é o **acesso**, não a “inteligência”.

## Instalar (1 minuto, sem loja)
1. Chrome/Edge → `chrome://extensions` (ou `edge://extensions`).
2. Ligue o **Modo do desenvolvedor** (canto superior direito).
3. **Carregar sem compactação** → selecione esta pasta (`evals/ground-truth/extensao-doc`).
4. Fixe o ícone “Coletor de Gabaritos TDC” na barra.

## Usar
Alvo: **Diário Oficial da Cidade** → https://diariooficial.prefeitura.sp.gov.br → *Pesquisar matérias*.

**Modo A — varredura de busca (recomendado):**
1. Na busca, filtre por palavra-chave (ex.: `Termo de Compromisso`, ou o nº da Declaração/processo do
   índice `zepec/raw/lista_declaracoes_ZEPEC-BIR_agosto-2025.csv`), órgão **SMC/CONPRESP** ou **SMUL**,
   e o período (a coluna *Data publicação* do índice te dá a data exata).
2. Com a **página de resultados** aberta, clique no ícone → **🔎 Varrer resultados da busca**.
   A extensão abre cada matéria por baixo dos panos, extrai e acumula.

**Modo B — publicação avulsa:** abra a matéria e clique **➕ Extrair esta publicação**.

**Exportar:** **⬇️ Baixar CSV** (ou JSON). Me mande o arquivo (ou solte em
`evals/ground-truth/gabaritos/coletados/`) que eu transformo em gabaritos validados.

**Refinar com IA (opcional):** em *Refinar com IA*, cole uma chave Claude (`x-api-key`, fica só no seu
navegador) e clique **✨ Reprocessar** — a IA relê o texto bruto e corrige/preenche os campos com um
prompt afinado pra TDC. Sem chave, a extração por regex já entrega o essencial.

## O que ela extrai (colunas do CSV)
`termo · declaracao · processo · sql_contribuinte · m2_transferivel · zona · resolucao · matricula · endereco · titulo · url`
+ `texto_bruto`/`trecho` no JSON (contexto p/ conferência humana).

## Arquivos
- `manifest.json` — MV3, restrito aos domínios do Diário Oficial (+ api.anthropic.com só p/ o modo IA).
- `extractor.js` — extração pura (regex), fonte única usada pela página e pela varredura.
- `content.js` — lê a publicação aberta / lista os links de resultados.
- `popup.js` · `popup.html` — botões, varredura por `fetch`, exportação, modo IA.

## Limites honestos
- Os seletores de “lista de resultados” são defensivos (vários padrões); se o layout do DO mudar e a
  varredura não achar links, use o **Modo B** por publicação, ou me avise que eu ajusto os seletores.
- A extração por regex acerta o caso comum; **confira o m²** antes de virar gabarito (o modo IA ajuda).
- Nada sai do seu navegador exceto (a) as páginas do próprio Diário Oficial e (b), SÓ se você ligar a IA,
  o texto enviado à API da Anthropic com a sua chave.

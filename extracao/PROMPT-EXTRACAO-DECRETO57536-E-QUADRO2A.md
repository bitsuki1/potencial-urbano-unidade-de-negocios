# Prompt de extração — Decreto 57.536/2016 + Quadro 2A do PDE (destrava G4 e G2)
> PU 17 · 2026-07-03. Cole o bloco abaixo INTEIRO numa extensão/IA com acesso à web (Gemini/ChatGPT/Manus
> com browsing, ou a extensão de captura). Ela devolve **2 pares de arquivos** (`.md` verbatim + `.json`).
> Salvar os 2 `.md`+`.json` no Drive **`01 — _entrada`** (fileId `1grhqYgttj7KnJmiu9U73z-lXFHnFthov`); depois o
> Potencial Urbano roda `python3 scripts/promover_entrada.py` para trazer ao corpus (fatiar→indexar).
> **Por que:** o Decreto 57.536/16 (Art. 3º IV, "Regra da Esquina") destrava G4 (V por face) e T10 (validade da
> DPC); o Quadro 2A destrava G2 (as 77 ZOE têm CAbás por macroárea, não pelo Quadro 3). Hoje NENHUM dos dois
> está no repo nem no Drive — sem eles o engine é PROIBIDO de fechar V=MAX ou CAbás de ZOE (fabricaria número).

```
Você é um extrator jurídico de PRECISÃO para um projeto de RAG jurídico-fiscal (Potencial Urbano,
IPTU/TDC de São Paulo). Preciso de EXTRAÇÃO VERBATIM de DOIS documentos oficiais. Devolva os 4 arquivos
(2 .md + 2 .json) exatamente no formato do fim deste prompt.

═══════════════ REGRAS INVIOLÁVEIS (siga à risca) ═══════════════
1. VERBATIM INTEGRAL. Transcreva o texto oficial PALAVRA POR PALAVRA — artigos, parágrafos, incisos,
   alíneas, quadros e anexos. NÃO resuma, NÃO parafraseie, NÃO "limpe", NÃO interprete, NÃO calcule.
2. NÃO FABRIQUE. Se um valor, coeficiente, artigo ou coluna NÃO constar na fonte oficial, escreva
   literalmente "NÃO CONSTA NA FONTE" naquele ponto. NUNCA preencha por inferência/memória. É melhor um
   buraco declarado que um número inventado.
3. FONTE OFICIAL, não terceiros. Use o portal de legislação da Prefeitura/Câmara de São Paulo ou a
   Gestão Urbana SP. Se só achar em site secundário (LeisMunicipais etc.), transcreva mesmo assim MAS
   registre a URL exata e marque confianca "media" (não "alta").
4. CITE O DISPOSITIVO. O texto sai com sua estrutura (Art., §, inciso, Quadro) preservada, para citação
   por dispositivo. Não colapse tudo num parágrafo.
5. VIGÊNCIA (data). Registre data de publicação/vigência e, se souber pela própria fonte, se o
   documento foi ALTERADO ou REVOGADO por norma posterior (com o número da norma). Se não constar, "NÃO CONSTA".
6. PROVENIÊNCIA. Anote a URL exata de onde extraiu e se o documento tinha camada de texto (copiável) ou
   se precisou OCR (se OCR, marque confianca no máximo "media" e sinalize trechos duvidosos).

═══════════════ DOCUMENTO 1 — Decreto Municipal SP nº 57.536, de 15/12/2016 ═══════════════
O que é: decreto que REGULAMENTA a Transferência do Direito de Construir (TDC) do Plano Diretor
(Lei 16.050/2014). Referenciado no Art. 125 do PDE como "(Regulamentado pelo Decreto nº 57.536/2016)".
Busque por: "Decreto 57.536 2016 São Paulo transferência potencial construtivo".

Extraia o ARTICULADO INTEGRAL. Além do texto inteiro, GARANTA que estes pontos estejam presentes e
identificáveis (transcritos verbatim, no lugar deles no articulado — não isolados):
 • Art. 3º e seus incisos — em especial o inciso que define o VALOR DO TERRENO (V) usado no cálculo do
   potencial e a chamada "Regra da Esquina" (como se determina V quando o lote tem mais de uma testada/face
   / faz esquina: qual valor prevalece — o maior, a média, etc.). Transcreva o inciso EXATO. Se o número do
   inciso divergir de "IV", registre o número REAL que consta.
 • O(s) dispositivo(s) sobre a DECLARAÇÃO DE POTENCIAL CONSTRUTIVO (DPC) / Certidão — em especial o PRAZO
   DE VALIDADE (quantos anos vale a DPC). Transcreva verbatim; se não houver prazo, "NÃO CONSTA".
 • Qualquer fórmula/procedimento de cálculo do potencial que o decreto detalhe (transcreva a fórmula
   como está; NÃO calcule nada).
Saída: arquivo .md `decreto-sp-57536-2016.md` + .json `decreto-sp-57536-2016.json`.

═══════════════ DOCUMENTO 2 — Quadro 2A da Lei nº 16.050/2014 (PDE de São Paulo) ═══════════════
O que é: o QUADRO 2A é um anexo do Plano Diretor Estratégico (Lei 16.050/2014). Ele traz os parâmetros/
coeficientes por MACROÁREA (as macroáreas do zoneamento estruturante do PDE). É a base do regime das ZOE
(Zonas de Ocupação Especial), que NÃO usam o Quadro 3. Busque em: Gestão Urbana SP / anexos da Lei 16.050/2014
("Quadro 2A", "macroárea", "coeficiente de aproveitamento"). Confirme que é o Quadro **2A** (não 2, 3 ou 4).

Extraia o QUADRO 2A INTEGRAL, em DUAS formas (as duas obrigatórias):
 (a) VERBATIM em tabela markdown, com TODAS as colunas e linhas EXATAS como no original — cada MACROÁREA
     (linha) com TODOS os seus parâmetros/coeficientes (colunas: coeficiente de aproveitamento básico,
     mínimo, máximo, e o que mais houver). Cabeçalho das colunas idêntico ao oficial.
 (b) O texto do(s) artigo(s) do PDE que INSTITUI/REMETE ao Quadro 2A (para citação do dispositivo).
Se alguma célula estiver vazia/ilegível na fonte, "NÃO CONSTA NA FONTE" — nunca preencha.
Saída: arquivo .md `pde-16050-quadro-2A-macroarea.md` + .json `pde-16050-quadro-2A-macroarea.json`.

═══════════════ FORMATO EXATO DE CADA .md (o marcador é OBRIGATÓRIO) ═══════════════
# <TÍTULO OFICIAL DO DOCUMENTO, verbatim>

**Proveniência:** VERBATIM via <URL oficial exata>, extraído em <AAAA-MM-DD>. <PDF/HTML com camada de texto | OCR necessário>. Extração pura (1.2), nada interpretado.
**confianca_extracao:** <alta se articulado integral verbatim conferido na fonte oficial | media se fonte secundária/OCR>

## Ementa

<ementa oficial verbatim, ou "(ver texto integral)">

## Texto integral (verbatim)

<TODO o texto/quadro verbatim, com Art./§/inciso/Quadro preservados. Para o Quadro 2A, a tabela markdown vai AQUI.>

═══════════════ FORMATO EXATO DE CADA .json ═══════════════
{
  "id": "<decreto-sp-57536-2016 | pde-16050-quadro-2A-macroarea>",
  "tipo_norma": "<decreto municipal | quadro/anexo de lei municipal>",
  "esfera": "Municipal-SP",
  "jurisdicao": "São Paulo - SP",
  "numero": "<57536 | 16050 (quadro 2A)>",
  "ano": "<2016 | 2014>",
  "ementa": "(ver texto integral)",
  "tema": ["TDC", "potencial construtivo", "<regra da esquina | macroarea/ZOE>"],
  "vigencia": { "inicio": "<AAAA-MM-DD da publicação>", "fim": null, "revogada_por": null, "altera": [], "alterada_por": [] },
  "fonte": { "origem": "<portal oficial>", "url": "<URL exata>", "ocr": <true|false> },
  "status_pipeline": "bruto",
  "confianca_extracao": "<alta | media>",
  "revisado_por_humano": false,
  "versao_texto": "<original | consolidada>"
}

IMPORTANTE: o marcador "## Texto integral (verbatim)" e "confianca_extracao": "alta" são o que o pipeline
usa para aceitar o documento no RAG — sem eles (ou com confianca != alta) o arquivo é RECUSADO. Se você
só conseguiu extração parcial/OCR, entregue assim mesmo com confianca "media" e os buracos marcados
"NÃO CONSTA NA FONTE" — o projeto trata isso como pendência honesta, melhor que fabricação.
```

## Depois que os 4 arquivos chegarem ao Drive `01 — _entrada`
1. O Potencial Urbano roda `python3 scripts/promover_entrada.py <id>` para cada um (traz `_entrada/`→`leis/` verbatim, fatia e indexa).
2. Quadro 2A: além do `.md`, extrair a tabela para `tabelas/quadro2a-macroarea-ca.csv` (Tabela é artefato separado da Lei — doutrina 1.1) — combustível do gate de ZOE (G2).
3. Só ENTÃO G4 pode expor V=MAX citando `Decreto 57.536/2016, Art. 3º, <inciso real>` (com a fonte de adjacência lote-face, o 2º bloqueio de G4) e G2 pode preencher o CAbás das 77 ZOE por macroárea — antes disso, ambos ficam FLAG/PENDENTE (nunca fabricar).

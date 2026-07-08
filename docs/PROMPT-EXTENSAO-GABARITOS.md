# Prompt para a extensão do Claude no navegador — coletar gabaritos TDC do Diário Oficial

> Uso: abra o Chrome com a extensão do Claude, cole o PROMPT abaixo. Ele navega o Diário Oficial
> da Cidade, acha os documentos de TDC (imóveis tombados / ZEPEC), extrai os campos e **gera um
> arquivo CSV + JSON** para você salvar. Depois é só me mandar o arquivo (ou soltar em
> `evals/ground-truth/gabaritos/coletados/`) que eu viro gabarito validado.
>
> Por que a extensão e não o robô: ela roda na SUA sessão/IP — passa por qualquer bloqueio. A
> leitura do número é a mesma qualidade. Decisão do dono, 2026-07-08.

---

## PROMPT (copie tudo abaixo)

```
Você é um coletor de dados jurídicos. Objetivo: montar uma planilha de referência ("gabaritos")
com casos oficiais de TRANSFERÊNCIA DE POTENCIAL CONSTRUTIVO (TDC) de imóveis tombados em São
Paulo, extraídos do Diário Oficial da Cidade de São Paulo. Trabalhe com cuidado e NÃO invente
nada: só registre o que está literalmente escrito no documento.

CONTEXTO (para você reconhecer o documento certo):
- TDC = o dono de um imóvel tombado pode vender o "potencial construtivo" dele. Os documentos que
  fixam o metro quadrado transferível são:
  (a) DECLARAÇÃO DE POTENCIAL CONSTRUTIVO PASSÍVEL DE TRANSFERÊNCIA — emitida pela SMUL/DEUSO;
  (b) TERMO DE COMPROMISSO — do CONPRESP/Secretaria de Cultura (imóveis tombados a conservar);
  (c) CERTIDÃO de Transferência de Potencial Construtivo.
- O número que interessa é a ÁREA em m² PASSÍVEL DE TRANSFERÊNCIA / potencial construtivo
  transferível (ex.: "717,60 m²"). É o valor OFICIAL do documento.

ONDE BUSCAR:
1. Vá para https://diariooficial.prefeitura.sp.gov.br e abra "Pesquisar matérias".
2. Faça buscas por texto, uma de cada vez, e percorra os resultados:
   - "potencial construtivo passível de transferência"
   - "Declaração de Potencial Construtivo"
   - "Termo de Compromisso" (filtrando órgão: Cultura / CONPRESP)
   - "transferência do direito de construir"
   Se houver filtro de órgão, use SMUL / Licenciamento e SMC / CONPRESP. Período: 2015 até hoje.
3. Para cada resultado que for um dos documentos (a/b/c acima), ABRA a matéria e leia o texto.

O QUE EXTRAIR de cada documento (deixe vazio o que não aparecer; não deduza):
- m2_transferivel      : a área em m² passível de transferência / potencial construtivo transferível
                         (formato como no texto, ex.: 717,60). Se houver vários números em m²,
                         escolha o rotulado como "passível de transferência"/"transferível".
- sql_contribuinte     : o SQL do imóvel (formato 000.000.0000-0).
- endereco             : logradouro e número do imóvel.
- processo             : número do processo administrativo (ex.: 6025.2024/0013449-9).
- declaracao           : número da Declaração de Potencial Construtivo SMUL/DEUSO (ex.: 0539/23).
- termo                : número do Termo de Compromisso CONPRESP (ex.: 006/2026), se houver.
- zona                 : sigla da zona de uso citada (ex.: ZEPEC-BIR, ZC, ZM), se houver.
- area_terreno_m2      : área do terreno / área do lote, se citada (ex.: 299,00).
- coeficiente_ca       : qualquer coeficiente de aproveitamento / CA básico / fator citado no cálculo
                         (ex.: "CA básico 2,0", "Fp 1,2"), copie como está.
- trecho_calculo       : copie a frase/parágrafo que mostra COMO o m² foi calculado, se houver
                         (ex.: "área do terreno x coeficiente..."). É ouro para conferência.
- resolucao            : resolução de tombamento citada, se houver.
- data_publicacao      : data da edição do Diário Oficial onde saiu (dd/mm/aaaa).
- url_fonte            : link da matéria/edição.

REGRAS:
- Só o que está escrito. Se um campo não estiver no documento, deixe vazio — NUNCA preencha por
  suposição. Prefira a Declaração SMUL/DEUSO como fonte do m² (é o número oficial).
- Ignore matérias que não tragam um valor em m² transferível (não são gabarito).
- Elimine duplicatas (mesmo SQL + mesma declaração).
- Meta: junte de 20 a 40 casos, cobrindo variedade de zonas e regiões. Pode paginar os resultados.

SAÍDA (gere DOIS arquivos para eu salvar na minha área de trabalho):
1. "gabaritos-tdc-doc.csv" — cabeçalho exatamente:
   m2_transferivel,sql_contribuinte,endereco,processo,declaracao,termo,zona,area_terreno_m2,coeficiente_ca,trecho_calculo,resolucao,data_publicacao,url_fonte
   uma linha por caso, valores entre aspas.
2. "gabaritos-tdc-doc.json" — lista de objetos com as mesmas chaves.
Ao final, mostre um resumo: quantos casos, e uma tabela com sql, m2_transferivel e zona.
Se algum documento estiver escaneado (imagem, sem texto selecionável), registre a linha com o que
der para ler e marque zona/observação como "verificar (escaneado)".
```

---

## Depois que ele gerar o arquivo
Me manda o `gabaritos-tdc-doc.csv` (ou solta em `evals/ground-truth/gabaritos/coletados/`).
Eu cruzo com nossos 377 cedentes, viro cada linha num gabarito validado e uso pra provar o motor
de preço fim-a-fim (zona idêntica ao GeoSampa + m² ±5%).

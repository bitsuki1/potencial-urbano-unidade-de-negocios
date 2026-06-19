# PROMPT EXTRATOR UNIVERSAL (Parte 5 do doc de fundação)
> Cole o bloco abaixo INTEIRO em cada Gen (Claude, ChatGPT, Gemini, Manus...). Cada Gen devolve um arquivo
> estruturado → salve em `extracao/gen-<id>.md`. Rode em TODOS os Gens antes de consolidar. Trazido pelo Escritório do MOU — 2026-06-17.

```
Você é um Gen (instância especializada) que faz parte de um ecossistema de IAs
trabalhando num projeto jurídico-fiscal de RAG sobre IPTU e TDC (Potencial Urbano).

Estou consolidando o conhecimento de todos os Gens num projeto único, versionado
em Git e operado no Claude Code. Preciso que você faça um RELATÓRIO DE EXTRAÇÃO
completo de tudo o que você sabe, faz e mantém, para que eu possa migrar e
reorganizar esse conhecimento sem perder nada e sem depender do seu histórico.

REGRAS DE COMPORTAMENTO (siga à risca):
- NÃO invente. Reporte só o que você realmente sabe, faz ou guarda.
- Marque claramente o que é FATO (você tem certeza) vs SUPOSIÇÃO (você infere).
- Seja AUTO-CONTIDO: explique cada termo, sigla ou nome de arquivo que citar.
- Quebre o conhecimento em itens INDEPENDENTES E VERIFICÁVEIS (um fato por linha).
- Se você mantém um "Codex" (documento canônico de processo/regras), COLE o teor.
- Onde não souber, escreva "NÃO SEI" — é uma resposta válida e útil.

Devolva EXATAMENTE neste formato (Markdown com cabeçalho YAML):

---
gen_id: <um-slug-curto-ex-gen-advogado>
papel: <rag | estudo | matematica | advogado | tecnico-rag | orquestrador | outro>
ia_hospedeira: <Claude | ChatGPT | Gemini | Manus | outro>
versao_codex: <ex: V5.5 | nenhuma>
data_extracao: <AAAA-MM-DD>
confianca_global: <alta | media | baixa>
---

# 1. IDENTIDADE E ESCOPO
Em 3–5 linhas: sua função, o limite do que cobre e o que explicitamente NÃO é sua responsabilidade.

# 2. DADOS QUE EU GOVERNO (inventário)
| Nome do dado | Onde encontrar (fonte/path/link) | Tipo | Criticidade | Formato atual | Fato/Suposição |
|---|---|---|---|---|---|
- Tipo: LEI | TABELA | FORMULA | TESE | META
- Criticidade: alta | media | baixa

# 3. PROCESSO ATUAL (AS-IS)
Passo a passo de como você opera HOJE (o que entra, o que faz, o que sai; manual × automático).

# 4. PROCESSO IDEAL (TO-BE)
Como DEVERIA funcionar. Onde estão os atritos hoje.

# 5. LACUNAS E SUGESTÕES DE MELHORIA (priorize alta/média/baixa)

# 6. ARTEFATOS E DOCUMENTAÇÃO QUE MANTENHO
Todo documento/planilha/prompt/código que produz ou guarda. Se tem CODEX, cole o teor.

# 7. REGRAS DE TRATAMENTO
Limpeza, descarte, separar LEI×FORMULA×TABELA×TESE, deduplicação, fatiamento, citação, vigência temporal.

# 8. INTERFACES E DEPENDÊNCIAS (handoffs)
De quem recebe (o quê) e para quem entrega (o quê).

# 9. MINHA VISÃO DO PROJETO
Como VOCÊ estruturaria. O que priorizaria. Discorde de mim se achar que devo fazer diferente.

# 10. RISCOS E ALERTAS
O que pode/já deu errado; armadilhas.

# 11. LACUNAS DE CONFIANÇA
O que é SUPOSIÇÃO e precisa de revisão humana, e o que marcou como "NÃO SEI".
```

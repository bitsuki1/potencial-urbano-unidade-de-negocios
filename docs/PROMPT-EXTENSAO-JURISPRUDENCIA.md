# Prompt para a extensão (Manus) — inteiro teor da jurisprudência (E)
> Entregue ao dono em 2026-08-07 (PU 23). Cobre a metade-extensão da task #7 (STJ 3-4 + TJSP 8-10)
> + os 3 TJSP que o runner não alcançou (o teor mora na pasta digital). Colar o texto abaixo na extensão.

---

Você é meu assistente de captura de documentos judiciais PÚBLICOS (decisões judiciais são domínio público — Lei 9.610/98, art. 8º, IV). Sua missão: baixar o INTEIRO TEOR (PDF oficial completo) de 8 processos, um a um, e me entregar os arquivos nomeados EXATAMENTE como indico. Não resuma, não interprete, não edite: só baixe o documento oficial.

**LOTE 1 — STJ (scon.stj.jus.br):**
1. Acesse https://scon.stj.jus.br/SCON/ e pesquise por: `AgRg no AREsp 179340`. Abra o acórdão (AgRg no AREsp 179.340/SP, 2ª Turma), clique em "Inteiro Teor" e baixe o PDF. Nome do arquivo: `stj-agrg-aresp-179340-sp.pdf`
2. Na mesma pesquisa, busque: `REsp 1130545`. Abra o acórdão do REsp 1.130.545 (repetitivo, Rel. Min. Luiz Fux), baixe o PDF do inteiro teor. Nome: `stj-resp-1130545.pdf`

**LOTE 2 — TJSP, Apelações (esaj.tjsp.jus.br — consulta de julgados CJSG ou pasta digital do cposg):**
Para cada processo: acesse https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do, pesquise pelo número no campo "Número do processo" e baixe o PDF do ACÓRDÃO. Se a CJSG não achar, use https://esaj.tjsp.jus.br/cposg/open.do, pesquise o número, abra o processo e use "Pasta digital" → localize o documento "Acórdão" e baixe o PDF.
3. `0000175-39.2017.8.26.0053` → nome: `tjsp-apciv-0000175-39-2017.pdf`
4. `0000177-09.2017.8.26.0053` → nome: `tjsp-apciv-0000177-09-2017.pdf`
5. `1070175-76.2019.8.26.0053` → nome: `tjsp-apciv-1070175-76-2019.pdf`

**LOTE 3 — TJSP, Agravos de Instrumento (pasta digital do cposg — o acórdão/decisão não sai pela consulta pública simples):**
Mesmo procedimento do Lote 2, priorizando a "Pasta digital"; baixe a DECISÃO/ACÓRDÃO mais recente de mérito:
6. `2126162-35.2025.8.26.0000` → nome: `tjsp-ai-2126162-35-2025.pdf`
7. `2257458-20.2024.8.26.0000` → nome: `tjsp-ai-2257458-20-2024.pdf`
8. `2324382-13.2024.8.26.0000` → nome: `tjsp-ai-2324382-13-2024.pdf`

**REGRAS:**
- Só fonte OFICIAL (scon.stj.jus.br e esaj.tjsp.jus.br). NUNCA baixe de JusBrasil, Escavador ou espelhos.
- Se um documento exigir login/senha do processo, PULE e me diga qual foi e por quê.
- Ao final, me entregue os PDFs com os nomes exatos acima e uma lista do que conseguiu e do que não conseguiu.

---
> **Destino dos PDFs (dono):** jogar na pasta `_entrada/` do Drive do PU (ou me mandar) — a instância
> extrai (OCR se preciso), grava no corpus com `ocr`/hash e reindexa, como fez com os 2 do STF.

---
## v2 (2026-08-07, tarde) — SÓ OS 5 FALTANTES, SEM PASTA DIGITAL (nada de senha)
> Rodada 1 da extensão entregou 3/8 (AgRg AREsp 179.340 ✓, REsp 1.130.545 ✓, ApCiv 0000175 ✓ — já no corpus).
> Lição: a "pasta digital" do cposg pede senha do processo (Res. 121/CNJ) — mas o ACÓRDÃO sai SEM senha
> pela Consulta de Julgados (CJSG), que é pública. O prompt abaixo proíbe a rota errada.

Você é meu assistente de captura de documentos judiciais PÚBLICOS. Baixe o INTEIRO TEOR (PDF) de 5 julgados do TJSP. REGRA DE OURO: use SOMENTE a consulta pública de jurisprudência — NUNCA abra a "Pasta Digital" nem qualquer tela que peça senha do processo ou login; se uma tela pedir senha, volte e use a rota pública.

ROTA ÚNICA — Consulta de Julgados do TJSP (pública, sem login):
1. Acesse https://esaj.tjsp.jus.br/cjsg/consultaCompleta.do
2. No campo "Número do processo" (aba de pesquisa), digite o número abaixo.
3. Em "Tipo de decisão", marque AMBOS: "Acórdãos" E "Decisões Monocráticas" (os agravos podem ter sido decididos por decisão monocrática).
4. Pesquise (resolva o captcha visual se aparecer — é permitido, é público).
5. No resultado, clique no ícone/link do PDF do julgado (abre direto, sem senha) e salve com o nome indicado.
6. Se a pesquisa não retornar nada, tente o mesmo número em https://esaj.tjsp.jus.br/cjpg/ (julgados de 1º grau) e anote o que apareceu.

Os 5 processos:
1. `0000177-09.2017.8.26.0053` → salvar como `tjsp-apciv-0000177-09-2017.pdf`
2. `1070175-76.2019.8.26.0053` → salvar como `tjsp-apciv-1070175-76-2019.pdf`
3. `2126162-35.2025.8.26.0000` → salvar como `tjsp-ai-2126162-35-2025.pdf`
4. `2257458-20.2024.8.26.0000` → salvar como `tjsp-ai-2257458-20-2024.pdf`
5. `2324382-13.2024.8.26.0000` → salvar como `tjsp-ai-2324382-13-2024.pdf`

Ao final: entregue os PDFs com os nomes exatos + uma lista do que conseguiu e, para o que não conseguiu, uma captura de tela da página de resultado (sem dados pessoais seus).

---
## v3 (2026-08-07, noite) — resposta às limitações da rodada 2 (o link é javascript, não âncora)
> Rodada 2 entregou o ED do 1070175 (ingerido). Dúvida da extensão respondida: os números CONFEREM
> (validados no cposg com câmara/relator). O "Visualizar Inteiro Teor" da CJSG é javascript que
> chama getArquivo.do — o PDF existe e é público, só não é um link direto.

Os números de processo estão corretos e confirmados. O link "Visualizar Inteiro Teor" da consulta de julgados NÃO é um link comum — é javascript. O PDF é público e sai assim:

1. Na página de resultados da CJSG, clique com o BOTÃO DIREITO sobre o link "Visualizar Inteiro Teor" (ou sobre o título do julgado) → "Inspecionar". No código, procure `getArquivo(NÚMERO)` ou `cdAcordao=NÚMERO` — anote o NÚMERO.
2. Abra em nova aba: `https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=NÚMERO&cdForo=0` — o PDF do acórdão abre direto, sem senha. Salve com o nome combinado.
3. `1070175-76.2019.8.26.0053`: dos 2 resultados, baixe o da **Apelação Cível** (o dos Embargos de Declaração eu já tenho). Nome: `tjsp-apciv-1070175-76-2019.pdf`
4. `0000177-09.2017.8.26.0053`: tente a "Pesquisa Livre" com `0000177-09.2017` (sem o sufixo) e também com a parte `Fundação Armando Álvares Penteado`. Se nada aparecer, me diga — declaro o caso como "sem acórdão indexado na consulta pública".
5. Agravos `2126162-35.2025`, `2257458-20.2024`, `2324382-13.2024`: na CJSG, marque "Decisões Monocráticas" além de "Acórdãos". Se não vier nada, use o **Diário da Justiça Eletrônico** (público, sem login): https://dje.tjsp.jus.br/cdje/consultaAvancada.do — pesquise pelo número do processo, abra o caderno do dia da decisão e salve o PDF da(s) página(s). Nomes: `tjsp-ai-<numero>.pdf` (ou `-dje.pdf` se vier do Diário).

---
## v4 (2026-08-07, noite) — SÓ FALTAM OS ACÓRDÃOS PRINCIPAIS: 5 links diretos p/ o navegador do dono
> Rodada 3 entregou 5 PDFs (ingeridos): a APELAÇÃO do 1070175 ✓ e os EMBARGOS DE DECLARAÇÃO dos
> outros 4 processos. O relatório da extensão trouxe os `cdAcordao` de TODOS os resultados — os que
> baixamos eram a "primeira opção"; a "segunda opção" de cada processo é o acórdão PRINCIPAL que falta.
> Não precisa de extensão: basta o dono abrir os links abaixo no navegador dele (logado no e-SAJ como
> estava) e salvar o PDF. Se algum link abrir o documento errado, me avise qual.

| Processo | O que falta | Link direto (abrir e salvar) | Salvar como |
|---|---|---|---|
| 0000177-09.2017.8.26.0053 | Acórdão da Apelação | https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=10898038&cdForo=0 | `tjsp-apciv-0000177-09-2017.pdf` |
| 2126162-35.2025.8.26.0000 | Acórdão do Agravo | https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=19642789&cdForo=0 | `tjsp-ai-2126162-35-2025.pdf` |
| 2126162-35.2025.8.26.0000 | (alternativa, se o de cima vier errado) | https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=19642788&cdForo=0 | `tjsp-ai-2126162-35-2025-b.pdf` |
| 2257458-20.2024.8.26.0000 | Acórdão do Agravo | https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=18543735&cdForo=0 | `tjsp-ai-2257458-20-2024.pdf` |
| 2324382-13.2024.8.26.0000 | Acórdão do Agravo | https://esaj.tjsp.jus.br/cjsg/getArquivo.do?cdAcordao=18704310&cdForo=0 | `tjsp-ai-2324382-13-2024.pdf` |

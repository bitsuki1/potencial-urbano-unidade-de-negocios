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

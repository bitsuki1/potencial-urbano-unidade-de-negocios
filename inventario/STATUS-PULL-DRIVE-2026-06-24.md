# STATUS — Pull do Drive (corpus-texto + pesados + apagar) · 2026-06-24
> Orquestrador PU. Estado HONESTO (D83: "declarei feito" ≠ "provei feito"). Trabalho PARCIAL — ver "Pendente".

## O que ENTROU no repo (verbatim, provado)
- **30 arquivos novos** de corpus-texto em `_entrada/{tdc,iptu,misto}/`, cada um com cabeçalho de proveniência (fileId + conta + data).
- Destaques de produto (TDC): **Lei 16.402/2016 (LPUOS) íntegra** (278 KB), **Certidão de Transferência de Potencial Construtivo (SMUL)**, **14 normas infralegais** SMUL/CEUSO/CTLU/CONPRESP (resoluções, portarias, IN, pronunciamento) — o tier infralegal do TDC, antes inexistente.
- Decretos municipais, APTs/tombamentos (ZEPEC-APC), quadros do PDE2013, doutrina IPTU.

## BUG corrigido (D24/RO-09 — nada se descarta em silêncio)
O `.gitignore` tinha `*secret*` (mira credencial) que casava **"Secretaria"** → 14 normas infralegais reais estavam sendo **silenciosamente ignoradas pelo git**. Regra reancorada a arquivo de credencial (`*secret*.json`, `*.secret`, `*.key`, `*.pem`). As 14 foram recuperadas e commitadas.

## PARCIAL / PENDENTE (não declarar feito)
- **Extração incompleta:** os 8 sub-agentes de lote bateram no **limite de sessão (reset 09:40 UTC)** antes de terminar. Dos **378** docs-texto planejados, ~**30** entraram nesta leva. Os `RELATORIO-lote-*.json` **não foram gravados** → a **lista consolidada de OCR-needed ainda NÃO existe**.
- **Resume (quando a sessão renovar):** re-rodar os lotes a partir de `inventario/lotes-pull/lote-{1..8}.json` (worklist já no git). Cada agente grava só texto-válido e lista o que é PDF-imagem → OCR.
- **OCR:** o acervo tem cópias múltiplas; muitas são **PDF-imagem/capa-de-catálogo** (sem texto). Essas exigem OCR antes de virar verbatim (D-PU-OCR) — não entram como estão.

## PRÓXIMOS PASSOS (ordem)
1. **Após reset:** re-rodar os 8 lotes → completar o corpus-texto + gerar a lista OCR consolidada.
2. **Promover ao RAG:** rodar `scripts/promover_entrada.py` nas leis verbatim de `_entrada/` → `leis/` → `fatiar`+`indexar`. Os 3 evals `tdc-produto-pendente.json` viram o gate de aceite (destrava H0).
3. **Pesados → Supabase Storage:** rodar `scripts/transferir-pesados-drive-supabase.md` (rclone, fora do chat). Manifesto: `inventario/PESADOS-PARA-SUPABASE.csv` (351 arquivos).
4. **Apagar duplicatas no Drive:** completar os IDs truncados e rodar o `Sanear-Duplicatas-*.gs`. Lista: `drive-arrumacao/LISTA-APAGAR-script.csv`.

## Artefatos desta leva
- `inventario/PULL-MANIFEST-corpus-texto.json` (388 docs-texto + 10 núcleo) · `inventario/lotes-pull/` (worklists)
- `inventario/PESADOS-PARA-SUPABASE.csv` + `scripts/transferir-pesados-drive-supabase.md`
- `drive-arrumacao/LISTA-APAGAR-script.csv`

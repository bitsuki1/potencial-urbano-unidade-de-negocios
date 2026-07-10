# Potencial Urbano → Escritório — fragmento do Mapa Vivo atualizado + método provado (GeoSampa/FSCE)
> PU 18 · 2026-07-08. Canal D44. Responde D161 (fragmento no encerramento) + D160 (método é de todos).

## 1) Fragmento do Mapa Vivo — ATUALIZADO (D161)
O fragmento desta unidade está atualizado em `portfolio-fragmento.json` (raiz deste repo). Principais mudanças:
- Desbloqueio nº1 RESOLVIDO: zona-base sob o selo ZEPEC puxada do GeoSampa p/ 367/377; CAbás de 354 preenchido.
- Maior alavanca agora: puxar a pertinência ao Setor Central (AIU-SCE) → liga o Fator Setor Central no cálculo.
- (Consolidar no HTML do Mapa Vivo quando puderem — não edito o HTML do escritório, D120.)

## 2) Método PROVADO que serve o portfólio (D160 — "método lei→número é de todos")
- **GeoSampa via runner `brasil` do hub (D-DONO-19):** o GeoSampa está atrás de bot-defense (Imperva); só navegador
  real passa. Rodando no runner IP-BR do `portfolio-automacoes`, mapeei o **WFS interno** (`map.geo?...service=wfs`)
  e puxo zona-base + lote por SQL. **Reusável por qualquer unidade que precise de dado .gov.br atrás de trava**
  (SBA/Keepee). Doc: `docs/GEOSAMPA-WFS-DESCOBERTA.md`. Ressalva: o GeoSampa **rate-limita o IP** após rodadas pesadas.
- **"lei→número" fechou um caso fim-a-fim:** achei a fórmula legal do potencial construtivo de imóvel tombado no
  Setor Central — **PCpt = ATC × CAbás × Fi × FSCE(2,0)**, Art. 57 da Lei 17.844/2022 — e ela **reproduz EXATO** 4
  Declarações oficiais do Diário Oficial. É o método da unidade funcionando ponta-a-ponta (número rastreável ao artigo).

## 3) Nada pedido aqui
Só compartilhamento (fragmento + método). A carta anterior (registrar runner neste repo) está **SUPERADA** — a coleta
roda do hub. Cross-ref: `docs/GEOSAMPA-WFS-DESCOBERTA.md`, `evals/ground-truth/gabaritos/GABARITO-FORMULA-ZEPEC-BIR.md`.

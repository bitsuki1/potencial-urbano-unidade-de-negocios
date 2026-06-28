# ZEPEC — verificação e estudo (itens 2–8 da limpeza)
> PU 14 · 2026-06-28. Sobre `zepec/limpo/zepec_unificada.csv` (7.175 linhas). Agnóstico: só fato.
> Disposição do MOU por item: 1 ok · 2 verificar · 3 estudar · 4 idem · 5 normalizar+padrão · 6 verificar · 7 idem · 8 também.

## FEITO (1, 5, 8)
- **(1) Casing:** logradouro/nome/distrito em Title Case PT (conectores `de/da/do/e` minúsculos; acentos preservados). Ex.: `BAIRRO DA BELA VISTA → Bairro da Bela Vista`.
- **(5) Datas → ISO + padrão estabelecido:** saída `data_pub_iso` em `AAAA-MM-DD`.
  - **Padrão:** série do Excel (inteiro) convertida (dias desde 1899-12-30); texto `DD/MM/YYYY` com heurística US/BR — campo >12 desambigua; ambos ≤12 ⇒ assume **BR (D/M)** e marca `data_amb=ambiguo`.
  - Resultado: **5.084 ok · 1.723 ambíguo (marcado) · 367 sem data · 1 só-ano**. Conferido: `36789 → 2000-09-20` (= "9/20/2000" do cru).
- **(8) Categoria AUE/APPa marcada como FATO:** colunas `categoria` + `cessao_vedada_art124p2` (sim p/ Área de Urbanização Especial e Áreas de Proteção Paisagística — vedação do **Art. 124 §2º PDE**, fato legal, não juízo). **56 linhas** marcadas.

## VERIFICADO (2, 6, 7)
- **(2) 48 SQL inválidos** — 3 declarações · 5 certidões · 40 tombados. Causas: SQ **não-numérico na fonte** (`COND 02`, `Vila Inglesa`), SQ **7 dígitos** (`0001063`), **quadra 2-díg / lote ausente** (tombados). **Não auto-corrigidos**: recuperar o lote exige cadastro/conferência (externo ou manual). Ficam com `sql_status=invalido` (rastreáveis pelo filtro).
- **(6) Duplicata / 2ª via / vínculo** — `4.292` SQL_MESTRE distintos; **589 com >1 ocorrência**; **31 declarações "2ª via"**; **49 imóveis aparecem em declaração E certidão-cedente**. Isto é o **ciclo declaração→certidão** (Art. 131), não lixo. → mantido como ⏳ **A OBSERVAR**; dedup precisa de regra (mesmo SQL + origem diferente ≠ duplicata) — não fizemos.
- **(7) OCR/encoding** — **baixíssimo**. Os "suspeitos" do `Ó` são quase todos **legítimos** ("Freguesia do Ó", "Nossa Senhora do Ó"). Único candidato real: APC **"Bar Ó do Borogodó"** (provável "Bar do Borogodó"). → 1 item para conferência manual; resto OK.

## ESTUDO — decisão sua (3, 4)
- **(3) Endereço multi (`end_multi=1`: 1.098 após remover falsos "s/nº").** Três padrões: (a) vários nºs na mesma rua (`624 e 628`); (b) **lote de esquina / conjunto** com frentes em ruas diferentes (`R X, 10 / Av Y, 20`); (c) conjunto de vários imóveis.
  - **Recomendação (para você decidir):** grão = **1 linha por SQL_MESTRE** (a unidade cadastral). Endereço multi de um mesmo SQL = atributo do mesmo imóvel (esquina) → **não explodir o endereço**. Só explodimos **lote** (já feito), não endereço. Confirma?
- **(4) 21 endereços sem tipo** (após reconhecer EST/PR/JD). Restantes são **nomes sem tipo na própria fonte** (`Normandia, 12` · `Vila Suíça, 2A`). Opções: (i) manter o logradouro como veio (fato); (ii) inferir tipo por geocodificação (externo). **Recomendo (i)** por ora.

## Estado das colunas A OBSERVAR (intocadas, como pedido)
`potencial/área` (formato misto US/BR) · `vínculo declaração↔certidão` (49) · `saldo/ESGOTADO` — carregadas cruas, não resolvidas.

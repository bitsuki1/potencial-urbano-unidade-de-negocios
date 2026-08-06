# ESTUDO — Qual "valor do m²" o produto deve expor: venal do IPTU (PGV) × VTcd do Quadro 14?
> Unidade Potencial Urbano · instância de estudo (5 lentes) · 2026-08-06 · somente-leitura (nenhum arquivo ou banco alterado)
> Pedido do dono (2026-08-06): "estude sob várias lentes e me traga o resultado com sugestões" (item ③a da auditoria PU 20).
> Fontes: `engines/tdc/art128.py` · `leis/municipal-sp/lei-municipal-saopaulo-16050-2014.md` (Art. 128, linhas 4978–5028) · `zepec/oficial/q14_cedentes_2026_oficial.csv` · `CODEX-PRECIFICACAO-TDC.md` · `CODEX-CALCULOS-TDC.md` · Supabase `csnalylpvysjvejgsymr`, schema `motor4` (consultas SELECT desta sessão)

## Resumo executivo
1. A view `motor4.cedentes` expõe hoje `c.valor_m2_terreno AS valor_m2` — que é o **venal de terreno do IPTU 2026**, um artefato que **não aparece na fórmula do Art. 128**; a lei manda usar o **VTcd do Cadastro de Valor de Terreno para fins de Outorga Onerosa (Quadro 14)**.
2. Medição fresca no banco: os dois valores divergem em quase todos os cedentes — razão VTcd/venal com **mediana 0,754**, faixa **0,260–2,763**; só **7,9%** dos casos ficam dentro de ±5%. São artefatos diferentes, confirmado.
3. O VTcd oficial **já está no banco** (`motor4.c_q14_cedentes_2026_oficial`, 3.678 faces) e o join por SQ+codlog cobre **3.878 dos 3.905 cedentes (99,31%)**; ficam **27 órfãos** (0,69%), 24 deles numa única face de quadra ausente do Q14.
4. O "preço legal" rastreável já existe como engine (`art128.py`: numerador PCpt×VTcd e referência ÷4, Art. 128 caput+§1º) — o risco atual é de **rótulo**: um campo genérico `valor_m2` na camada de produto convida a usar o número errado como se fosse o preço TDC.
5. A decisão é do dono; este estudo fecha 3 opções (A/B/C) com prós/contras e recomendação ao final.

---

## 1 · Lente jurídica — o que o Art. 128 manda usar

**Fórmula legal (verbatim):** *"PCr = (PCpt x VTcd) / (Cr x CAmaxcd)"* — **Lei Municipal SP nº 16.050/2014 (PDE), Art. 128, caput** (redação vigente; fonte: `leis/municipal-sp/lei-municipal-saopaulo-16050-2014.md`, linhas 4978–4984).

**Definição legal do VTcd (verbatim):** *"VTcd – valor unitário, valor por 1m2 (um metro quadrado), do terreno cedente ou doado **de acordo com o Cadastro de Valor de Terreno para fins de Outorga Onerosa** vigente na data de referência ou doação, conforme consta da declaração expedida pela Secretaria Municipal de Desenvolvimento Urbano"* — **Art. 128, caput** (linhas 4992–4996). Esse Cadastro é o **Quadro 14 do PDE**.

**Complementos:**
- **§1º** — origem no Art. 125 (sem doação — o universo ZEPEC do produto): **CAmaxcd = 4 fixo** (linhas 5012–5016).
- **§2º** — o VTcd é **corrigido pelo IPCA** entre o mês seguinte à referência da Declaração e o mês anterior ao protocolo da Certidão (linhas 5018–5028).

**Papel do venal da PGV na fórmula: NENHUM.** O texto do Art. 128 cita exclusivamente o Cadastro para fins de Outorga Onerosa (Quadro 14). O valor venal de terreno do cadastro do IPTU (PGV) não é mencionado em nenhum dispositivo do Art. 128 — nem no caput, nem nos parágrafos. Conclusão jurídica: **usar o venal como valor do cálculo TDC não tem amparo no dispositivo**; qualquer número apresentado como "preço legal" que parta do venal é, por definição, não-fundamentado (princípio 1.7).

O engine `art128.py` já implementa exatamente isso: recebe VTcd do Quadro 14 (com o reajuste anual acumulado — fator 2026 = 1,25953…, Dec. 64.884/2025, validado contra a Portaria SMUL nº 19/2024 no auto-teste), aplica §1º (CAmaxcd=4) e §2º (IPCA), e devolve memorial com citação linha a linha.

## 2 · Lente de dados/engenharia — o que cada campo é e o que o join cobre

**O que existe no schema `motor4`** (verificado via `information_schema` nesta sessão):

| Objeto | Conteúdo | Linhas |
|---|---|---|
| `c_iptu2026_cedentes` | cadastro IPTU 2026 por cedente (`sql_mestre`, `codlog`, `valor_m2_terreno`, área, uso, padrão…) | **3.905** |
| `c_q14_cedentes_2026_oficial` | Quadro 14 vigente 2026 por face (`sq`, `codlog`, `valor_m2_brl`) — espelha `zepec/oficial/q14_cedentes_2026_oficial.csv` (3.678 linhas de dados; 1.781 codlogs distintos) | **3.678** |
| `cedentes` (VIEW) | `c_iptu2026_cedentes` LEFT JOIN `c_zona_por_cedente`; expõe **`c.valor_m2_terreno AS valor_m2`** | 3.905 |

- **`valor_m2` da view = venal IPTU**: cobertura 100% (3.905/3.905 preenchidos, zero vazios). É dado da PGV — serve a triagem, contexto e sanidade, **não** ao cálculo do Art. 128.
- **VTcd Q14**: join `left(sql_mestre,6) = sq AND replace(codlog,'-','') = codlog` recupera **3.878/3.905 (99,31%)**, **sem fan-out** (a contagem permanece 3.905 — nenhum cedente duplica).
- **Órfãos: 27 (0,69%)**, com padrão claro:
  - **24** estão na **mesma quadra SQ 001023, codlog 325481** — a quadra existe no Q14, mas essa face não;
  - 1 caso (`0060250022`) tem SQ e codlog existentes no Q14 separadamente, mas não combinados (face divergente entre cadastros);
  - 1 caso (`0904790108`) com SQ ausente do Q14; 1 caso residual (`1230010010`) com face ausente.
  - Caminho técnico possível para parte deles (a validar juridicamente e sob gate): a regra do maior valor da quadra do **Decreto 57.536/2016, Art. 3º, IV** — já referenciada no engine (`DEC_ESQUINA`) — ou fallback explícito `NULL + motivo`, nunca silencioso.
- **Divergência medida (razão VTcd Q14-2026 ÷ venal IPTU-2026, n=3.878):** mín **0,260** · p25 **0,647** · mediana **0,754** · p75 **0,880** · máx **2,763**; apenas **308 (7,9%)** dentro de ±5%. *(A auditoria anterior citou 0,62–1,76; a medição fresca sobre o join completo dá faixa ainda mais ampla — reforça, não contradiz: são artefatos distintos, não intercambiáveis.)*
- Nota de higiene: existem dois CSVs irmãos no repo (`q14_cedentes_2026.csv` e `q14_cedentes_2026_oficial.csv`) com diferenças de centavos (ex.: 3021,62 × 3021,61). A tabela do banco espelha o `_oficial`. Vale registrar qual é o SSOT para não reabrir a ambiguidade em outra camada.

## 3 · Lente de produto — o que o validador v1 deve exibir como "preço legal"

Pelos princípios 1.1/1.3 (número nasce no engine, rastreável ao dispositivo) e pela doutrina da unidade (CODEX-PRECIFICACAO: o preço legal entra no produto pela coluna `preco_legal_ref_brl`, saída do `art128.py`):

- O "preço legal" exibido deve ser a **saída do engine** — `referencia_brl = (PCpt × VTcd) ÷ 4` (Art. 128 caput + §1º) e, quando o dono quiser o bruto, `numerador_brl = PCpt × VTcd` (decisão do dono 2026-07-10: "mostrar os dois") — **sempre com VTcd do Quadro 14 vigente** e com o memorial/citação que o engine já devolve.
- Um campo de view chamado `valor_m2`, sem sobrenome, **não é rastreável**: quem consome não sabe se é PGV ou Q14, e a mediana 0,754 mostra que a troca **subestimaria ou superestimaria** o valor em ~25% no caso típico (e até ~4× nos extremos).
- O venal do IPTU **pode e deve continuar existindo** na camada de produto — ele é útil (contexto patrimonial, triagem, banda de sanidade) — desde que **rotulado pelo que é** (`valor_m2_venal_iptu2026` ou similar), nunca como "o valor" genérico.
- Para os 27 órfãos de VTcd: o validador deve exibir **"sem VTcd Q14 — pendência"** (fail-closed, como o engine já faz com entrada ambígua), jamais silenciosamente cair no venal.

## 4 · Lente de risco — se o produto expõe o venal como se fosse o preço TDC

- **Erro material na comunicação ao cliente:** no caso mediano, o valor apresentado divergiria ~25% do que a lei assegura (mediana da razão 0,754); nos extremos, de −74% a +176%. Cliente vendedor pode aceitar menos do que o piso legal ou criar expectativa impossível — dano em ambas as direções.
- **Quebra da promessa central do produto:** a proposta de valor da unidade é "número rastreável ao artigo" (1.3/1.7 e DE-52: preço LEGAL = saída de engine, rastreável). Um preço construído sobre o venal **não resiste a uma checagem** contra o Art. 128 — e o produto é vendido exatamente para quem faz essa checagem (advogados, proprietários assessorados).
- **Contaminação em cascata (1.8):** se a view "batiza" o venal de `valor_m2` e alguém o alimenta no engine como se fosse VTcd, o erro se propaga com aparência de rigor — memorial citando o Art. 128 sobre insumo errado é o pior cenário: citação certa, número errado.
- **Retrabalho:** cada dossiê/lista emitido com a base errada teria de ser reemitido e re-comunicado; o custo de renomear uma coluna hoje é trivial perto do custo reputacional de corrigir um parecer entregue.
- **Risco residual mesmo sem erro de cálculo:** enquanto o rótulo genérico existir, todo novo consumidor da view (dashboard, Lovable, planilha) recomeça a ambiguidade. O risco não é um bug pontual; é uma **bomba semântica** armada no schema.

## 5 · Lente comercial — doutrina D-DONO-7/15

- Doutrina em vigor (CLAUDE.md/DE-52 + `art128.py`): **preço legal é dado técnico de engine, não alavanca comercial; a margem é do usuário**. Consequência direta: o produto **não precisa** — e não deve — escolher o número "mais bonito"; deve entregar o número **defensável**, e o defensável é o do Quadro 14 via Art. 128.
- O VTcd via engine é justamente o argumento de venda honesto: "este é o valor de referência que a própria lei lhe assegura, artigo por artigo" (incl. a tese OP-1b do MAX piso/teto já implementada em `referencia_max_art128`). O venal, se exposto como preço, viraria alavanca comercial disfarçada de dado — exatamente o que o reparo do PU à DE-53 vetou ("preço é dado de engine, NÃO alavanca comercial").
- O venal mantém papel comercial legítimo **como contexto**: mostrar ao proprietário "seu terreno vale X no cadastro do IPTU e o potencial construtivo tem referência legal Y" é narrativa poderosa — mas só funciona se os dois números estiverem **separados e nomeados**. Misturá-los destrói a narrativa dos dois.

---

## SUGESTÕES AO DONO
> A decisão é sua (D21/D157). Três opções fechadas; nenhuma exige coleta de dado novo — o VTcd oficial já está no banco.

### Opção A — A view passa a expor o VTcd/engine como o campo de preço; o venal vira coluna separada claramente rotulada
`motor4.cedentes` ganha `vtcd_q14_2026_m2` (join com `c_q14_cedentes_2026_oficial`, a chave testada acima) e o atual `valor_m2` é **renomeado** para `valor_m2_venal_iptu2026`; o campo genérico `valor_m2` deixa de existir. O `preco_legal_ref_brl` continua nascendo só no engine.
- **Prós:** mata a ambiguidade na raiz (no schema, não na doc); qualquer consumidor futuro herda os nomes certos; alinha a camada de produto ao Art. 128 com custo de uma migração de view.
- **Contras:** quebra o contrato da view — consumidores existentes que leem `valor_m2` precisam ser inventariados e ajustados na mesma janela; os 27 órfãos aparecem como `NULL` no VTcd (precisa de regra explícita de exibição "pendência").

### Opção B — Duas colunas com nomes inequívocos, sem eleger "o" campo de preço na view
Igual à A no join e nos nomes (`valor_m2_venal_iptu2026` + `vtcd_q14_2026_m2`), mas a view **não designa** nenhum campo como preço: o "preço legal" só existe nas saídas do engine (`numerador_brl`/`referencia_brl` com memorial), que o validador v1 consome. A view é insumo; o preço é sempre computado, citado e carimbado.
- **Prós:** máxima fidelidade aos princípios 1.1/1.3 (view = dado, engine = número); impossível confundir insumo com resultado; mesma correção de rótulos da A.
- **Contras:** mesmos custos de migração da A; exige que o validador v1 chame (ou pré-materialize) a saída do engine em vez de ler um campo pronto — um passo a mais de plumbing.

### Opção C — View intocada; o desvio é tratado só na camada do validador/dossiê
`motor4.cedentes` permanece como está e o validador v1 ignora `valor_m2`, buscando o VTcd direto de `c_q14_cedentes_2026_oficial` + engine.
- **Prós:** zero migração, zero risco de quebrar consumidores hoje; entrega o preço certo no v1 do mesmo jeito.
- **Contras:** a bomba semântica continua armada — `valor_m2` genérico segue disponível para o próximo dashboard/integração usar errado; a correção vive em convenção (doutrina), não em schema; contradiz o espírito de 1.7 na superfície de dados.

### Recomendação (não-decisão)
**Recomendo a Opção B**, com a A como segunda escolha. Fundamento: (i) juridicamente só o VTcd do Quadro 14 sustenta o Art. 128 (caput, verbatim acima) — então o preço deve nascer **sempre** do engine, nunca de um campo de view, e a B é a única que torna isso estrutural; (ii) o join já cobre 99,31% sem fan-out, então o custo de dado é só a política para 27 órfãos (sugiro `NULL` + rótulo "pendência", e estudar a regra do maior valor da quadra — Dec. 57.536/2016, Art. 3º, IV — como destravamento futuro, sob gate do dono); (iii) a C deixa o risco reputacional armado por economia pequena. A escolha do COMO (janela de migração, nomes finais das colunas, tratamento dos órfãos) é do dono.

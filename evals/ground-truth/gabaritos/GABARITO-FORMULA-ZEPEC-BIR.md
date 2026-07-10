# A fórmula do PCpt para ZEPEC-BIR no Setor Central: **CAbás × Fi × FSCE(2,0)** — Art. 57, Lei 17.844/2022

> 2026-07-08. Âncora LEGAL encontrada no corpus (o dono apontou: a resposta estava nos documentos do Drive,
> que citam a Lei 17.844). Provado contra **4 Declarações oficiais** do Diário Oficial. Corrige a hipótese
> anterior "CAmax" (era coincidência: CAmax do ZC = 2 = FSCE).

## O dispositivo (verbatim, `leis/municipal-sp/lei-municipal-saopaulo-17844-2022.md`, Art. 57)
"Para os imóveis classificados como **ZEPEC-BIR** com área de terreno de até **1.000 m²**, localizados na
**AIU-SCE** e no âmbito de seus perímetros expandidos, será aplicado ao cálculo do PCpt ... o **fator setor
central – FSCE de 2,0**, segundo a equação:
**PCpt = ATC × CAbás × Fi × FSCE**", onde ATC = área do terreno; CAbás = coef. básico (data de referência);
Fi = Fator de Incentivo (Art. 24 §1º da Lei 16.402/2016, escalonado por área); **FSCE = 2,0**.

## A prova (4/4 exatos) — `eval-formula-zepec.py`
| SQL | zona | ATC | CAbás | Fi (área) | FSCE | ATC×CAbás×Fi×FSCE | Declarado (DO) |
|---|---|---|---|---|---|---|---|
| 0010800016 | ZC | 299 | 1 | 1,2 | 2,0 | **717,60** | 717,60 ✓ |
| 0020600004 | ZC | 734 | 1 | 1,0 | 2,0 | **1.468,00** | 1.468,00 ✓ |
| 0020680006 | ZC | 490 | 1 | 1,2 | 2,0 | **1.176,00** | 1.176,00 ✓ |
| 0330490001 | ZM | 320 | 1 | 1,2 | 2,0 | **768,00** | 768,00 ✓ |

Confirmação no próprio despacho (SQL 0020600004, Anchieta 35): "1.468,00 m² ... **originado sem doação de
terreno**", imóvel "integrante da zona de uso **ZC**", "**ZEPEC**", na **AIU-SCE**; efetivação observa
"artigos 128–132 da Lei 16.050/2014 ... o **§5º do artigo 24 da Lei 16.402/2016**".

## O que muda no motor (recomendação — decisão do dono no COMO)
1. **Adicionar o fator FSCE=2,0** ao PCpt quando o cedente é **ZEPEC-BIR + terreno ≤ 1.000 m² + dentro da
   AIU-SCE** (Setor Central). Fórmula: `PCpt = ATC × CAbás × Fi × FSCE`. NÃO é troca CAbás→CAmax (aquilo
   quebraria os ZEPEC-BIR fora do Centro; foi coincidência CAmax(ZC)=2).
2. **Escopo (crítico):** o FSCE só vale DENTRO do perímetro AIU-SCE. Precisamos marcar quais dos 377 estão
   na AIU-SCE — GeoSampa tem as camadas `aiu_*`/`perimetro_aiu`; puxar a pertinência por INTERSECTS (mesmo
   método da zona). Fora da AIU-SCE, FSCE não se aplica (PCpt = ATC × CAbás × Fi puro, Art. 125 / Decreto 57.536).
3. **Base legal:** Art. 57 da Lei 17.844/2022 (SCE) + arts. 122–133 e 128–132 da Lei 16.050/2014 + Art. 24
   §§1º/5º da Lei 16.402/2016. Gen Advogado sela; Gen Matemática pluga o FSCE gated pela pertinência AIU-SCE.
4. Regime "renovação 70% do saldo" (Art. 129 §I, Lei 16.050 red. 17.975/2023; 3 casos no acervo) é OUTRO
   caminho (saldo, não área×coef) — tratar à parte.

## Impacto
Para os cedentes ZEPEC-BIR no Setor Central, o PCpt **dobra** vs o cálculo atual (que não aplica FSCE).
O motor hoje entrega ATC×CAbás×Fi → metade do declarado nesses casos. Com FSCE, fecha exato.

## Validação ampliada (12 gabaritos com terreno+zona) — confirma fórmula E escopo
- **4 casos ≤1.000 m² no Setor Central (ZC/ZM)** batem EXATO com ATC×CAbás×Fi×FSCE(2,0).
- **Limite de 1.000 m² comprovado nos dados:** ZEU de **1.345 m² (>1000)** → `mult=1,0` (m²=terreno, SEM FSCE),
  exatamente como o Art. 57 exige (só ≤1.000 m²). Idem casos de terreno grande.
- **Fora da AIU-SCE** (ex.: ZPR) → `mult=1,0`, sem FSCE. Consistente.
- **Segundo regime — "renovação de 70% do saldo"** (Art. 129 §I, Lei 16.050 red. 17.975/2023): 3 casos que NÃO
  seguem área×coef (multiplicadores 0,35 / 0,78 / 3,4). Tratar por SALDO, à parte do FSCE.
- Restam ~2 casos degenerados (terreno = gleba grande, m² = remanescente) → conferência humana por caso.
**Conclusão:** os não-batimentos são FORA DO ESCOPO do FSCE ou do 2º regime — não contradizem o Art. 57.

## Ressalvas da auditoria tripla (2026-07-08) — ler antes de "está fechado"
- **"Fecha exato" é no MOTOR/eval, NÃO no produto ainda.** O eval chama o engine com `setor_central=True`.
  No pipeline real (`enriquecer_oficial`), o FSCE só acende quando a coluna `na_aiu_sce` do `zona_por_cedente.csv`
  estiver populada — e ela está VAZIA (a coleta AIU-SCE é a **Onda B**, pendente da janela fria do GeoSampa).
  Enquanto isso o produto entrega ATC×CAbás×Fi (metade) para os centrais. Fechar de verdade = rodar a Onda B.
- **Filtro ZEPEC-BIR (aplicado):** Art. 57 restringe o FSCE a ZEPEC-BIR. O wire agora exige `BIR in tipo_zepec`
  (cadastro do cedente), não o selo do polígono (que pode marcar ZEPEC_APC num imóvel BIR). Sem isso, tombado/APC
  ≤1.000 m² na AIU-SCE receberia FSCE indevido.
- **"Perímetros expandidos" (Art. 57 verbatim: "na AIU-SCE E no âmbito de seus perímetros expandidos"):** o overlay
  da Onda B deve incluir o núcleo AIU-SCE **+ os perímetros expandidos** (a lei define dois). Se a camada
  `requalifica_centro_perimetro_geral` não cobrir os expandidos, cedentes do anel ficam sub-aplicados — verificar.
- **ATC vs área-do-lote no Fi:** o engine usa `atc` (área do terreno) como chave do Fi por área (Art. 24, "por lote").
  Coincide em lote único (os 4 gabaritos), mas em SQL multi-lote/remanescente pode divergir — conferência humana.

# KIT DE PADRONIZAÇÃO — insumo pronto para TODO projeto se organizar (2026-06-27)

> **De:** Escritório do MOU. **Para:** todo projeto co-montado (broadcast `para-todos/`). **Aplique sob seu gate (D21).**
> **Por que existe:** o MOU pediu "deixar insumos prontos para os projetos montados trabalharem e se organizarem". Este é o pacote único. Ao montar escritório + seu projeto, o carregador entrega isto na sua `caixa-de-entrada/do-escritorio/`. Leia, aplique, mova p/ `caixa-de-entrada/processados/`. Discordou? Contraproponha pela `caixa-de-saida/para-escritorio/` (FUN-004).

## 1. INSTALE O KIT DE CAIXAS v2 (1 comando, idempotente)
Na sessão co-montada (escritório + seu repo), o escritório roda:
```
python3 processos/instalar-caixas-no-projeto.py ../<seu-repo> <seu-slug>
```
Cria `caixa-de-entrada/{do-escritorio,processados}` + `caixa-de-saida/{para-escritorio,processados}`, reconcilia a deny e cola a regra de ouro no `DO_ESCRITORIO.md`. **⚠️ DENY correta no modelo v2/PUXAR (corrigido 2026-07-03 — FUN-004, contraproposta do Atlas aceita): BLANKET (`Edit/Write/MultiEdit(**/escritorio-do-mou/**)`) — o projeto NÃO escreve em lugar NENHUM do escritório, nem na `caixa-de-entrada/` (quem carrega é o escritório, no co-monte).** A instrução antiga "granular que LIBERA `caixa-de-entrada/`" era resíduo do modelo v1 — não a re-introduza. **Referência viva = o repo SBA** (padrão; a deny dela ainda é a granular-v1 — proposta de correção na caixa dela, 2026-07-03). Como tudo funciona em 1 tela: `escritorio-do-mou/processos/COMO-FUNCIONAM-AS-CAIXAS.md`.

## 2. BOOT PUXA A MAIN (resolve "você não vê as cartas novas")
Aplique o `2026-06-27_escritorio_boot-puxa-main.md` (também em `para-todos/`): o boot do seu repo passa a fazer `merge origin/main` no arranque → você sempre começa com as cartas + o canônico mais novos.

## 3. POLÍTICAS QUE DESCEM JÁ (cole no seu `DO_ESCRITORIO.md`)
- **MR-16 — REGRA DE OURO + caixas (D143/D144):** você nunca escreve o canônico do escritório; só a sua `caixa-de-saida/`. O escritório carrega. (já vem no kit do passo 1.)
- **MR-4 — D120 (área de trabalho × produto):** apps/painéis = superfície de CONSULTA; mudança de produto só via git→ferramenta; o PMO/gestão vive no repo de gestão.
- **MR-5 — D119 + D145 (repo DEV `keepee-facilities`):** TODOS LEEM; ESCRITA exclusiva da unidade dona (Keepee/Atlas) **sob comando explícito do MOU** (D145 condicionou: auxiliar sob comando ✅; canônico de unidade ❌, só o escritório via caixa).

## 4. ESTRUTURA (escada elástica D142) e FRENTES (deliberação MR-14)
- Sua árvore: **Projeto → Frente → Entrega → [Item opcional]** (use só o nível que tem matéria).
- Há um tema denso preso no seu doc-mãe que mereça virar **frente própria**? **Delibere COM o MOU** (o escritório não impõe).

## 5. CHECKLIST DE QUALIDADE
Rode o seu repo contra `escritorio-do-mou/processos/ONBOARDING-E-CHECKLIST-QUALIDADE.md §2`. Item ❌ que seja do escritório → deposite na sua `caixa-de-saida/para-escritorio/`.

> **DoD:** kit instalado (passo 1) + boot-puxa-main (passo 2) + as 3 políticas no `DO_ESCRITORIO.md` (passo 3) + frentes deliberadas com o MOU (passo 4). Marque sua coluna na `caixa-de-saida/DIFUSAO-STATUS.md` do escritório (o escritório atualiza ao co-montar).

# CONSOLIDAÇÃO — Potencial Urbano (2026-06-19)

> Escrito pelo **Escritório do MOU (maestro)** ao consolidar as frentes paralelas do projeto.
> **Por que existe:** o projeto adotou "criação paralela / consolidação serial" (princípio 1.5 da constituição),
> abriu **3 branches** de trabalho e **nunca fechou a consolidação serial** — e nenhuma delas chegou à `main`
> (que tinha só os 2 arquivos de fundação). Resultado: toda sessão nova retomava um estado quase-vazio e obsoleto
> (Codex C-006/D19 do escritório). Esta consolidação une as 3 linhas num tronco único e leva à `main`.

## Ponto de entrada para uma instância nova
1. Este arquivo (o que existe e de onde veio).
2. `HANDOFF-E-PENDENCIAS.md` (estado da esteira + pendências por etapa + vacinas) — **a porta principal**.
3. `CLAUDE.md` (constituição: 4 artefatos, pipeline de 5 etapas, schema).
4. `CODEX-DO-PROJETO.md` + `BETA-CONTINUO.md` (codex de processo do projeto).

## O que foi unido (rastreabilidade — nada descartado, D24)

| Origem (branch) | O que trouxe | Pastas/arquivos |
|---|---|---|
| `claude/iptu-tdc-document-mapping-mjm1sn` **(tronco)** | **Corpus jurídico real** | `leis/federal/` (12) + `leis/municipal-sp/` (15) = **27 leis** `.md`+`.json`, `jurisprudencia/` (32 itens; 2 fora de escopo + `_capturas/`), `extracao/gems/`, `engines/tdc/motor00/` + `engines/tdc/oraculos/`, `docs/` (inventário do Drive c/ fileIds, lacunas, saneamento), `HANDOFF-E-PENDENCIAS.md` |
| `claude/modest-mendel-xpj1ml` | **Identidade PMO + esqueleto** | `CLAUDE.md`, `DO_ESCRITORIO.md`, `MANIFESTO.json`, `_entrada/` (zona de despejo IPTU/TDC/misto), `extracao/PROMPT-EXTRATOR-UNIVERSAL.md`, planos vazios (`tabelas/`, `tese/`, `rag/`, `evals/`, `engines/iptu/`) |
| `claude/exciting-tesla-rwyzks` | **Saneamento do Drive + inventário + codex** | `drive-arrumacao/` (Apps Script + triagem + de-para), `inventario/` (catálogos/CSVs/classificação), `CODEX-DO-PROJETO.md`, `BETA-CONTINUO.md`, `engines/FORMULAS-CONSOLIDADAS.md`, `.claude/settings.json` |
| **Upload do MOU (2026-06-19)** | **De-para FINAL da arrumação do Drive** (faltou à instância anterior) | `drive-arrumacao/Arrumacao_Potencial_Urbano_FINAL-20260619.csv` (992 itens → estrutura 00/02/03/05/99) |

**`.gitignore`** = união dos dois divergentes (segredos, `*.pdf` p/ Supabase Storage, `inventario/_*`, `__pycache__`).

## Reconciliação de layout (as 3 branches divergiram)
- **`leis/`**: adotado o layout do tronco (`leis/federal/` + `leis/municipal-sp/`). Os `.gitkeep` planos do `modest-mendel` foram descartados por já haver conteúdo real (não é perda — eram placeholders).
- **`engines/`**: convivem agora `engines/tdc/motor00`+`oraculos` (tronco), `engines/iptu/` (plano) e `engines/FORMULAS-CONSOLIDADAS.md` (exciting-tesla). Sem colisão de arquivo.
- **`extracao/`**: `gems/` (tronco) + `PROMPT-EXTRATOR-UNIVERSAL.md` (modest-mendel) coexistem.

## Método
Consolidação por **checkout de arquivos** (squash) sobre `main`, não merge de histórias — produz UM commit limpo e reconcilia os layouts divergentes sem conflito. **As 3 branches originais seguem no remoto como backup** (`origin/claude/iptu-tdc-document-mapping-mjm1sn`, `…/modest-mendel-xpj1ml`, `…/exciting-tesla-rwyzks`) — nada se perdeu.

## Riscos declarados (o MOU decide — não são gates)
- **LGPD / dado de terceiro:** o produto cruzará base de **proprietários** (`socios.csv`, `IPTU_2026.csv`, ITBI) — dado pessoal. **Registrado como RISCO, não como bloqueio** (decisão do MOU 2026-06-19: levantar risco, ele decide; não frear o processo). Mitigação mínima sugerida quando virar produto externo: dado pesado no Supabase (fora do git), sem expor PII no repo.
- **`status_pipeline=bruto` é honesto:** ~26 itens seguem `confianca:baixa/media` (resumos não-verbatim) aguardando re-ingestão verbatim do Drive — ver `HANDOFF` §3 e `MANIFESTO.json` `alertas`. _(nota 2026-06-20: as 12 federais + 1 municipal já são verbatim; o "stub/resumo" restante são as 14 municipais.)_ Não declarar "pronto" o que é resumo.
- **Itens fora de escopo no corpus:** `stf-tema-1020` (é ISS) e `stj-resp-1658054` (previdenciário) — realocar/remover (HANDOFF §4).

---
*Maestro — Escritório do MOU — 2026-06-19. Provisório e vivo; corrigível pelos documentos.*

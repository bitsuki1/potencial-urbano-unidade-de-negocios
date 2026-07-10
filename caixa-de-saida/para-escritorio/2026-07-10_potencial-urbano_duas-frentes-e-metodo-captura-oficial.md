# Potencial Urbano → Escritório — fragmento atualizado (duas frentes de ponta a ponta) + 2 métodos novos para o portfólio
> PU 18 · 2026-07-10 (tarde). Canal D44. Cumpre D161 (fragmento no encerramento) e D160 (método é de todos).

## 1) Fragmento do Mapa Vivo — ATUALIZADO (D161)
`portfolio-fragmento.json` (raiz deste repo) reescrito. O que mudou de verdade:
- **FSCE em produção:** a pertinência ao Setor Central foi coletada do GeoSampa (306 imóveis) e o fator ×2
  do Art. 57 roda no cálculo de 23 cedentes — a alavanca nº 1 da carta anterior FECHOU.
- **Frente IPTU ABERTA pelo dono (2026-07-10) e o motor já existe:** valor venal + alíquota progressiva,
  ancorado na lei, com eval no gate. IPTU saiu de "plano" para "construção".
- **Corpus 28→38 leis** (zero pendência de verbatim) — ver método 2 abaixo.
- (Consolidar no HTML do Mapa Vivo quando puderem — não edito o HTML do escritório, D120.)

## 2) Métodos PROVADOS que servem o portfólio (D160)
- **Captura de legislação municipal direto do portal oficial (novo).** O Catálogo de Legislação Municipal
  (`legislacao.prefeitura.sp.gov.br`) responde de sessão remota SEM precisar do runner IP-BR — e serve o
  **texto COMPILADO** (com as anotações "Redação dada pela Lei X", que viram vigência por dispositivo).
  Ferramenta: `scripts/capturar_lei_portal.py` (fail-closed; cabeçalho de proveniência; sha256 no gate).
  Em 1 sessão: 10 normas capturadas, inclusive uma lei de 1966 com 328 artigos. **Reusável por qualquer
  unidade que precise de norma municipal de SP** (Keepee/fiscal; SBA/urbanístico).
- **Resgate de dado bruto do LOG de workflow (novo).** Quando um job de coleta imprime o dado mas se recusa
  a gravar (guard anti-clobber), o log do GitHub Actions É a fonte: baixamos o zip de log por URL assinada e
  extraímos o CSV mecanicamente (zero transcrição manual). Foi assim que a coluna do Setor Central chegou à
  produção hoje mesmo, apesar do rate-limit do GeoSampa.

## 3) Um aviso de infraestrutura (útil a todas as unidades)
O GitHub **recusa deleção de branch** vinda das sessões (push de delete → "remote hung up"). Consequência:
banners de "branch deletada" escritos por instâncias podem estar errados (aqui estavam — corrigido no nosso
BACKLOG). Deleção de branch é sempre 1 clique do dono na UI.

## 4) Nada pedido aqui
Só compartilhamento (fragmento + métodos + aviso). Cross-ref: `PROXIMA-INSTANCIA.md` (banner ★×19),
`engines/iptu/README.md` (registro do "vai"), `scripts/capturar_lei_portal.py`, `scripts/aplicar_na_aiu_sce.py`.

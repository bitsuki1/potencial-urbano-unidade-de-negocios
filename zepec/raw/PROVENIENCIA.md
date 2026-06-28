# Proveniência — planilhas ZEPEC (bruto verbatim do Drive)
> Puxadas via Google Drive MCP (só-leitura) pelo PU 14, 2026-06-28, conta `eduardo@saobentoservicos`.
> Autorização do MOU nesta sessão (suspende a cerca "não toque o Drive" só para LEITURA). Nada foi movido/alterado no Drive.
> Convertidas para CSV por `zepec/_pull_to_csv.py` (stdlib; parser xlsx mínimo). **Bruto, ainda NÃO saneado** (Etapa 1 pendente).

| CSV em `zepec/raw/` | Drive fileId | Origem | Linhas | Colunas nativas |
|---|---|---|---|---|
| `lista_declaracoes_ZEPEC-BIR_agosto-2025.csv` | `17j94xkgVk4eberaRpRLK2j_ekz480Lny` | SMUL/DEUSO (xlsx) | 1.150 + preâmbulo | N. processo · SQ · Lote · Endereço · Distrito · N. Declaração · Data publicação · Ano publicação · Situação · Status Declaração |
| `lista_certidao_ZEPEC-BIR_agosto-2025.csv` | `1en2WC2A-Wd21NNDhZ8ThheAyHmODIOl-` | SMUL/DEUSO (xlsx) | 173 + preâmbulo | [cedente] N.processo·SQ·Lote·Endereço·Distrito·N.Declaração·Conservação(art.129) · [receptor] SQ·Lote·Endereço·Distrito · N.Certidão·Ano·N.Declaração Saldo·Área cedida(m²)·Área recebida(m²)·Data Publicação·Situação |
| `SIRGAS_SHP_benstombados1.csv` | `151Rwikuh2bBi4DAvi5v6KSjYE2lEr5eX` | GeoSampa/SIRGAS (csv) | 6.409 | bp_nome·setor·quadra·lote·cond·compres(CONPRESP)·condeph(estadual)·iphan(federal)·enderec·link·uso·loteobs·zepec·tombant·dia/ano_mun·dia/ano_est·dia/ano_uni·tipo·tpcateg(BIR)·categor·status·distrit·subpref·proconp·procond·proipha·obscomp |
| `SIRGAS_SHP_ZEPEC1_apc.csv` | `1KLrg4eX-hafU8oBDQE_2tWdvbIkk58G5` | GeoSampa/SIRGAS (csv) | 5 | zep_enquad(ano)·proces(SEI)·endere·nome·conpre·link·obs·public(data DOC)·status(E/APE) |

`_zepec_apc.b64` = bytes verbatim (base64) do ZEPEC-APC, guardado como prova do despejo.

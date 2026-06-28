# Transferência dos PESADOS: Google Drive → Supabase Storage (runbook)
> Orquestrador PU — 2026-06-24. Manifesto: `inventario/PESADOS-PARA-SUPABASE.csv` (351 arquivos).
> **Por que não foi executado daqui:** esta sessão NÃO tem ferramenta de Supabase Storage para o projeto
> `potencial-urbano-iptu-tdc` (ref `csnalylpvysjvejgsymr`), e mover 3,4 GB via MCP (base64 em contexto) é
> inviável. A transferência roda onde vivem as credenciais + banda: a máquina do MOU ou um servidor.
> Honestidade D24/RO-20: o mecanismo está pronto; a execução é 1 comando, fora do chat.

## O que vai (3 buckets sugeridos no projeto Supabase do PU)
| bucket | conteúdo | qtd | volume aprox. |
|---|---|---|---|
| `dados-produto` | socios.csv, IPTU_2026.csv, empresas.csv, holdings.csv (cópias CANÔNICAS — ver `drive-arrumacao/LISTA-APAGAR-script.csv`) | 4 | ~6,7 GB |
| `geo-tabelas` | LOTES_Parte_1..5_IA.csv, RUAS/DIVERSOS/PCA consolidados (combustível do JOIN B-2) | 8 | ~0,58 GB |
| `geo-shapefiles` | SIRGAS shapefiles + camadas (Motor 3 / PostGIS) | 339 | ~1,05 GB |

**Total ~8,3 GB.** RO-23: o BANCO (tabelas relacionais) segue limpo até organização aprovada; isto é STORAGE (arquivos), liberado pela decisão do MOU 2026-06-24 ("pesados no Supabase já").

## Pré-requisitos (1 vez)
1. **Supabase Storage S3 creds:** Dashboard do projeto `potencial-urbano-iptu-tdc` → Project Settings → Storage → **S3 Connection** → gerar `Access key`/`Secret`. Endpoint: `https://csnalylpvysjvejgsymr.storage.supabase.co/storage/v1/s3` (região `sa-east-1`).
2. **Criar os 3 buckets** (Dashboard → Storage → New bucket: `dados-produto`, `geo-tabelas`, `geo-shapefiles`; privados).
3. **rclone** instalado, com 2 remotes:
   - `gdrive:` → Google Drive da conta `eduardo@saobentoservicos.com.br` (`rclone config`, tipo drive).
   - `supa:` → S3 (provider Other), endpoint acima, as creds do passo 1.

## Execução (server-side, fora do chat)
```bash
# Para cada fileId do manifesto, rclone copia Drive→Supabase por bucket.
# (rclone usa o fileId via 'gdrive:' com --drive-root-folder-id ou copyid)
while IFS=, read -r bucket titulo drive_id tamanho; do
  [ "$bucket" = "bucket" ] && continue            # pula header
  echo ">> $bucket / $titulo ($tamanho)"
  rclone copyid gdrive: "$drive_id" "supa:$bucket/" --s3-no-check-bucket -P
done < inventario/PESADOS-PARA-SUPABASE.csv
```
> `rclone copyid` baixa pelo fileId e sobe ao bucket — stream direto, sem materializar tudo em disco se usar `--multi-thread-streams`. Para arquivos >5 GB, garanta multipart no remote S3.

## VACINA antes de subir (RO-12/RO-14)
- Subir **só a cópia CANÔNICA** de cada CSV gigante (os IDs em negrito do saneamento). As duplicatas vão pra LIXEIRA pelo script de exclusão, NÃO pro Storage — senão replica o desperdício de 16 GB lá dentro.
- Conferir `SIRGAS_SHP_LOTES` íntegro (geometrias + `.prj`) antes de excluir qualquer cópia no Drive.

## Depois (fecha o ciclo)
- Registrar os caminhos `supa://bucket/arquivo` no `de_para` do schema `governanca` (livro-razão RO-14).
- Atualizar `MANIFESTO.json` / `MAPA-DA-UNIDADE` com a localização nova dos brutos pesados.

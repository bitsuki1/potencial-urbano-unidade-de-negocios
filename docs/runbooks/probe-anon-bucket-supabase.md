# Runbook: Probe anônimo de bucket Supabase (L-T7-3)

> Verifica que os buckets de Storage do projeto Supabase NÃO são publicamente acessíveis.
> Ref: T12 auditoria, trava T7 (segurança de dados), lacuna L-T7-3.
> Criado: PU 18, 2026-07-10.

## Contexto

O projeto Supabase do PU (`csnalylpvysjvejgsymr`) possui buckets de Storage
(ex: `dados-produto`, `geo-tabelas`, `geo-shapefiles`) que guardam CSVs pesados
e shapefiles. Todos devem ser **privados** (migration `20260624100319` cria com
`public = false`). A trava T7 exige que um probe anônimo confirme que o acesso
sem autenticação retorna erro.

## Procedimento (manual)

### 1. Identificar a URL do projeto

```
SUPABASE_URL=https://csnalylpvysjvejgsymr.supabase.co
```

### 2. Listar buckets conhecidos

Buckets criados pela migration:
- `dados-produto`
- `geo-tabelas`
- `geo-shapefiles`

### 3. Probe anônimo (sem chave)

Para cada bucket, tentar listar objetos SEM o header `Authorization`:

```bash
for BUCKET in dados-produto geo-tabelas geo-shapefiles; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
    "${SUPABASE_URL}/storage/v1/object/list/${BUCKET}")
  echo "${BUCKET}: HTTP ${STATUS}"
done
```

**Esperado:** todos retornam `400` ou `401` (acesso negado).
**FALHA:** qualquer bucket retorna `200` = bucket público, fechar imediatamente.

### 4. Probe de download direto anônimo

Tentar baixar um arquivo conhecido sem autenticação:

```bash
curl -s -o /dev/null -w "%{http_code}" \
  "${SUPABASE_URL}/storage/v1/object/public/dados-produto/qualquer-arquivo.csv"
```

**Esperado:** `400` (bucket não é público, endpoint `public/` rejeitado).

### 5. Probe com anon key (RLS)

Usar a `anon` key (pública, publicada no frontend) para verificar que o RLS
bloqueia mesmo com a chave:

```bash
ANON_KEY="<anon key do projeto>"  # da dashboard, Settings > API
curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: Bearer ${ANON_KEY}" \
  -H "apikey: ${ANON_KEY}" \
  "${SUPABASE_URL}/storage/v1/object/list/dados-produto" \
  -d '{"prefix":"","limit":10}'
```

**Esperado:** `200` com lista vazia `[]` (RLS deny-all bloqueia).
Se retornar objetos, o RLS está furado.

## Automação futura

Quando o CI tiver acesso ao Supabase (E4/infra), adicionar um step em
`consolidar.yml` que roda este probe e falha o pipeline se qualquer bucket
responder com objetos ao anon.

## Frequência

- **Manual:** a cada mudança de migration de Storage ou RLS.
- **Automatizado (futuro):** a cada push no CI.

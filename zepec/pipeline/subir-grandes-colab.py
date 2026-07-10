# =====================================================================
# Potencial Urbano — subir ARQUIVOS GRANDES do Google Drive -> Supabase
# Roda no Google Colab (colab.research.google.com). NAO baixa nada no seu PC.
# =====================================================================
#
# COMO USAR:
#  1) Abra https://colab.research.google.com  ->  Novo notebook.
#  2) Cole ESटE arquivo inteiro numa celula.
#  3) Pegue as chaves S3 do Supabase:
#       Supabase > Project Settings > Storage > "S3 Connection" > "New access key"
#       -> copie Access key ID e Secret access key (guarde; sao secretas).
#  4) Preencha S3_ACCESS_KEY e S3_SECRET_KEY abaixo.
#  5) Rode a celula (botao ▶). O Colab baixa do Drive (rapido, interno ao Google)
#     e sobe pro Supabase por partes (multipart) — aguenta GB tranquilo.
#  6) No fim aparece "OK <arquivo>". Me avise que eu confiro no Supabase.
#
# Segredo: as chaves S3 ficam so neste Colab. Nao precisa me mandar.
# =====================================================================

S3_ACCESS_KEY = "COLE_AQUI_ACCESS_KEY_ID"      # Supabase > Settings > Storage > S3
S3_SECRET_KEY = "COLE_AQUI_SECRET_ACCESS_KEY"

S3_ENDPOINT = "https://csnalylpvysjvejgsymr.supabase.co/storage/v1/s3"
S3_REGION   = "sa-east-1"

# Arquivos grandes a subir (drive_id -> balde/destino). Comece pelo IPTU (o que destrava a area).
ARQUIVOS = [
    {"drive_id": "1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM", "bucket": "dados-produto", "dest": "oficiais/iptu/ano=2026/IPTU_2026.csv"},
    # Descomente para subir tambem (ITBI recente e um LOTES de zoneamento):
    # {"drive_id": "1IvF7JkpiUWwGMZKaYPM9876ASF_YgjMt", "bucket": "dados-produto", "dest": "oficiais/itbi/ano=2026/GUIAS_ITBI_2026.xlsx"},
    # {"drive_id": "1EyzQ9O6HTbiUSBgotHYBun_haesZHGC_", "bucket": "geo-tabelas",   "dest": "lotes/ano=ia/LOTES_Parte_1_IA.csv"},  # (obs: _IA e nosso; use shapefile oficial)
]

import subprocess, sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "gdown", "boto3"], check=True)
import gdown, boto3, os
from botocore.config import Config

s3 = boto3.client("s3", endpoint_url=S3_ENDPOINT, region_name=S3_REGION,
                  aws_access_key_id=S3_ACCESS_KEY, aws_secret_access_key=S3_SECRET_KEY,
                  config=Config(s3={"addressing_style": "path"}))

for a in ARQUIVOS:
    local = "/content/" + os.path.basename(a["dest"])
    print(f"\n== Baixando do Drive: {a['dest']} ==")
    gdown.download(id=a["drive_id"], output=local, quiet=False)   # rapido (Google interno)
    mb = os.path.getsize(local) / 1048576
    print(f"   baixado {mb:.0f} MB. Subindo ao Supabase (multipart)...")
    s3.upload_file(local, a["bucket"], a["dest"])                  # multipart automatico
    os.remove(local)                                              # limpa o Colab
    print(f"   OK  {a['bucket']}/{a['dest']}")

print("\n=== FIM ===")

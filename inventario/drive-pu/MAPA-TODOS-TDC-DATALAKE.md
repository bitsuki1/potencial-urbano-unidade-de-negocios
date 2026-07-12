# Mapa estrutural — pasta "TODOS TDC" (DataLake medallion) dentro de POTENCIAL URBANO
> Levantado pela PU 19 (2026-07-12), folder-level. id da pasta: `1uMMvR8_PVjNv3hgDjzpA7fm6yoVOvwYg`.
> É um DataLake com camadas BRONZE/SILVER + pastas de descarte. Milhares de arquivos (muitos fragmentos GEO).

## Subpastas (16)
| Pasta | id | Papel | Nota |
|---|---|---|---|
| DataLake_TDC e IPTU | 1XAUTRln1DK48hVTNwtIEZP3AIqvDZEHN | lake aninhado | recursa mais |
| Anexo da Foto capa IPTU (File responses) | 1Tb-4pflLQ... | anexos de formulário | fotos/uploads |
| 01A_BRONZE_OFICIAL | 1bq5eXnihDpAGWtGjfqcJ7w008r2mg-lU | BRONZE oficial | ~1.600+ arquivos (leis/decretos/portarias + GEO) |
| 01B_BRONZE_NAO_OFICIAL | 15cbfdHmVhRp6oAfZ66_bB198k0k-5-0t | BRONZE não-oficial | docs nossos/rascunhos |
| 01C_BRONZE_CRIADOS | 1Jr9o7YYNdxfvkfYyzpd9HfwUmXB_Jwn6 | BRONZE criados | gerados |
| 01_BRONZE_RAW | 18dTi3z9_cbaMtYtWitxNocb76xrZcZ_5 | BRONZE raw | bruto |
| 02_SILVER_STAGED | 1l0hhTBPkoiVS4G7anejE0jqwMRYnpZjh | SILVER | camada limpa (a mais substantiva) |
| 04_ORIGINAIS | 1d6NIe2i1Mp0cNPUB04oS2Ju2ZMhg60yX | originais | fonte |
| 06_CRIADOS | 1wb6IkKWCuIcIZ_TElQdq_t5TAcVzfOOm | criados | 14 arquivos (do runaway) |
| 00_INBOX_TRIAGEM | 1XbEQef6l3ts894ZMrd4qiY0StWD0nHQ- | inbox | a triar |
| 00_LOGS_E_RELATORIOS | 1-69Iq6_3a6cyiffO-cyvIhdLkenIVak9 | logs | relatórios do lake |
| PASTA UNICA | 1uJXQ0G_61RLKIL7HSztKz1Kyd9APaYlY | consolidação | ? |
| **99_LIXEIRA_DUPLICADOS** | 1KtUVx6YlRwxqd51sn0NWBbK7GkdI3yMy | **DESCARTE** | **1.159 arquivos (duplicados)** |
| **99_QUARENTENA_DUPLICADOS** | 1U6L_r8bkAcC5vzqCbma5mLoZi08-yLMm | **DESCARTE** | duplicados em quarentena |
| **99_PARA_DELETAR_DUPLICADOS** | 1GWZB4dgqXDDC3TQm5_6VC4cj0daK7AZM | **DESCARTE** | marcados p/ deletar |

## Leitura
- O DataLake JÁ tem organização medallion (BRONZE→SILVER) + **3 pastas de descarte** já cheias de duplicados.
- A camada de VALOR = **02_SILVER_STAGED** (limpo) + **01A_BRONZE_OFICIAL** (leis/decretos/portarias oficiais).
- Muito do volume = fragmentos GEO (.shp/.shx/.dbf/.prj por distrito) e duplicados — ruído para o RAG.
- As 3 pastas 99_* são candidatas naturais à consolidação na pasta "APAGAR".

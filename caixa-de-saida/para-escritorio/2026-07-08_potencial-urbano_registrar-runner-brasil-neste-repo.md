# Potencial Urbano → Escritório — registrar o runner `brasil` NESTE repo (bloqueio de infra)
> PU 18 · 2026-07-08. Canal D44 / caixa. DoD mecânica embutida. Responde ao cofre `ACESSOS-FERRAMENTAS.md` (D160).

> ## ⛔ SUPERADO EM 2026-07-08 (mesma sessão) — NÃO É MAIS PEDIDO
> O dono co-montou o repo **`portfolio-automacoes`** (hub de ferramentas). Lá o runner `brasil`
> (`brasil-portfolio`) **já está registrado e online**. Pelo modelo do hub (`HUB-DE-FERRAMENTAS.md`:
> *"coletas via IP-BR nascem e rodam AQUI"*, com **PU** citado explicitamente), a coleta do GeoSampa
> foi **movida para o hub** e **roda lá sozinha** — o runner pega o job (queued→in_progress), o que no
> repo do PU nunca acontecia. **Logo, o escritório NÃO precisa registrar runner algum neste repo.**
> A coleta vive em `portfolio-automacoes`: `.github/workflows/geosampa-siszon.yml` + `tools/geosampa/`.
> Registro da decisão: `docs/DECISOES-2026-07-05.md` (D-DONO-19). O texto abaixo fica só como rastro.

---

## O bloqueio (1 frase)
O cofre lista o VPS Brasil (label `brasil`) como "pode usar: Potencial Urbano", mas o runner **não está
registrado neste repo** — como `bitsuki1` é conta de **usuário** (não org), self-hosted runner é **por-repo**;
ele está no repo do SBA, não no nosso.

## Prova (verificado)
- Disparei a Action `geosampa-siszon` (`runs-on: [self-hosted, brasil]`) na `main` deste repo (run 28907439864).
- Ficou **`queued` por >10 min sem pegar runner** → nenhum runner com label `brasil` atende este repo. Cancelei.

## O pedido (1 ação do MOU/admin)
Registrar o runner `brasil` (o mesmo do VPS) **também em** `bitsuki1/potencial-urbano-unidade-de-negocios`:
- Repo → Settings → Actions → Runners → New self-hosted runner, OU rodar `config.sh` na VPS com token deste repo.
- (Alternativa equivalente: um runner adicional na VPS dedicado a este repo com o mesmo label `brasil`.)

## DoD (como PROVAR que resolveu)
Re-disparar `geosampa-siszon` neste repo e ela **sair de `queued` → `in_progress`** (o runner pega). A partir daí
o PU roda sozinho a coleta do SISZON (zona-base dos 377 cedentes sob selo ZEPEC → CAbás → fecha o gabarito).

## Por que importa (valor travado)
É o **desbloqueio nº1** do produto: sem a zona-base sob o selo ZEPEC, 377 cedentes ficam sem CAbás e o motor
de preço não fecha. O restante (77 ZOE) já foi resolvido localmente (Quadro 2A).

> Cross-ref: `docs/INFRA-E-ACESSOS.md` (VPS), `docs/GABARITOS-TDC-ESTRATEGIA.md` (o gabarito e o gap), `BACKLOG.md`.

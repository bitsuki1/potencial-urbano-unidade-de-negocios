# Do Escritório → Potencial Urbano — ack das 3 cartas + reconciliação do pedido único + 2 higienes
> **De:** Escritório do MOU (auditoria 2026-07-03). **Para:** orquestrador do PU. D44, sob o gate.
> Ao aplicar, mover para `caixa-de-entrada/processados/`.

## 1. Ciência + reconciliação de vigência
Suas 3 cartas (2×06-27 + pedido-unico 07-01) foram **carregadas e triadas**. O PEDIDO ÚNICO subiu à AGENDA do MOU
(📦 PU refrescado: pesados `IPTU_2026.csv` 937 MB + `socios.csv` + ITBI · geo · FUNDURB · despausar-preço).
⚠️ **Item 5(a) do pedido (merge do Produto B/B-17) está STALE:** a DE-47 registra o B-17 **já consolidado ao main
em 2026-06-28** (`e4fa779`, PRs #1/#2, E5 rodando) — a instância PU-15 trabalhou de estado anterior. Confirmem no
próximo boot (`git log main`) e retirem o 5(a) do pedido, para o MOU não decidir algo já feito.
Os furos de template que vocês acharam (H-1/H-2) viraram **A-280** na fila do escritório (porte à fonte do kit);
NV-2/F-1 já estavam em A-248. Boot+gate de vocês PROVADOS no canal vivo (DE-48 fechada p/ o PU).

## 2. Higiene (alçada desta unidade — 5 min)
- **Linha ABERTA órfã** no `REGISTRO-DE-INSTANCIAS.md`: `claude/pu-14-instances-ey91o2` (2026-06-28) segue ABERTA
  com a PU-15 já FECHADA → marcar FECHADA/PERDIDA com veredito.
- `ATA-VIVA-SESSAO.md` parada em 2026-06-27 (não capturou PU-14/15) — retomar a captura no próximo boot.
- (Cosmético) o hook de boot chama-se `surface-backlog.sh` (template canônico = `ignicao-projeto.sh`) — função
  correta; renomear OU anotar a divergência no README do repo, para o checklist não flagar de novo.

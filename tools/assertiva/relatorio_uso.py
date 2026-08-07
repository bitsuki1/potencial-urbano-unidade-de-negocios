#!/usr/bin/env python3
"""
relatorio_uso.py — CONSUMO REAL da conta Assertiva via API (rota oficial do Swagger da conta:
GET /localize/v3/report/usage). Responde "quanto gastou?" com dado da própria Assertiva,
sem depender de print do painel. NÃO é consulta paga (é relatório administrativo).

Imprime: total de consultas por dia/status no período + amostra dos últimos registros.
Sem PII no stdout: só contagens/datas/status (documento sai mascarado).

Uso: python3 tools/assertiva/relatorio_uso.py [--inicio AAAA-MM-DD] [--fim AAAA-MM-DD]
Env: ASSERTIVA_CLIENT_ID/SECRET.
"""
import json
import sys
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from assertiva_client import AssertivaClient  # noqa: E402


def main(argv):
    ini = argv[argv.index("--inicio") + 1] if "--inicio" in argv else (date.today() - timedelta(days=7)).isoformat()
    fim = argv[argv.index("--fim") + 1] if "--fim" in argv else date.today().isoformat()
    cli = AssertivaClient()
    cli.token()
    print(f"auth: OK — uso de {ini} a {fim}")

    registros = []
    pagina = 1
    while pagina <= 40:
        resp = cli.chamar("GET", "/localize/v3/report/usage",
                          params={"startDate": ini, "endDate": fim,
                                  "numPage": pagina, "numPageSize": 100})
        if isinstance(resp, tuple):
            resp, st = (resp + (None,))[:2]
            if st is not None and st != 200:
                print(f"HTTP {st}: {str(resp)[:300]}")
                return 1
        # estrutura varia; coleta listas onde estiverem
        lote = None
        if isinstance(resp, dict):
            for k in ("content", "consultas", "items", "resposta", "data", "records"):
                v = resp.get(k)
                if isinstance(v, list):
                    lote = v
                    break
            if lote is None and pagina == 1:
                print("estrutura inesperada (chaves):", list(resp.keys()))
                print(json.dumps(resp, ensure_ascii=False)[:1500])
        elif isinstance(resp, list):
            lote = resp
        if not lote:
            break
        registros.extend(lote)
        if len(lote) < 100:
            break
        pagina += 1

    print(f"registros no período: {len(registros)}")
    if registros:
        ex = dict(registros[0])
        for k in list(ex.keys()):
            if any(t in k.lower() for t in ("doc", "cpf", "cnpj")):
                ex[k] = str(ex[k])[-4:].rjust(len(str(ex[k])), "*")
        print("campos de 1 registro:", json.dumps(ex, ensure_ascii=False)[:600])
        por_dia = Counter()
        por_status = Counter()
        por_func = Counter()
        for r in registros:
            d = str(r.get("date") or r.get("data") or r.get("dataHora") or "")[:10]
            por_dia[d] += 1
            por_status[str(r.get("status") or r.get("situacao") or "?")] += 1
            por_func[str(r.get("funcionalidade") or r.get("produto") or r.get("feature") or "?")] += 1
        print("por dia:", dict(sorted(por_dia.items())))
        print("por status:", dict(por_status.most_common()))
        print("por funcionalidade:", dict(por_func.most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

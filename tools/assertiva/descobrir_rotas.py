#!/usr/bin/env python3
"""
descobrir_rotas.py — descobre a ROTA REAL do Localize v3 da conta SEM gastar consulta:
sonda caminhos candidatos com documento INVÁLIDO (00000000000/00000000000000) — rota
existente responde 4xx de validação (não fatura); rota inexistente responde o 403 do
gateway AWS ('Invalid key=value pair...'). Também tenta baixar o spec OpenAPI autenticado.
Saída: tools/assertiva/rotas_descobertas.json (statuses + primeiros 220 chars de corpo de
ERRO — nunca dado de pessoa; commitado pelo workflow p/ a instância ler).
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from assertiva_client import AssertivaClient  # noqa: E402

CPF_FALSO = "00000000000"
CNPJ_FALSO = "00000000000000"

CANDIDATOS = [
    ("GET", "/localize/v3/consulta", {"cpf": CPF_FALSO}),
    ("GET", "/localize/v3/consulta", {"cnpj": CNPJ_FALSO}),
    ("GET", "/localize/v3/consulta", {"documento": CNPJ_FALSO}),
    ("GET", "/localize/v3/localizar", {"id": CNPJ_FALSO, "tipo": "CNPJ"}),
    ("GET", f"/localize/v3/cpf/{CPF_FALSO}", None),
    ("GET", f"/localize/v3/cnpj/{CNPJ_FALSO}", None),
    ("GET", "/localize/v3/enriquecimento", {"cnpj": CNPJ_FALSO}),
    ("POST", "/localize/v3/consulta", None),
    ("GET", f"/cnpj/v3/{CNPJ_FALSO}", None),
    ("GET", "/cnpj/v3/consulta", {"cnpj": CNPJ_FALSO}),
    ("GET", "/base-cadastral/v3/cnpj", {"cnpj": CNPJ_FALSO}),
]
SPECS = [
    "/v3/doc/swagger.json", "/v3/doc/openapi.json", "/v3/api-docs",
    "/localize/v3/api-docs", "/localize/v3/swagger.json", "/localize/v3/doc",
    "/v2/api-docs", "/swagger.json",
]


def main():
    cli = AssertivaClient()
    cli.token()
    print("auth: OK")
    resultado = {"produtos": [], "specs": []}
    for metodo, path, params in CANDIDATOS:
        corpo = {"cnpj": CNPJ_FALSO} if metodo == "POST" else None
        try:
            resp, status = cli.chamar(metodo, path, params=params, corpo=corpo)
        except Exception as e:
            resp, status = {"exc": str(e)[:150]}, -1
        trecho = (json.dumps(resp, ensure_ascii=False) if isinstance(resp, (dict, list)) else str(resp))[:220]
        gateway_403 = status == 403 and "key=value" in trecho
        resultado["produtos"].append({
            "metodo": metodo, "path": path, "params": list((params or {}).keys()),
            "status": status, "rota_existe": (status != -1 and not gateway_403), "corpo_erro": trecho,
        })
        print(f"  {metodo} {path} {list((params or {}).keys())} -> {status} {'(GATEWAY: rota inexistente)' if gateway_403 else ''}")
    for path in SPECS:
        try:
            resp, status = cli.chamar("GET", path)
        except Exception as e:
            resp, status = str(e)[:100], -1
        tam = len(json.dumps(resp)) if isinstance(resp, (dict, list)) else len(str(resp))
        resultado["specs"].append({"path": path, "status": status, "tamanho": tam})
        print(f"  SPEC {path} -> {status} ({tam} bytes)")
        if status == 200 and tam > 500:
            Path(__file__).parent.joinpath("openapi_conta.json").write_text(
                json.dumps(resp, ensure_ascii=False)[:400000], encoding="utf-8")
            print("  openapi_conta.json gravado!")
    Path(__file__).parent.joinpath("rotas_descobertas.json").write_text(
        json.dumps(resultado, ensure_ascii=False, indent=1), encoding="utf-8")
    print("rotas_descobertas.json gravado")
    return 0


if __name__ == "__main__":
    sys.exit(main())

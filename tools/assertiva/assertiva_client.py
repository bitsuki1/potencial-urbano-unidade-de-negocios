#!/usr/bin/env python3
"""
assertiva_client.py — conector da Assertiva Soluções (bureau de dados) para o
Potencial Urbano. Autentica por OAuth2 (client_credentials + Basic) e expõe os
três usos pedidos pelo dono (2026-08-05) + um método genérico para o que mais surgir:

  1) Localizar / enriquecer contato  — telefone/e-mail/endereço por CPF/CNPJ
     (alimenta o Motor Comercial: prospecção do lado vendedor / cedentes).
  2) Validar / qualificar CPF-CNPJ   — situação cadastral e dados básicos.
  3) Score / risco de crédito        — score e indicadores para qualificação.

Princípios do projeto:
  • Credencial é PODER (D106): NÃO vive no git. O cliente lê ASSERTIVA_CLIENT_ID /
    ASSERTIVA_CLIENT_SECRET do ambiente (GitHub Secret / painel). Nada hardcoded.
  • Fail-closed (1.3): sem credencial, não inventa; sem 200, devolve erro claro.
  • Custo consciente (1.4): `--probe` autentica APENAS (prova a rota e a credencial)
    e NÃO dispara consulta paga. As consultas de produto só rodam quando pedidas.
  • Extensível: `chamar(metodo, path, ...)` é a porta genérica p/ qualquer endpoint v3.

Respeita o CA do proxy quando existir (nunca desabilita verificação TLS).

Referência: doc oficial https://integracao.assertivasolucoes.com.br/v3/doc/
Os caminhos de PRODUTO abaixo seguem o padrão v3 documentado; os "leaf paths"
exatos (nomes de query/param por produto contratado) devem ser confirmados no
Swagger autenticado da conta — por isso o probe (auth) é o teste de conexão, e
cada produto é validado contra o Swagger vivo quando a credencial estiver setada.
"""
import base64
import json
import os
import ssl
import sys
import time
import urllib.parse
import urllib.request

# Host de API da Assertiva (produção). Token e produtos ficam sob /oauth2/v3 e /<produto>/v3.
BASE = os.environ.get("ASSERTIVA_BASE", "https://api.assertivasolucoes.com.br")
TOKEN_PATH = "/oauth2/v3/token"
UA = "PU-assertiva-conector/1.0"


def _ctx():
    for var in ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "CURL_CA_BUNDLE"):
        p = os.environ.get(var)
        if p and os.path.exists(p):
            return ssl.create_default_context(cafile=p)
    p = "/root/.ccr/ca-bundle.crt"
    if os.path.exists(p):
        return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


class AssertivaErro(Exception):
    pass


class AssertivaClient:
    def __init__(self, client_id=None, client_secret=None, base=BASE):
        self.client_id = client_id or os.environ.get("ASSERTIVA_CLIENT_ID")
        self.client_secret = client_secret or os.environ.get("ASSERTIVA_CLIENT_SECRET")
        if not self.client_id or not self.client_secret:
            raise AssertivaErro(
                "credencial ausente: defina ASSERTIVA_CLIENT_ID e ASSERTIVA_CLIENT_SECRET "
                "(GitHub Secret / painel) — não vão no git (D106)."
            )
        self.base = base.rstrip("/")
        self._tok = None
        self._tok_exp = 0

    # --- OAuth2 client_credentials (Basic base64(id:secret)) ---
    def token(self, forcar=False):
        agora = time.time()
        if self._tok and not forcar and agora < self._tok_exp - 60:
            return self._tok
        basic = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        body = urllib.parse.urlencode({"grant_type": "client_credentials"}).encode()
        req = urllib.request.Request(
            self.base + TOKEN_PATH, data=body, method="POST",
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
                "Accept": "application/json",
                "User-Agent": UA,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=40, context=_ctx()) as r:
                data = json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            detalhe = e.read().decode("utf-8", "replace")[:500]
            raise AssertivaErro(f"auth falhou: HTTP {e.code} {detalhe}")
        except Exception as e:
            raise AssertivaErro(f"auth falhou (rede/TLS): {e}")
        tok = data.get("access_token")
        if not tok:
            raise AssertivaErro(f"auth sem access_token no retorno: {data}")
        self._tok = tok
        self._tok_exp = agora + int(data.get("expires_in", 3600))
        return tok

    # --- porta genérica p/ qualquer endpoint v3 (extensível) ---
    def chamar(self, metodo, path, params=None, corpo=None):
        url = self.base + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        headers = {
            "Authorization": f"Bearer {self.token()}",
            "Accept": "application/json",
            "User-Agent": UA,
        }
        data = None
        if corpo is not None:
            data = json.dumps(corpo).encode()
            headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, method=metodo, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=60, context=_ctx()) as r:
                txt = r.read().decode("utf-8", "replace")
                return (json.loads(txt) if txt.strip().startswith(("{", "[")) else txt), r.status
        except urllib.error.HTTPError as e:
            return {"erro": e.read().decode("utf-8", "replace")[:800]}, e.code

    # --- 1) Localizar / enriquecer contato (Localize v3) ---
    def localizar(self, documento, tipo=None):
        """documento = CPF (11) ou CNPJ (14). tipo = 'CPF'|'CNPJ' (auto pelo tamanho)."""
        so_num = "".join(ch for ch in str(documento) if ch.isdigit())
        tipo = tipo or ("CNPJ" if len(so_num) == 14 else "CPF")
        return self.chamar("GET", "/localize/v3/localizar", params={"id": so_num, "tipo": tipo})

    # --- 2) Validar / qualificar CPF-CNPJ ---
    def validar_cpf(self, cpf):
        so_num = "".join(ch for ch in str(cpf) if ch.isdigit())
        return self.chamar("GET", f"/cpf/v3/situacao/{so_num}")

    def consultar_cnpj(self, cnpj):
        so_num = "".join(ch for ch in str(cnpj) if ch.isdigit())
        return self.chamar("GET", f"/cnpj/v3/situacao/{so_num}")

    # --- 3) Score / risco de crédito ---
    def score(self, cpf):
        so_num = "".join(ch for ch in str(cpf) if ch.isdigit())
        return self.chamar("GET", "/score/v3/pf", params={"cpf": so_num})


def _probe():
    """Prova credencial + rota SEM gastar consulta paga: só autentica."""
    try:
        c = AssertivaClient()
    except AssertivaErro as e:
        print(f"PROBE: BLOQUEADO — {e}")
        return 2
    try:
        tok = c.token()
        print(f"PROBE: OK — autenticou na Assertiva ({c.base}). "
              f"token_len={len(tok)} exp_em~{int(c._tok_exp - time.time())}s. "
              f"Rota confirmada; nenhuma consulta paga disparada.")
        return 0
    except AssertivaErro as e:
        print(f"PROBE: FALHOU — {e}")
        return 1


def main(argv):
    if not argv or argv[0] == "--probe":
        return _probe()
    cmd = argv[0]
    arg = argv[1] if len(argv) > 1 else None
    try:
        c = AssertivaClient()
    except AssertivaErro as e:
        print(f"BLOQUEADO — {e}")
        return 2
    fn = {
        "--localizar": lambda: c.localizar(arg),
        "--cpf": lambda: c.validar_cpf(arg),
        "--cnpj": lambda: c.consultar_cnpj(arg),
        "--score": lambda: c.score(arg),
    }.get(cmd)
    if not fn or arg is None:
        print("uso: assertiva_client.py [--probe | --localizar CPF/CNPJ | "
              "--cpf CPF | --cnpj CNPJ | --score CPF]")
        return 2
    res, st = fn()
    print(f"HTTP {st}")
    print(json.dumps(res, ensure_ascii=False, indent=2)[:4000])
    return 0 if st and st < 400 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

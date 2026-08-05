#!/usr/bin/env python3
"""
capturar_juris_portais.py — captura o INTEIRO TEOR da jurisprudência (metade-runner)
dos portais .gov.br que só respondem do Brasil, para rodar no runner `brasil`
(workflow capturar-br.yml). Fecha o item 3/7 da metade que NÃO precisa da extensão
do dono (STF + TJSP 2ª instância sem captcha).

Escopo (metade-runner):
  STF:  RE 226.942/SC, RE 387.047/SC   (jurisprudencia.stf.jus.br)
  TJSP: AI 2126162-35.2025, 2257458-20.2024, 2324382-13.2024  (esaj/cposg, 2º grau)

A metade que precisa do navegador do dono (STJ + TJSP 1º grau com captcha) NÃO entra
aqui — é capturada pela extensão (prompt entregue), fora deste script.

Princípios: extração PURA (1.2) — recorta o teor verbatim, sem interpretar. Cada caso
vira `jurisprudencia/<id>.md` (texto) + `.json` (metadados/citação, 1.7), no schema já
usado no corpus. Fail-closed (1.3): sem teor reconhecível, NADA é gravado (o caso fica
como pendente e é relatado); nunca inventa conteúdo.

Modos:
  --probe     : só testa alcance (HTTP 200) das fontes; não grava. (rota BR confirmada?)
  --capturar  : baixa e grava o que conseguir; relata sucesso/pendência caso a caso.
  (sem flag)  : equivale a --probe (seguro por padrão).

Dependências no runner: urllib (stdlib) + pypdf (PDF do STF). O workflow instala pypdf.
Respeita o CA do proxy quando existir (nunca desabilita verificação TLS).
"""
import json
import os
import re
import ssl
import sys
import time
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
JURIS = RAIZ / "jurisprudencia"
CAPTURAS = JURIS / "_capturas"

UA = "Mozilla/5.0 (X11; Linux x86_64) PU-runner-juris/1.0"

# --- Casos da metade-runner (id do corpus, fonte, identificadores) ---
CASOS = [
    {"id": "stf-re-226942-sc", "corte": "STF", "classe": "RE", "numero": "226942",
     "uf": "SC", "tema": ["solo_criado", "outorga_onerosa", "nao_e_tributo"]},
    {"id": "stf-re-387047-sc", "corte": "STF", "classe": "RE", "numero": "387047",
     "uf": "SC", "tema": ["solo_criado", "outorga_onerosa", "nao_e_tributo"]},
    {"id": "tjsp-ai-2126162-35-2025", "corte": "TJSP", "classe": "AI",
     "numero_cnj": "2126162-35.2025.8.26.0000", "tema": ["tdc", "tombamento", "potencial_construtivo"]},
    {"id": "tjsp-ai-2257458-20-2024", "corte": "TJSP", "classe": "AI",
     "numero_cnj": "2257458-20.2024.8.26.0000", "tema": ["tdc", "compensatoria", "penhora"]},
    {"id": "tjsp-ai-2324382-13-2024", "corte": "TJSP", "classe": "AI",
     "numero_cnj": "2324382-13.2024.8.26.0000", "tema": ["tdc", "potencial_construtivo"]},
]

FONTES_PROBE = [
    "https://jurisprudencia.stf.jus.br",
    "https://esaj.tjsp.jus.br/cposg/open.do",
    "https://scon.stj.jus.br/SCON/",
]


def _ctx():
    for var in ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "CURL_CA_BUNDLE"):
        p = os.environ.get(var)
        if p and Path(p).exists():
            return ssl.create_default_context(cafile=p)
    p = "/root/.ccr/ca-bundle.crt"
    if Path(p).exists():
        return ssl.create_default_context(cafile=p)
    return ssl.create_default_context()


def _get(url, timeout=40, binario=False):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=timeout, context=_ctx()) as r:
        dados = r.read()
        return dados if binario else dados.decode("utf-8", "replace"), r.status


def probe():
    print("=== PROBE — alcance das fontes (rota BR) ===")
    print("IP público:", end=" ")
    try:
        txt, _ = _get("https://api.ipify.org", timeout=15)
        print(txt.strip())
    except Exception as e:
        print("(falhou)", e)
    ok = 0
    for u in FONTES_PROBE:
        try:
            _, st = _get(u, timeout=30)
            print(f"  HTTP {st}  {u}")
            if st and st < 500:
                ok += 1
        except Exception as e:
            print(f"  FALHOU  {u}  ({e})")
    print(f"PROBE: {ok}/{len(FONTES_PROBE)} fontes responderam. "
          f"{'Rota BR OK — pode --capturar.' if ok else 'Rota BR não resolveu.'}")
    return ok


# --- STF: busca o acórdão e baixa o inteiro teor (PDF) ---
STF_API = ("https://jurisprudencia.stf.jus.br/api/search/search?"
           "base=acordaos&sinonimo=true&plural=true&page=1&pageSize=10&"
           "queryString={q}")


def captura_stf(caso):
    q = f"{caso['classe']}%20{caso['numero']}"
    try:
        txt, st = _get(STF_API.format(q=q), timeout=40)
        data = json.loads(txt)
        hits = (((data.get("result") or {}).get("hits") or {}).get("hits") or [])
        if not hits:
            return None, f"sem hit na busca STF para {caso['classe']} {caso['numero']}"
        src = hits[0].get("_source", {})
        # url do inteiro teor (campo varia; tenta os conhecidos)
        url_pdf = (src.get("inteiro_teor_url") or src.get("urlInteiroTeor")
                   or (src.get("documento") or {}).get("url"))
        ementa = src.get("ementa") or src.get("txtEmenta") or ""
        if not url_pdf:
            return None, "hit sem URL de inteiro teor (schema do STF mudou?)"
        pdf = _get(url_pdf, timeout=90, binario=True)
        CAPTURAS.mkdir(parents=True, exist_ok=True)
        raw = CAPTURAS / f"{caso['id']}.pdf"
        raw.write_bytes(pdf)
        texto = _pdf_texto(raw)
        if not texto or len(texto) < 500:
            return None, "PDF sem texto extraível (>=500 chars) — checar OCR"
        return {"texto": texto, "ementa": ementa, "fonte": url_pdf}, None
    except Exception as e:
        return None, f"erro STF: {e}"


def _pdf_texto(path):
    try:
        from pypdf import PdfReader
    except Exception:
        return None
    try:
        r = PdfReader(str(path))
        return "\n".join((p.extract_text() or "") for p in r.pages).strip()
    except Exception:
        return None


# --- TJSP: cposg (2º grau) — busca por número CNJ e recorta o teor/ementa ---
TJSP_BUSCA = ("https://esaj.tjsp.jus.br/cposg/search.do?conversationId=&"
              "cbPesquisa=NUMPROC&numeroDigitoAnoUnificado={dda}&"
              "foroNumeroUnificado=0000&dePesquisaNuUnificado={cnj}&"
              "dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO")


def captura_tjsp(caso):
    cnj = caso["numero_cnj"]
    m = re.match(r"(\d{7}-\d{2}\.\d{4})", cnj)
    dda = m.group(1) if m else cnj[:14]
    try:
        html, st = _get(TJSP_BUSCA.format(dda=dda, cnj=cnj), timeout=60)
        # ementa / trecho do julgado no cposg
        ementa = _recorta(html, r'Ementa[:\s]*</?[^>]*>?(.{80,4000}?)<', flags=re.I | re.S)
        classe_relator = _recorta(html, r'Relator[^<]*</[^>]*>\s*<[^>]*>([^<]{3,120})', flags=re.I)
        texto = re.sub(r"<[^>]+>", " ", html)
        texto = re.sub(r"\s+", " ", texto).strip()
        if "não encontrado" in texto.lower() or len(texto) < 800:
            return None, "cposg sem resultado utilizável (captcha? número? 2º grau?)"
        return {"texto": texto[:20000], "ementa": (ementa or "").strip(),
                "relator": (classe_relator or "").strip(),
                "fonte": TJSP_BUSCA.format(dda=dda, cnj=cnj)}, None
    except Exception as e:
        return None, f"erro TJSP: {e}"


def _recorta(html, pat, flags=0):
    m = re.search(pat, html, flags)
    return m.group(1).strip() if m else None


def _grava(caso, res):
    JURIS.mkdir(parents=True, exist_ok=True)
    md = JURIS / f"{caso['id']}.md"
    js = JURIS / f"{caso['id']}.json"
    cab = f"# {caso['corte']} {caso.get('classe','')} {caso.get('numero') or caso.get('numero_cnj','')}\n\n"
    md.write_text(cab + "## Inteiro teor (verbatim)\n\n" + res["texto"] + "\n", encoding="utf-8")
    meta = {
        "id": caso["id"], "tipo_norma": "jurisprudencia", "corte": caso["corte"],
        "classe": caso.get("classe"), "numero": caso.get("numero") or caso.get("numero_cnj"),
        "tema": caso.get("tema", []), "ementa": res.get("ementa", ""),
        "relator": res.get("relator", ""),
        "fonte": {"origem": f"portal {caso['corte']} (runner brasil)", "url": res.get("fonte"),
                  "metodo": "captura runner-half (inteiro teor), extração pura 1.2", "ocr": False},
        "status_pipeline": "bruto", "revisado_por_humano": False,
    }
    js.write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")


def capturar():
    ok, pend = [], []
    for caso in CASOS:
        fn = captura_stf if caso["corte"] == "STF" else captura_tjsp
        res, err = fn(caso)
        if res:
            _grava(caso, res)
            ok.append(caso["id"])
            print(f"  OK   {caso['id']} (teor {len(res['texto'])} chars)")
        else:
            pend.append((caso["id"], err))
            print(f"  PEND {caso['id']}: {err}")
        time.sleep(2)
    print(f"\nRESUMO: {len(ok)} capturados, {len(pend)} pendentes.")
    if pend:
        print("Pendentes (fail-closed — nada inventado):")
        for cid, err in pend:
            print(f"  - {cid}: {err}")
    return 0 if ok else 1


def main(argv):
    if "--capturar" in argv:
        if not probe():
            print("Rota BR não resolveu — abortando captura (fail-closed).")
            return 2
        return capturar()
    return 0 if probe() else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

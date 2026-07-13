#!/usr/bin/env python3
"""
vistoria_conteudo_sa.py — VISTORIA DE PROVENIÊNCIA POR CONTEÚDO (sem atalho) do Drive PU.
ABRE cada arquivo (conta de serviço), EXTRAI o texto REAL e classifica pela EVIDÊNCIA DO CONTEÚDO —
nunca por nome/pasta/tag. Classe ∈ {OFICIAL, NAO_OFICIAL_EXTERNO, CRIADO, ILEGIVEL, PENDENTE}.
Grava, por arquivo, o TRECHO literal que decidiu (prova de que abriu). PU 19 · 2026-07-13.

Regra de ouro (MOU): nenhuma classe sem conteúdo inspecionado + evidência. "Não consegui ler" = ILEGIVEL
(estado explícito), nunca palpite. A automação escala o esforço de ABRIR; não substitui o olhar.

Como abre cada tipo (o conteúdo, não a borda):
  PDF nativo   → pypdf 1ª+última página + metadados; se <120 chars ⇒ OCR pág.1
  PDF/imagem escaneada → pdf2image+tesseract-por (OCR pág.1)
  .md/.txt/.csv/.json → baixa só os 1ºs 256 KB (Range) e lê
  .xlsx        → openpyxl read_only, cabeçalho + 20 linhas
  .dbf (shape) → schema dos campos
  GIGANTES (csv/txt) → Range bytes=0-262143 (cabeçalho+amostra = a identidade do arquivo)
  Google-nativo → export text/plain (trunca)
Grava sha256 do que leu (custódia). Idempotente (pula quem já está no CSV de saída). Shardável.

Env: GOOGLE_SA_KEY (obrig) · GEMINI_API_KEY (opcional, resolve AMBIGUO) · NSHARDS · SHARD · LIMIT · OUT
"""
import os
import re
import sys
import csv
import json
import time
import hashlib
import io
import subprocess
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CATALOGO = RAIZ / "inventario" / "CATALOGO-DRIVE-PU-2026-07-12.csv"
NSHARDS = int(os.environ.get("NSHARDS", "1"))
SHARD = int(os.environ.get("SHARD", "0"))
LIMIT = int(os.environ.get("LIMIT", "0"))            # 0 = sem limite
OUT = Path(os.environ.get("OUT", str(RAIZ / "inventario" / "drive-pu" / f"PROVENIENCIA-shard{SHARD}.csv")))
HEAD_BYTES = 262144                                  # 256 KB p/ texto/csv/gigantes
COLS = ["drive_id", "nome", "mime", "ext", "bytes", "classe", "comercial", "metodo",
        "confianca", "evidencia_conteudo", "sha256_lido", "n_chars", "path_contexto"]

# ---- marcas de CONTEÚDO (atuam sobre o TEXTO extraído, nunca sobre o nome) ----
RX_OFICIAL = re.compile(r"(di[áa]rio\s+oficial|imprensa\s+oficial|prefeitura\s+do\s+munic[íi]pio\s+de\s+s[ãa]o\s+paulo|"
                        r"c[âa]mara\s+municipal\s+de\s+s[ãa]o\s+paulo|este\s+texto\s+n[ãa]o\s+substitui\s+o\s+publicado|"
                        r"secretaria\s+municipal|gabinete\s+do\s+prefeito|catálogo\s+de\s+legisla[çc][ãa]o\s+municipal)", re.I)
RX_NORMA = re.compile(r"\b(lei|decreto|portaria|resolu[çc][ãa]o|instru[çc][ãa]o\s+normativa|delibera[çc][ãa]o)\b"
                      r".{0,40}\bn[º°o]?\s*[\d.]{3,}", re.I)
RX_ARTICULADO = re.compile(r"\bart(?:igo)?\.?\s*1[\s.ºo]", re.I)
RX_CRIADO = re.compile(r"(texto\s+integral\s*\(verbatim\)|\*\*proveni[êe]ncia|oraculo_|conhecimento_mestre|"
                       r"log_extracao|deep_scan|estrutura_silver|_chunk\b|gerado\s+(por|pelo)\s+motor|"
                       r"pipeline\s+potencial\s+urbano|## +metadados|\"chunk_id\"|\"drive_id\":)", re.I)
# CRIADO por ENRIQUECIMENTO nosso — marcas no CONTEÚDO (colunas derivadas/nomes de etapa nossa):
RX_CRIADO_ENR = re.compile(r"(enriquecid|blindad|asset_light|\bdossie\b|sql_unificad|sql_key|bp_proipha|bp_obscomp|"
                           r"lista\s*prospec|prospec[çc][ãa]o\s+ativa|_final_v\d|\btiers\b|potencialurbano|"
                           r"amostralista|base_tdc_)", re.I)
RX_COMERCIAL_HDR = re.compile(r"\b(cnpj|raz[ãa]o\s+social|s[óo]cio|qsa|quadro\s+societ[áa]rio|contribuinte|"
                              r"inscri[çc][ãa]o\s+imobili[áa]ria|numero_contribuinte|sql\b|testada|"
                              r"valor\s+venal|cep\b|logradouro|proprietari|itbi)", re.I)
RX_GOV_CADASTRO = re.compile(r"(iptu|itbi|valor\s+venal|inscri[çc][ãa]o\s+imobili[áa]ria|sirgas|geosampa|setor\s+fiscal)", re.I)
# FONTE governamental (produtor público, qualquer esfera) — decide OFICIAL por si:
RX_GOV_FONTE = re.compile(r"(geosampa|sirgas|\bsvma\b|geoportal|secretaria\s+municipal|prefeitura\s+(do\s+munic[íi]pio|municipal)|"
                          r"c[âa]mara\s+municipal|dados\s+abertos|receita\s+federal|imprensa\s+oficial|di[áa]rio\s+oficial|"
                          r"minist[ée]rio\s+p[úu]blico|tribunal\s+de\s+justi[çc]a|conpresp|iphan|condephaat)", re.I)


def _drive():
    raw = os.environ.get("GOOGLE_SA_KEY", "").strip()
    if not raw:
        print("ERRO: GOOGLE_SA_KEY ausente.", file=sys.stderr); sys.exit(2)
    info = json.loads(raw)
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/drive.readonly"])
    print(f"autenticado: {info.get('client_email')}")
    return build("drive", "v3", credentials=creds, cache_discovery=False)


def baixar(drive, fid, mime, nbytes, so_cabecalho):
    """Baixa bytes do arquivo. so_cabecalho ⇒ Range dos 1ºs 256 KB (gigantes/texto). Google-nativo ⇒ export."""
    if mime and mime.startswith("application/vnd.google-apps"):
        exp = {"application/vnd.google-apps.document": "text/plain",
               "application/vnd.google-apps.spreadsheet": "text/csv",
               "application/vnd.google-apps.presentation": "text/plain"}.get(mime, "text/plain")
        try:
            data = drive.files().export(fileId=fid, mimeType=exp).execute()
            return data if isinstance(data, bytes) else str(data).encode("utf-8", "ignore")
        except Exception:
            return b""
    req = drive.files().get_media(fileId=fid, supportsAllDrives=True)
    # Range dos 1ºs bytes p/ arquivos grandes/texto — ler cabeçalho+amostra é ler o documento, não atalho.
    from googleapiclient.http import MediaIoBaseDownload
    buf = io.BytesIO()
    dl = MediaIoBaseDownload(buf, req, chunksize=HEAD_BYTES)
    done = False; passos = 0
    while not done:
        _, done = dl.next_chunk()
        passos += 1
        if so_cabecalho or passos * HEAD_BYTES >= max(HEAD_BYTES, 4 * 1024 * 1024):
            break                      # cabeçalho (texto) ou teto 4 MB (PDF/xlsx) — nunca o corpo inteiro dos gigantes
    return buf.getvalue()


def extrair_texto(nome, ext, mime, data):
    """Devolve (texto, metodo). Abre o CONTEÚDO real conforme o tipo."""
    ext = (ext or "").lower()
    if not data:
        return "", "vazio"
    # texto direto
    if ext in ("md", "txt", "csv", "json", "tsv", "geojson", "xml", "html", "prj", "cpg") or (mime or "").startswith("text"):
        try:
            return data[:HEAD_BYTES].decode("utf-8", "ignore"), "texto_nativo"
        except Exception:
            return data[:HEAD_BYTES].decode("latin-1", "ignore"), "texto_nativo"
    # PDF
    if ext == "pdf" or (mime == "application/pdf"):
        txt = ""
        try:
            from pypdf import PdfReader
            r = PdfReader(io.BytesIO(data))
            meta = " ".join(str(v) for v in (r.metadata or {}).values())
            paginas = r.pages
            alvo = [paginas[0]] + ([paginas[-1]] if len(paginas) > 1 else [])
            txt = meta + "\n" + "\n".join((p.extract_text() or "") for p in alvo)
        except Exception:
            txt = ""
        if len(txt.strip()) >= 120:
            return txt, "pdf_nativo"
        # escaneado → OCR pág.1
        try:
            from pdf2image import convert_from_bytes
            import pytesseract
            imgs = convert_from_bytes(data, dpi=110, first_page=1, last_page=1)
            ocr = pytesseract.image_to_string(imgs[0], lang="por") if imgs else ""
            return (ocr, "ocr_pdf") if ocr.strip() else ("", "sem_texto")
        except Exception:
            return (txt, "pdf_nativo") if txt.strip() else ("", "sem_texto")
    # imagem
    if ext in ("png", "jpg", "jpeg", "tif", "tiff", "bmp", "gif") or (mime or "").startswith("image"):
        try:
            from PIL import Image
            import pytesseract
            ocr = pytesseract.image_to_string(Image.open(io.BytesIO(data)), lang="por")
            return (ocr, "ocr_imagem") if ocr.strip() else ("", "sem_texto")
        except Exception:
            return "", "sem_texto"
    # planilha xlsx/ods
    if ext in ("xlsx", "xlsm", "ods"):
        try:
            import openpyxl
            wb = openpyxl.load_workbook(io.BytesIO(data), read_only=True, data_only=True)
            ws = wb.active
            linhas = []
            for i, row in enumerate(ws.iter_rows(values_only=True)):
                linhas.append(" | ".join("" if c is None else str(c) for c in row))
                if i >= 20:
                    break
            return "\n".join(linhas), "planilha"
        except Exception:
            return "", "sem_texto"
    # shapefile dbf
    if ext == "dbf":
        try:
            from dbfread import DBF
            tmp = io.BytesIO(data)
            # dbfread precisa de path; escreve tmp
            p = RAIZ / f"_tmp_{hashlib.md5(nome.encode()).hexdigest()[:8]}.dbf"
            p.write_bytes(data)
            try:
                t = DBF(str(p), load=False)
                campos = ", ".join(f.name for f in t.fields)
            finally:
                p.unlink(missing_ok=True)
            return f"SHAPEFILE DBF campos: {campos}", "shape_schema"
        except Exception:
            # fallback: nomes de campo estão em ASCII no cabeçalho do .dbf
            try:
                head = data[:2048].decode("latin-1", "ignore")
                return f"DBF header: {head}", "shape_header"
            except Exception:
                return "", "sem_texto"
    # desconhecido: tenta como texto
    try:
        t = data[:HEAD_BYTES].decode("utf-8", "ignore")
        return (t, "bytes_texto") if len(t.strip()) > 20 else ("", "sem_texto")
    except Exception:
        return "", "sem_texto"


def classificar(texto, metodo):
    """Classe pela EVIDÊNCIA no texto. Devolve (classe, comercial, confianca, evidencia, ambiguo)."""
    t = texto or ""
    def trecho(rx):
        m = rx.search(t)
        return t[max(0, m.start()-40):m.end()+60].replace("\n", " ").strip() if m else ""
    if not t.strip():
        return "ILEGIVEL", "nao", "alta", f"(sem texto extraível — metodo={metodo})", False
    # 1) CRIADO por nós — cabeçalho de pipeline OU marcas de enriquecimento nosso no conteúdo (vem 1º:
    #    um arquivo que NÓS enriquecemos é CRIADO mesmo que contenha colunas cadastrais/oficiais).
    if RX_CRIADO.search(t):
        return "CRIADO", "nao", "alta", "CRIADO(pipeline): " + trecho(RX_CRIADO), False
    if RX_CRIADO_ENR.search(t):
        return "CRIADO", "nao", "media", "CRIADO(enriquecido por nós): " + trecho(RX_CRIADO_ENR), False
    # 2) OFICIAL: masthead/emissor, fonte governamental, OU norma articulada
    if RX_OFICIAL.search(t):
        return "OFICIAL", ("sim" if RX_GOV_CADASTRO.search(t) else "nao"), "alta", "OFICIAL(masthead): " + trecho(RX_OFICIAL), False
    if RX_GOV_FONTE.search(t):
        return "OFICIAL", ("sim" if (RX_GOV_CADASTRO.search(t) or RX_COMERCIAL_HDR.search(t)) else "nao"), "media", "OFICIAL(fonte gov): " + trecho(RX_GOV_FONTE), False
    if RX_NORMA.search(t) and RX_ARTICULADO.search(t):
        return "OFICIAL", "nao", "media", "OFICIAL(norma articulada): " + trecho(RX_NORMA), False
    # 3) COMERCIAL: cabeçalho de dado de proprietário (externo, não-nosso e não-gov)
    if RX_COMERCIAL_HDR.search(t):
        gov = bool(RX_GOV_CADASTRO.search(t))
        return ("OFICIAL" if gov else "NAO_OFICIAL_EXTERNO"), "sim", "media", "COMERCIAL/dado-proprietario: " + trecho(RX_COMERCIAL_HDR), False
    # 4) tem texto mas sem marca decisiva → AMBIGUO (vai p/ leitura LLM)
    return "PENDENTE", "nao", "baixa", "AMBIGUO: " + t.strip().replace("\n", " ")[:180], True


def classificar_llm(nome, texto):
    """Resolve AMBIGUO lendo a amostra com Gemini (se GEMINI_API_KEY). Devolve (classe,comercial,evidencia) ou None."""
    key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not key or not texto.strip():
        return None
    prompt = (
        "Você é perito em PROVENIÊNCIA documental de um projeto jurídico (TDC/IPTU em São Paulo). Decida a classe "
        "deste documento PELO CONTEÚDO abaixo (não pelo nome). As três classes e o teste de cada uma:\n"
        "• OFICIAL — produzido/publicado por órgão público (Diário Oficial, Prefeitura, Câmara, GeoSampa/SIRGAS, "
        "Receita Federal, tribunais). Marca do EMISSOR no texto. Inclui norma articulada e base cadastral pública.\n"
        "• NAO_OFICIAL_EXTERNO — texto/base de TERCEIRO, em formato nativo, SEM selo oficial e SEM sinais de ter sido "
        "gerado por nós (apostila, PDF de escritório, base comprada de terceiro). É a única classe 'externa' usável.\n"
        "• CRIADO — gerado/transformado pelo NOSSO pipeline de IA: resumo, análise, chunk, planilha enriquecida/cruzada "
        "por nós, prosa sintetizada no lugar do articulado literal, colunas derivadas (chaves unificadas, flags nossas). "
        "Na dúvida entre 'cópia externa de um oficial' e 'derivado nosso', pergunte: o TEXTO é o original como emitido, "
        "ou foi RE-TRABALHADO (colunas novas, síntese, enriquecimento)? Re-trabalhado = CRIADO.\n"
        "Responda SÓ um JSON: {\"classe\":\"OFICIAL|NAO_OFICIAL_EXTERNO|CRIADO\",\"comercial\":\"sim|nao\" "
        "(sim se serve para ACHAR O PROPRIETÁRIO: cadastro IPTU, sócios, CNPJ, ITBI, lote/SQL),"
        "\"confianca\":\"alta|media|baixa\",\"motivo\":\"<=18 palavras citando a marca do texto que decidiu\"}.\n\n"
        f"NOME(contexto, NÃO decisivo): {nome}\nCONTEÚDO EXTRAÍDO:\n{texto[:6000]}")
    import urllib.request
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}],
                       "generationConfig": {"temperature": 0}}).encode()
    # INTELIGÊNCIA onde decide (steer do MOU): modelo FORTE 1º na fração ambígua; flash só de reserva.
    modelos = [os.environ.get("GEMINI_MODEL", "gemini-2.5-pro"), "gemini-2.0-flash", "gemini-flash-latest"]
    for modelo in modelos:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={key}"
        try:
            req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as r:
                out = json.loads(r.read())
            txt = out["candidates"][0]["content"]["parts"][0]["text"]
            m = re.search(r"\{.*\}", txt, re.S)
            j = json.loads(m.group(0))
            cl = j.get("classe", "").upper()
            if cl not in ("OFICIAL", "NAO_OFICIAL_EXTERNO", "CRIADO"):
                return None
            conf = str(j.get("confianca", "media")).lower()
            conf = conf if conf in ("alta", "media", "baixa") else "media"
            return (cl, ("sim" if str(j.get("comercial", "")).lower().startswith("s") else "nao"),
                    f"LLM({modelo.split('-')[1]},{conf}): " + str(j.get("motivo", ""))[:120], conf)
        except Exception as e:
            classificar_llm._erros = getattr(classificar_llm, "_erros", 0) + 1
            if classificar_llm._erros <= 3:
                detalhe = ""
                try:
                    detalhe = e.read().decode()[:200]
                except Exception:
                    detalhe = str(e)[:200]
                print(f"  [gemini {modelo}] erro: {detalhe}", file=sys.stderr)
            continue
    return None


def _git_checkpoint():
    """Commita+push o CSV do shard PARCIAL (a cada N arquivos) para não perder o trabalho se o job for
    cortado (cancelamento de 90min). Só roda se GIT_CHECKPOINT=1. Rebase-retry (shards distintos = sem conflito)."""
    if os.environ.get("GIT_CHECKPOINT", "").strip() != "1":
        return
    branch = os.environ.get("BRANCH", "").strip()
    if not branch:
        return
    def run(*a):
        return subprocess.run(a, cwd=str(RAIZ), capture_output=True, text=True)
    run("git", "config", "user.name", "vistoria-bot")
    run("git", "config", "user.email", "contato@bitsuki.com.br")
    run("git", "add", str(OUT))
    if run("git", "diff", "--cached", "--quiet").returncode == 0:
        return                                   # nada novo a gravar
    run("git", "commit", "-q", "-m", f"Vistoria: checkpoint shard {SHARD} (parcial)")
    for i in range(5):
        run("git", "pull", "--rebase", "-X", "ours", "origin", branch)
        if run("git", "push", "origin", f"HEAD:{branch}").returncode == 0:
            print(f"  [checkpoint] shard {SHARD} salvo no git", flush=True)
            return
        time.sleep(3 * (i + 1))
    print(f"  [checkpoint] push falhou (segue local; próximo checkpoint tenta de novo)", flush=True)


def carregar_fila():
    fila = []
    with open(CATALOGO, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            did = (row.get("drive_id") or "").strip()
            if not did:
                continue
            if NSHARDS > 1:
                h = int(hashlib.md5(did.encode()).hexdigest(), 16)
                if h % NSHARDS != SHARD:
                    continue
            fila.append(row)
    # dedup por id
    vis, out = set(), []
    for r in fila:
        d = r["drive_id"].strip()
        if d not in vis:
            vis.add(d); out.append(r)
    return out


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    feitos = set()
    if OUT.exists():
        with open(OUT, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                feitos.add((row.get("drive_id") or "").strip())
    fila = [r for r in carregar_fila() if r["drive_id"].strip() not in feitos]
    if LIMIT:
        fila = fila[:LIMIT]
    print(f"=== VISTORIA CONTEÚDO — shard {SHARD}/{NSHARDS} — {len(fila)} a abrir (já feitos: {len(feitos)}) ===")
    drive = _drive()
    novo = not OUT.exists()
    fh = open(OUT, "a", encoding="utf-8", newline="")
    w = csv.DictWriter(fh, fieldnames=COLS)
    if novo:
        w.writeheader()
    from collections import Counter
    cont = Counter(); llm_ok = 0; n = 0
    for row in fila:
        did = row["drive_id"].strip(); nome = (row.get("nome") or "").strip()
        mime = (row.get("mime") or "").strip(); ext = (row.get("ext") or "").strip()
        try:
            nbytes = int(row.get("bytes") or 0)
        except Exception:
            nbytes = 0
        so_cab = ext.lower() in ("csv", "txt", "md", "json", "tsv", "geojson", "xml") or nbytes > 8 * 1024 * 1024
        try:
            data = baixar(drive, did, mime, nbytes, so_cab)
            texto, metodo = extrair_texto(nome, ext, mime, data)
            sha = hashlib.sha256(data).hexdigest()[:16] if data else ""
            classe, comercial, conf, evid, ambiguo = classificar(texto, metodo)
            if ambiguo:
                r = classificar_llm(nome, texto)
                if r:
                    classe, comercial, evid, conf = r; metodo += "+llm"; llm_ok += 1
                    # baixa confiança do modelo forte = fração que EU (orquestrador) reviso depois (filtra confianca=baixa)
            w.writerow({"drive_id": did, "nome": nome, "mime": mime, "ext": ext, "bytes": nbytes,
                        "classe": classe, "comercial": comercial, "metodo": metodo, "confianca": conf,
                        "evidencia_conteudo": evid[:300], "sha256_lido": sha, "n_chars": len(texto or ""),
                        "path_contexto": (row.get("path") or "")[:120]})
            cont[classe] += 1
        except Exception as e:
            w.writerow({"drive_id": did, "nome": nome, "mime": mime, "ext": ext, "bytes": nbytes,
                        "classe": "ILEGIVEL", "comercial": "nao", "metodo": "erro", "confianca": "alta",
                        "evidencia_conteudo": f"(erro ao abrir: {type(e).__name__}: {str(e)[:120]})",
                        "sha256_lido": "", "n_chars": 0, "path_contexto": (row.get("path") or "")[:120]})
            cont["ILEGIVEL"] += 1
        n += 1
        if n % 100 == 0:
            fh.flush()
            print(f"  ... {n}/{len(fila)}  {dict(cont)}  llm={llm_ok}", flush=True)
        if n % 300 == 0:                          # CHECKPOINT: grava o parcial no git (anti-perda em corte)
            fh.flush(); os.fsync(fh.fileno()); fh.close()
            _git_checkpoint()
            fh = open(OUT, "a", encoding="utf-8", newline="")
            w = csv.DictWriter(fh, fieldnames=COLS)
    fh.close()
    _git_checkpoint()
    print(f"=== FIM shard {SHARD} === abertos={n}  classes={dict(cont)}  llm_resolvidos={llm_ok}  saida={OUT.name}")


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""
fatiar.py — Chunking ESTRUTURAL de uma norma verbatim, por dispositivo (CLAUDE.md 2.5).

Princípios atendidos:
- 2.5: a unidade atômica é o dispositivo (Título→Capítulo→Seção→Artigo→…). Nunca corta
  por tamanho fixo. Cada chunk carrega o caminho hierárquico e o id da lei.
- 1.7: cada chunk leva a citação (lei, dispositivo, fonte, vigência) — pré-requisito do RAG.
- 1.2: extração PURA. Este script NÃO interpreta, NÃO resume, NÃO usa LLM: só recorta o
  verbatim em pedaços rastreáveis. Número nasce no engine, não aqui (1.3).
- ZERO-COMPRESSÃO / nada se descarta: o preâmbulo (texto antes do 1º artigo) vira chunk próprio;
  as assinaturas/fecho ficam coladas ao chunk do ÚLTIMO artigo (fidelidade > granularidade — não
  se cria um chunk 'fecho' separado). Nada do corpo verbatim é jogado fora.

GUARDA DE VERBATIM: só fatia .md que tenha o cabeçalho `## Texto integral (verbatim)` e
cujo .json par esteja com `confianca_extracao: alta`. Resumo não-verbatim NÃO entra no RAG
(citaria síntese, não dispositivo — violaria 1.7). Itens recusados são reportados, não fatiados.

Uso:
    python3 scripts/fatiar.py                 # fatia todas as leis verbatim elegíveis
    python3 scripts/fatiar.py leis/municipal-sp/lei-municipal-saopaulo-7228-1968.md

Escreve: rag/chunks/<lei_id>/<seq>__<rotulo>.json  (um arquivo por dispositivo)
         e atualiza o status_pipeline do .json da lei para "fatiado".

Trazido pela instância orquestradora do Potencial Urbano — 2026-06-20.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MARCADOR_VERBATIM = "## Texto integral (verbatim)"

# Regex de dispositivos (início de linha). Aceita "Art. 1º", "Art 1o", "Art. 10 -", "Art. 156-A".
# CAPTURA o sufixo -A/-B (achado A2-02/B-11): "Art. 156-A" é dispositivo DISTINTO de "Art. 156";
# rotulá-lo "Art. 156" cita dispositivo inexistente (viola 1.7).
# A-04 (auditoria 2026-07-05): NÃO incluir 'o/O' na classe do marcador ordinal — num artigo cardinal
# cujo corpo começa com "O"/"Os" ("Art. 54 Os sindicatos…") o 'O' era engolido e a linha caía como
# remissão (corpo em minúscula), fundindo o Art. 54 no 53 e citando o dispositivo ERRADO (viola 1.7).
# O ordinal real vem como 'º'/'°'; "1o/9o" ainda é coberto pelo rótulo (grupo é só o dígito).
RE_ARTIGO = re.compile(r"^\s*Art\.?\s*(\d+(?:-[A-Z])?)\s*[º°.\-–]?", re.IGNORECASE)
RE_TITULO = re.compile(r"^\s*T[ÍI]TULO\s+([IVXLCDM]+|\d+)\b", re.IGNORECASE)
RE_CAPITULO = re.compile(r"^\s*CAP[ÍI]TULO\s+([IVXLCDM]+|\d+)\b", re.IGNORECASE)
RE_SECAO = re.compile(r"^\s*SE[ÇC][ÃA]O\s+([IVXLCDM]+|\d+)\b", re.IGNORECASE)


# B-11c — VIGÊNCIA POR CHUNK (1.6): em texto CONSOLIDADO, um dispositivo pode estar REVOGADO
# ("(Revogado pela Lei ...)") ou carregar redação ALTERADA ("Redação dada pela Lei ..."). Sem marcar
# isso, o RAG devolve redação revogada como vigente (defeito real: PDE 16.050 Art. 148/52, revogados
# pela Lei 17.975/2023, vinham no TOPO da consulta). Aqui a marcação é DETERMINÍSTICA e por chunk.
# Revogação INTEGRAL do dispositivo: parentética "(Revogado ...)" OU "Revogado pel[oa] Lei/Decreto".
# NÃO confundir com a cláusula de ENCERRAMENTO "Revogadas as disposições em contrário, esta Lei
# entrará em vigor..." (art. final que revoga OUTRAS normas e PROMULGA esta — não é o artigo revogado).
RE_REVOGADO_INICIO = re.compile(r"^\(\s*Revogad[oa]|^Revogad[oa]s?\s+pel[oa]s?\b", re.IGNORECASE)
RE_REVOGADO_FONTE = re.compile(r"Revogad[oa]s?\s+(?:pel[oa]s?\s+)?"
                               r"(Lei[^)\n]*|Decreto[^)\n]*|EC[^)\n]*)", re.IGNORECASE)
RE_REDACAO_DADA = re.compile(r"Reda[çc][ãa]o dada", re.IGNORECASE)
# AUD-C05 — Extrai a norma alteradora e o ANO da redação nova. Cobre os formatos reais do corpus:
# "Lei nº 17.975/2023", "Lei nº 10.931, de 2004", "Lei 10.931, de 2004" (sem nº),
# "Lei nº 4.864, de 29.11.1965", "Lei nº 13.144 de 2015" (sem vírgula),
# "Decreto nº 57.665/2017", "Medida Provisória nº 1.085, de 2021",
# "Lei Complementar nº 214, de 2025", "Pela Medida Provisória nº 1.085, de 2021",
# "Lei nº 13.275, de 4 de janeiro de 2002" (data completa com mês por extenso),
# "pelo art. 1º do Decreto nº 21.928, de 10 de outubro de 1932" (via artigo).
RE_REDACAO_DADA_FONTE = re.compile(
    r"[Rr]eda[çc][ãa]o\s+dada\s+"
    r"(?:[Pp]el[oa]s?\s+(?:art\.?\s*\d+[ºo°]?\s*(?:d[oa]s?\s+|dest[ae]\s+))?)?"
    r"((?:Lei(?:\s+Complementar)?|Decreto(?:-Lei)?|Emenda\s+Constitucional|EC"
    r"|Medida\s+Prov[ió]s[oó]ria)"
    r"(?:\s+n[ºo°]\s*|\s+)[\d.]+"
    r"(?:/\d{4}"
    r"|,?\s+de\s+\d{1,2}\s+de\s+\w+\s+de\s+\d{4}"
    r"|,?\s+de\s+[\d.]+(?:\.\d+)*)?"
    r")",
    re.IGNORECASE)
# Extrai o ano de 4 dígitos da referência da norma alteradora.
# Aceita ano no final da string, antes de ), ou após / , . ou espaço.
RE_ANO_4D = re.compile(r"[/,. ](\d{4})(?:\s*$|\))")
RE_ROTULO_PREFIXO = re.compile(r"^\s*Art\.?\s*\d+(?:-[A-Z])?\s*[ºoO°.\-–]?\s*")

# C-28 / T1 — REMISSÃO line-initial NÃO é cabeçalho de artigo. Uma linha pode ABRIR com "art. N ..."
# sendo uma REMISSÃO a outro dispositivo DENTRO do corpo do artigo corrente (a frase quebrou de linha),
# não a abertura do Art. N. Defeito real: a fórmula central `PCpt = Atc × CAbas × Fi` mora numa linha
# "art. 124 desta lei, o potencial construtivo..." que é o CORPO do Art. 125 (a frase "...previstos nos
# incisos do\nart. 124 desta lei..." quebrou) — o chunker abria um chunk falso "Art. 124", citando o
# dispositivo ERRADO na consulta mais importante (viola 1.7). Idem "art. 126 desta lei" (corpo do Art. 127).
# DISCRIMINADOR (proibido usar monotonicidade de número — falso-positivo em lei alteradora tipo EC-132
# Art. 2º após Art. 156-B; falso-negativo em remissão para número maior): um cabeçalho REAL, após "Art. N"
# (+ ordinal/sep), inicia a norma com MAIÚSCULA/dígito OU é a linha inteira; uma REMISSÃO tem, logo após o
# número, um conectivo de remissão ("desta/da Lei", "e seguintes", "c/c", "§") OU vírgula OU continuação
# em minúscula (corpo de artigo em redação BR sempre começa maiúsculo após "Art. N.").
RE_CONECTIVO_REMISSAO = re.compile(
    r"^(?:,|;|desta\b|deste\b|dessa\b|desse\b|da\s+lei\b|das\s+leis\b|do\s+decreto\b|dos\s+decretos\b|"
    r"e\s+seguintes\b|e\s+ss\.?|c/c\b|§|inc\b|incisos?\b|al[ií]neas?\b)",
    re.IGNORECASE)


def eh_remissao_line_initial(ln: str, ma: "re.Match") -> bool:
    """True se a linha, embora comece com 'Art. N', é uma REMISSÃO (corpo do artigo corrente),
    não a abertura de um novo artigo. `ma` é o match de RE_ARTIGO já calculado (evita recomputar).
    A-04: `resto` deriva do FIM DO NÚMERO (não de ma.end()), p/ o marcador ordinal opcional nunca
    consumir a 1ª letra do corpo — senão 'Art. 54 Os…' perde o 'O' e vira falso-remissão."""
    resto = ln[ma.start(1) + len(ma.group(1)):].lstrip(" º°.\t")
    if not resto:
        return False                      # "Art. N" sozinho: cabeçalho legítimo (corpo vem nas próximas linhas)
    if RE_CONECTIVO_REMISSAO.match(resto):
        return True                        # conectivo de remissão logo após o número
    if resto[:1].islower():
        return True                        # continuação em minúscula: corpo de artigo real inicia MAIÚSCULO
    return False


def vigencia_dispositivo(texto: str) -> dict:
    """Classifica a vigência de UM dispositivo pelo seu próprio texto verbatim (B-11c, 1.6):
    - 'revogado'  : o artigo ABRE com '(Revogado ...)' — revogação INTEGRAL do dispositivo;
    - 'compilado' : contém 'Redação dada por ...' — redação vigente ALTERADA por norma posterior;
    - 'original'  : sem marcador (redação original).
    Conservador: só marca 'revogado' quando a revogação abre o corpo do artigo (revogação integral),
    para NÃO rotular um artigo inteiro como revogado quando só um §/inciso interno o foi.

    AUD-C05 — quando compilado, extrai `data_redacao` (ano da norma alteradora) e `norma_redacao`
    (referência da norma que deu a redação). Sem isso, `--data` pode devolver redação futura como
    vigente no passado (293 chunks afetados). O campo é o ANO da lei alteradora (dado verbatim),
    não a data exata de publicação (que exigiria lookup externo — princípio 1.2)."""
    corpo = RE_ROTULO_PREFIXO.sub("", texto).lstrip()
    if RE_REVOGADO_INICIO.match(corpo):
        fonte = RE_REVOGADO_FONTE.search(texto)
        return {"status": "revogado", "revogado_por": (fonte.group(1).strip() if fonte else None),
                "marcadores": ["revogado_integral"],
                "data_redacao": None, "norma_redacao": None}
    if RE_REDACAO_DADA.search(texto):
        # Extrair a norma alteradora e o ano da redação nova (AUD-C05).
        norma_redacao = None
        data_redacao = None
        m_fonte = RE_REDACAO_DADA_FONTE.search(texto)
        if m_fonte:
            norma_redacao = m_fonte.group(1).strip()
            m_ano = RE_ANO_4D.search(norma_redacao)
            if m_ano:
                data_redacao = m_ano.group(1)
        return {"status": "compilado", "revogado_por": None, "marcadores": ["redacao_dada"],
                "data_redacao": data_redacao, "norma_redacao": norma_redacao}
    return {"status": "original", "revogado_por": None, "marcadores": [],
            "data_redacao": None, "norma_redacao": None}


def slug(texto: str, limite: int = 40) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t[:limite] or "trecho"


def extrair_corpo_verbatim(md: str):
    """Retorna o texto após o marcador de verbatim, ou None se ausente."""
    idx = md.find(MARCADOR_VERBATIM)
    if idx < 0:
        return None
    return md[idx + len(MARCADOR_VERBATIM):].strip("\n")


def fatiar_corpo(corpo: str):
    """
    Divide o corpo verbatim em dispositivos. Estratégia conservadora e fiel:
    - A unidade de corte é o ARTIGO (Art. N). Subdispositivos (incisos, §§, alíneas) e
      redações citadas entre aspas ficam DENTRO do chunk do artigo — recortá-los
      arriscaria mutilar o verbatim (esta é uma lei 'alteradora', cheia de texto citado).
    - Cabeçalhos Título/Capítulo/Seção, quando existem, compõem o caminho hierárquico.
    - O texto antes do 1º artigo vira 'preambulo'; assinaturas/fecho ficam no chunk do último artigo.
    Retorna lista de dicts: {tipo, rotulo, numero, caminho[], texto}.
    """
    linhas = corpo.split("\n")
    titulo = capitulo = secao = None
    chunks = []
    atual = {"tipo": "preambulo", "rotulo": "Preâmbulo", "numero": None,
             "caminho": [], "linhas": []}

    def fechar(c):
        texto = "\n".join(c.pop("linhas")).strip()
        if texto:
            c["texto"] = texto
            chunks.append(c)

    visto_artigo = False
    for ln in linhas:
        mt, mc, ms = RE_TITULO.match(ln), RE_CAPITULO.match(ln), RE_SECAO.match(ln)
        ma = RE_ARTIGO.match(ln)
        # GUARDA (B-11): "Art. N" que abre entre ASPAS é redação CITADA dentro de uma lei alteradora
        # (ex.: 7.228 transcreve o "Art. 77" da 6.989) — NÃO é dispositivo desta norma; não abre chunk.
        if ma and ln.lstrip()[:1] in ('"', '“', '«'):
            ma = None
        # GUARDA (C-28/T1): "art. N ..." que é REMISSÃO line-initial (corpo do artigo corrente) não abre chunk.
        if ma and eh_remissao_line_initial(ln, ma):
            ma = None
        if mt:
            titulo, capitulo, secao = ln.strip(), None, None
        elif mc:
            capitulo, secao = ln.strip(), None
        elif ms:
            secao = ln.strip()
        if ma:
            fechar(atual)
            visto_artigo = True
            n = ma.group(1)
            # convenção legislativa BR: ordinal ("Art. 1º".."Art. 9º"), cardinal a partir de 10
            rot = f"Art. {n}º" if n.isdigit() and int(n) <= 9 else f"Art. {n}"
            caminho = [x for x in (titulo, capitulo, secao) if x] + [rot]
            # C-28/T1: header_raw = a linha CRUA que abriu o artigo (prova de proveniência do rótulo).
            # O eval compara rótulo ↔ header_raw e reprova divergência (fim do falso-verde do substring).
            atual = {"tipo": "artigo", "rotulo": rot, "numero": n, "header_raw": ln.strip(),
                     "caminho": caminho, "linhas": [ln]}
            continue
        atual["linhas"].append(ln)

    # último bloco: se já vimos artigos, o resto após o último artigo é parte dele;
    # mas assinatura/fecho costuma vir no mesmo bloco do último artigo — mantemos junto
    # (fidelidade > granularidade), exceto se nenhum artigo foi visto.
    if not visto_artigo:
        atual["tipo"] = "documento"
        atual["rotulo"] = "Documento"
    fechar(atual)

    # AUD-C06 — SEPARAR FECHO/ANEXO do último artigo: quando o último chunk tipo=artigo termina
    # com um bloco maciço de URLs (links do portal legislativo, referências a quadros/anexos),
    # esses links são FECHO (assinaturas/navegação do PDF capturado), não parte do dispositivo.
    # Deixá-los no artigo gera chunk de 6.888 tokens (PDE Art.174) e impede que os anexos sejam
    # recuperáveis como dispositivos separados. Critério: se >50% das linhas não-vazias do trecho
    # final são URLs (http/https ou <http...), separar em chunk tipo=anexo (não-citável).
    if chunks and chunks[-1]["tipo"] == "artigo":
        _separar_fecho_url(chunks)

    return chunks


# AUD-C06 — regex para detectar linhas que são URLs puras (capturadas do portal legislativo).
RE_LINHA_URL = re.compile(r"^\s*(?:<?\s*https?://|https?://|\[\\#)")


def _separar_fecho_url(chunks: list):
    """Se o último chunk tipo=artigo tem um bloco final de URLs, separa em chunk tipo=anexo.
    O ponto de corte é a PRIMEIRA linha URL após a qual >80% das linhas não-vazias restantes
    também são URL. Conservador: só separa se o bloco de URLs tiver >=10 linhas não-vazias
    (evita falso-positivo em artigos com 1-2 links inline no corpo)."""
    ultimo = chunks[-1]
    linhas = ultimo["texto"].split("\n")
    n_linhas = len(linhas)
    if n_linhas < 15:
        return  # artigo curto — não há bloco significativo de URLs

    # Procurar o ponto de corte: varrer de trás pra frente até achar texto não-URL
    # e verificar se o bloco de URLs é significativo.
    idx_primeiro_url = None
    for i, ln in enumerate(linhas):
        if RE_LINHA_URL.match(ln):
            if idx_primeiro_url is None:
                idx_primeiro_url = i
        elif ln.strip():
            # Linha não-vazia e não-URL: reseta o candidato (o bloco de URL deve ser CONTÍGUO no final)
            idx_primeiro_url = None

    if idx_primeiro_url is None:
        return

    # Contar linhas não-vazias no bloco de URLs
    bloco_urls = linhas[idx_primeiro_url:]
    linhas_nv_url = [l for l in bloco_urls if l.strip()]
    if len(linhas_nv_url) < 10:
        return  # bloco de URLs muito curto — não separar

    # Verificar que >80% das linhas não-vazias do bloco são de fato URLs
    n_urls = sum(1 for l in linhas_nv_url if RE_LINHA_URL.match(l))
    if n_urls / len(linhas_nv_url) < 0.8:
        return

    # Separar: o artigo fica com o texto até o ponto de corte; o bloco vira chunk tipo=anexo.
    texto_artigo = "\n".join(linhas[:idx_primeiro_url]).rstrip()
    texto_anexo = "\n".join(bloco_urls).strip()

    if not texto_artigo.strip():
        return  # segurança: não esvaziar o artigo

    ultimo["texto"] = texto_artigo
    chunks.append({
        "tipo": "anexo",
        "rotulo": "Anexos e referências",
        "numero": None,
        "caminho": ultimo["caminho"][:-1] + ["Anexos e referências"],
        "linhas_separadas_de": ultimo["rotulo"],
        "texto": texto_anexo,
    })


def fatiar_lei(md_path: Path, reportar):
    jpath = md_path.with_suffix(".json")
    if not jpath.exists():
        reportar(f"  SKIP {md_path.name}: sem .json par")
        return 0
    # Guarda de encoding (RAG-05): um arquivo não-UTF-8 na zona de despejo não pode
    # derrubar o batch inteiro (e o CI). Reporta e pula só o malformado.
    try:
        meta = json.loads(jpath.read_text(encoding="utf-8"))
        corpo = extrair_corpo_verbatim(md_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        reportar(f"  SKIP {md_path.name}: erro de leitura/encoding ({e.__class__.__name__}) — pulado")
        return 0
    lei_id = meta.get("id") or md_path.stem
    confianca = meta.get("confianca_extracao")

    if corpo is None:
        reportar(f"  SKIP {lei_id}: sem '{MARCADOR_VERBATIM}' (não-verbatim) — não entra no RAG (1.7)")
        return 0
    if confianca != "alta":
        reportar(f"  SKIP {lei_id}: confianca_extracao={confianca!r} (só 'alta' é fatiável) — RO verbatim")
        return 0

    fonte = meta.get("fonte") or {}
    vigencia = meta.get("vigencia") or {}
    tema = meta.get("tema") or []
    jurisdicao = meta.get("jurisdicao")
    # Separação TDC×IPTU (plano 2026-07-04): o domínio é METADADO e o chunk HERDA o da norma.
    # Por-documento hoje; quando o PDE for quebrado por-dispositivo, o chunk recebe o seu próprio.
    dominio = meta.get("dominio") or []
    dominio_primario = meta.get("dominio_primario")

    dispositivos = fatiar_corpo(corpo)
    if not dispositivos:
        reportar(f"  SKIP {lei_id}: corpo verbatim vazio")
        return 0

    destino = RAIZ / "rag" / "chunks" / lei_id
    if destino.exists():
        for antigo in destino.glob("*.json"):
            antigo.unlink()  # idempotência: regenera limpo
    destino.mkdir(parents=True, exist_ok=True)

    for i, d in enumerate(dispositivos, start=1):
        seq = f"{i:03d}"
        chunk_id = f"{lei_id}::{seq}-{slug(d['rotulo'])}"
        chunk = {
            "chunk_id": chunk_id,
            "lei_id": lei_id,
            "tipo_dispositivo": d["tipo"],
            "rotulo": d["rotulo"],
            "numero": d["numero"],
            # C-28/T1: proveniência do rótulo (linha crua que o gerou); ausente em preâmbulo/documento.
            "header_raw": d.get("header_raw"),
            "caminho_hierarquico": d["caminho"],
            "texto": d["texto"],
            # B-11d: preâmbulo = boilerplate do portal (órgão, título, data de captura, ementa, fórmula
            # de promulgação) — CONTEXTO, não dispositivo. Marcado NÃO-CITÁVEL: o RAG não pode fundamentar
            # uma resposta citando o preâmbulo (defeito real: "Presidência da República Casa Civil…" vinha
            # como FUNDAMENTADA). `consultar.py` o exclui por padrão (flag --incluir-nao-citavel reabre).
            # AUD-C06: anexo/fecho (URLs do portal) também é NÃO-CITÁVEL — são links de navegação, não
            # dispositivo legal que fundamente resposta.
            "citavel": d["tipo"] not in ("preambulo", "anexo"),
            # B-11c: vigência POR CHUNK (revogado/compilado/original) — deriva do próprio verbatim (1.6).
            "vigencia_dispositivo": vigencia_dispositivo(d["texto"]),
            # citação pré-montada (1.7): tudo que uma resposta precisa para fundamentar
            "citacao": {
                "norma": f"{meta.get('tipo_norma','norma')} nº {meta.get('numero')}/{meta.get('ano')} — {jurisdicao}",
                "dispositivo": " › ".join(d["caminho"]) if d["caminho"] else d["rotulo"],
                "fonte_url": fonte.get("url"),
                "vigencia": vigencia,
            },
            "tema": tema,
            # Separação TDC×IPTU: domínio herdado da norma (filtro pré-busca 2.6; compartilhado
            # entra nas consultas dos dois). Vocab fechado {tdc,iptu,compartilhado}.
            "dominio": dominio,
            "dominio_primario": dominio_primario,
            "jurisdicao": jurisdicao,
            "ementa": meta.get("ementa"),
        }
        (destino / f"{seq}__{slug(d['rotulo'])}.json").write_text(
            json.dumps(chunk, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # status_pipeline: bruto -> fatiado
    if meta.get("status_pipeline") in ("bruto", None):
        meta["status_pipeline"] = "fatiado"
        jpath.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reportar(f"  OK   {lei_id}: {len(dispositivos)} dispositivos -> rag/chunks/{lei_id}/")
    return len(dispositivos)


def main(argv):
    alvos = []
    if len(argv) > 1:
        alvos = [Path(a) if Path(a).is_absolute() else RAIZ / a for a in argv[1:]]
    else:
        alvos = sorted((RAIZ / "leis").rglob("*.md"))

    msgs = []
    total_chunks = total_leis = 0
    for md in alvos:
        n = fatiar_lei(md, msgs.append)
        if n:
            total_leis += 1
            total_chunks += n
    print("\n".join(msgs))
    print(f"\nfatiar: {total_leis} leis fatiadas, {total_chunks} dispositivos no total.")


if __name__ == "__main__":
    main(sys.argv)

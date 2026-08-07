// capturar_juris_br.js — navegador real (Playwright) no runner `brasil` para o que o
// urllib NÃO passa: WAF AWS do STF (desafio JS) e e-SAJ do TJSP. Roda dentro da imagem
// oficial do Playwright via Docker --network host (mesmo padrão dos coletores GeoSampa
// do hub — ver geosampa-siszon.yml). NÃO interpreta nada: só baixa VERBATIM (1.2) para
// jurisprudencia/_capturas/; a extração/gravação é do capturar_juris_portais.py --extrair.
//
// Saídas (fail-closed — sem teor reconhecível, nada além do diagnóstico é gravado):
//   _capturas/<id>.pdf                PDF oficial do inteiro teor (STF redir / TJSP acórdão)
//   _capturas/<id>-cposg.html         página do processo no cposg (diagnóstico + ementa)
//   _capturas/busca-stf-tdc.json      ampliação (#21): resultado VERBATIM da API de busca do STF
//   _capturas/busca-stj-tdc.html      ampliação (#21): resultado VERBATIM do SCON/STJ
//   _capturas/RELATORIO-RUNNER.txt    o que deu certo/pendente, caso a caso
const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const OUT = process.env.OUT_DIR || '/work/jurisprudencia/_capturas';
const REL = [];
const log = (...a) => { console.log(...a); REL.push(a.join(' ')); };

// Metade-runner (mesmos CASOS do capturar_juris_portais.py — manter em sincronia)
const STF = [
  { id: 'stf-re-226942-sc', docID: '592555' },
  { id: 'stf-re-387047-sc', docID: '524433' },
];
const TJSP = [
  { id: 'tjsp-ai-2126162-35-2025', cnj: '2126162-35.2025.8.26.0000' },
  { id: 'tjsp-ai-2257458-20-2024', cnj: '2257458-20.2024.8.26.0000' },
  { id: 'tjsp-ai-2324382-13-2024', cnj: '2324382-13.2024.8.26.0000' },
];

const ehPdf = (buf) => buf && buf.length > 1000 && buf.slice(0, 5).toString() === '%PDF-';

// Passa o desafio do WAF navegando no domínio e então baixa a URL com os cookies da sessão.
async function baixarComDesafio(page, urlDesafio, urlAlvo, tentativas = 3) {
  for (let i = 1; i <= tentativas; i++) {
    try {
      const r = await page.request.get(urlAlvo, { timeout: 60000 });
      const buf = Buffer.from(await r.body());
      const ct = (r.headers()['content-type'] || '').toLowerCase();
      if (ehPdf(buf)) return buf;
      log(`  tentativa ${i}: HTTP ${r.status()} content-type=${ct} (${buf.length} bytes, não-PDF) — navegando p/ resolver desafio…`);
    } catch (e) {
      log(`  tentativa ${i}: request falhou: ${String(e.message).split('\n')[0]}`);
    }
    try { await page.goto(urlDesafio, { waitUntil: 'domcontentloaded', timeout: 90000 }); } catch (e) {
      // navegação p/ PDF dispara download em vez de página — é sinal de sucesso do desafio
      log(`  goto: ${String(e.message).split('\n')[0]}`);
    }
    await page.waitForTimeout(9000); // o desafio JS do WAF resolve sozinho e planta o cookie
  }
  return null;
}

async function stfInteiroTeor(page) {
  for (const c of STF) {
    const url = `https://redir.stf.jus.br/paginadorpub/paginador.jsp?docTP=AC&docID=${c.docID}`;
    log(`== STF ${c.id} (docID ${c.docID}) ==`);
    // download via navegação também conta (headless baixa PDF em vez de renderizar)
    let porDownload = null;
    page.once('download', async (d) => { porDownload = d; });
    const buf = await baixarComDesafio(page, url, url);
    if (buf) {
      fs.writeFileSync(path.join(OUT, `${c.id}.pdf`), buf);
      log(`  OK: ${c.id}.pdf (${buf.length} bytes)`);
    } else if (porDownload) {
      const p = path.join(OUT, `${c.id}.pdf`);
      await porDownload.saveAs(p);
      log(`  OK (via download): ${c.id}.pdf (${fs.statSync(p).size} bytes)`);
    } else {
      log(`  PEND: WAF não liberou o PDF em 3 tentativas (fail-closed).`);
    }
  }
}

async function tjspCposg(page) {
  for (const c of TJSP) {
    log(`== TJSP ${c.id} (${c.cnj}) ==`);
    const dda = c.cnj.slice(0, 15); // NNNNNNN-DD.AAAA
    const foro = c.cnj.slice(-4);
    const busca = 'https://esaj.tjsp.jus.br/cposg/search.do?conversationId=&paginaConsulta=0' +
      `&cbPesquisa=NUMPROC&numeroDigitoAnoUnificado=${encodeURIComponent(dda)}` +
      `&foroNumeroUnificado=${foro}&dePesquisaNuUnificado=${encodeURIComponent(c.cnj)}` +
      '&dePesquisaNuUnificado=UNIFICADO&dePesquisa=&tipoNuProcesso=UNIFICADO';
    try {
      await page.goto(busca, { waitUntil: 'domcontentloaded', timeout: 90000 });
      await page.waitForTimeout(4000);
      const html = await page.content();
      fs.writeFileSync(path.join(OUT, `${c.id}-cposg.html`), html);
      log(`  página do processo salva (${html.length} chars): ${c.id}-cposg.html`);
      // links de acórdão/documento vinculado (PDF) na própria sessão
      const links = await page.$$eval('a', as => as
        .map(a => ({ href: a.href || '', texto: (a.textContent || '').trim() }))
        .filter(l => /getArquivo|abrirDocumentoVinculado|pastadigital/i.test(l.href)));
      log(`  ${links.length} link(s) de documento na página.`);
      let salvo = false;
      for (const l of links.slice(0, 6)) {
        try {
          const r = await page.request.get(l.href, { timeout: 60000 });
          const buf = Buffer.from(await r.body());
          if (ehPdf(buf)) {
            fs.writeFileSync(path.join(OUT, `${c.id}.pdf`), buf);
            log(`  OK: acórdão PDF via "${l.texto.slice(0, 60)}" (${buf.length} bytes)`);
            salvo = true; break;
          }
        } catch (e) { log(`  link falhou: ${String(e.message).split('\n')[0]}`); }
      }
      if (!salvo) log('  PEND: sem PDF direto — o HTML salvo diagnostica o caminho (senha do processo? pasta digital?).');
    } catch (e) {
      log(`  PEND: cposg não abriu: ${String(e.message).split('\n')[0]}`);
    }
  }
}

// Ampliação (#21): varre as bases oficiais por TDC e salva o resultado VERBATIM p/ curadoria.
async function buscarAmpliacao(page) {
  log('== BUSCA de ampliação (#21) — TDC nas bases oficiais ==');
  const qs = 'transferência do direito de construir';
  try {
    // resolve o desafio do domínio da pesquisa do STF, depois chama a API com os cookies
    try { await page.goto('https://jurisprudencia.stf.jus.br/pages/search', { waitUntil: 'domcontentloaded', timeout: 90000 }); } catch (_) {}
    await page.waitForTimeout(9000);
    const api = 'https://jurisprudencia.stf.jus.br/api/search/search?base=acordaos&sinonimo=true&plural=true&page=1&pageSize=30&queryString=' + encodeURIComponent(`"${qs}"`);
    const r = await page.request.get(api, { timeout: 60000 });
    const txt = await r.text();
    if (r.status() === 200 && txt.trim().startsWith('{')) {
      fs.writeFileSync(path.join(OUT, 'busca-stf-tdc.json'), txt);
      log(`  OK: busca-stf-tdc.json (${txt.length} chars)`);
    } else {
      log(`  PEND STF-busca: HTTP ${r.status()} (payload não-JSON, provável desafio).`);
    }
  } catch (e) { log(`  PEND STF-busca: ${String(e.message).split('\n')[0]}`); }
  try {
    const scon = 'https://scon.stj.jus.br/SCON/pesquisar.jsp?newsession=yes&tipo_visualizacao=RESUMO&b=ACOR&livre=' + encodeURIComponent(`"${qs}"`);
    await page.goto(scon, { waitUntil: 'domcontentloaded', timeout: 90000 });
    await page.waitForTimeout(4000);
    const html = await page.content();
    fs.writeFileSync(path.join(OUT, 'busca-stj-tdc.html'), html);
    log(`  OK: busca-stj-tdc.html (${html.length} chars)`);
  } catch (e) { log(`  PEND STJ-busca: ${String(e.message).split('\n')[0]}`); }
}

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch({ args: ['--no-sandbox'] });
  const ctx = await browser.newContext({ acceptDownloads: true, userAgent:
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36' });
  const page = await ctx.newPage();
  try { await page.goto('https://api.ipify.org', { timeout: 60000 }); log('IP público:', await page.textContent('body')); } catch (e) { log('IP: falhou', e.message); }
  await stfInteiroTeor(page);
  await tjspCposg(page);
  await buscarAmpliacao(page);
  fs.writeFileSync(path.join(OUT, 'RELATORIO-RUNNER.txt'), REL.join('\n') + '\n');
  await browser.close();
  log('FIM.');
})().catch(e => { console.error('ERRO FATAL:', e); process.exit(1); });

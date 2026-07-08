// geosampa_probe.js — DESCOBERTA do serviço interno do GeoSampa/SISZON (roda no VPS `brasil`, IP-BR).
// Por que no VPS: o proxy do ambiente de sessão bloqueia navegador headless (reset até em example.com);
// a VPS tem IP brasileiro e rede livre. Objetivo: achar o endpoint que a aba "Zoneamento" chama ao
// consultar por SQL, e capturar a ZONA-BASE do imóvel de teste (o gap CAbás do gabarito Termo 006/2026).
// Uso: TEST_SQL=001080-0016-8 node scripts/geosampa_probe.js   (label brasil; playwright instalado)
const { chromium } = require('playwright');

const TEST_SQL = process.env.TEST_SQL || '001080-0016-8';           // Líbero Badaró 306/310 (gabarito)
const [SETOR_QUADRA, LOTE] = TEST_SQL.split('-');                   // "001080", "0016-8" (ajuste se o form separar)

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox'] });
  const page = await (await browser.newContext({ ignoreHTTPSErrors: true })).newPage();

  const endpoints = new Set();
  const zoneResponses = [];
  const RE = /siszon|zonea|lote|consulta|servico|webservice|\.asmx|\.ashx|rest|geoserver|arcgis|json/i;
  page.on('request', r => { const u = r.url(); if (RE.test(u)) endpoints.add(r.method() + ' ' + u.split('?')[0]); });
  page.on('response', async resp => {
    const u = resp.url();
    if (/siszon|zonea|consulta|lote/i.test(u)) {
      try { const b = await resp.text(); if (b && b.length < 20000) zoneResponses.push({ url: u.slice(0, 160), status: resp.status(), body: b.slice(0, 4000) }); } catch (_) {}
    }
  });

  console.log('== abrindo GeoSampa (IP-BR esperado) ==');
  try { await page.goto('https://geosampa.prefeitura.sp.gov.br/PaginasPublicas/_SBC.aspx', { waitUntil: 'domcontentloaded', timeout: 90000 }); }
  catch (e) { console.log('goto erro:', e.message.split('\n')[0]); }
  await page.waitForTimeout(12000);
  console.log('TITULO:', await page.title());

  // Best-effort: abrir busca -> aba Zoneamento -> preencher SQL -> LISTAR. Se a UI mudou, o dump de rede abaixo já ajuda.
  const tried = [];
  try {
    for (const sel of ['#imgPesquisar', 'text=Pesquisar', '[title*="esquisar"]', '.lupa', '#btnBusca']) {
      const el = await page.$(sel); if (el) { await el.click().catch(()=>{}); tried.push('click '+sel); await page.waitForTimeout(1500); break; }
    }
    for (const sel of ['text=Zoneamento', 'a:has-text("Zoneamento")', '[id*="onea"]']) {
      const el = await page.$(sel); if (el) { await el.click().catch(()=>{}); tried.push('aba '+sel); await page.waitForTimeout(1500); break; }
    }
    // preencher qualquer input textual visível com o SQL e disparar LISTAR
    const inputs = await page.$$('input[type="text"], input:not([type])');
    if (inputs[0]) { await inputs[0].fill(SETOR_QUADRA + LOTE).catch(()=>{}); tried.push('fill sql'); }
    for (const sel of ['text=LISTAR', 'button:has-text("LISTAR")', 'input[value*="ISTAR"]']) {
      const el = await page.$(sel); if (el) { await el.click().catch(()=>{}); tried.push('LISTAR '+sel); await page.waitForTimeout(4000); break; }
    }
  } catch (e) { console.log('UI best-effort erro:', e.message.split('\n')[0]); }
  console.log('interações tentadas:', tried.join(' | ') || '(nenhuma — seletores não bateram)');
  await page.waitForTimeout(4000);

  console.log('\n== ENDPOINTS candidatos (' + endpoints.size + ') ==');
  [...endpoints].sort().forEach(u => console.log(u));
  console.log('\n== RESPOSTAS de zoneamento/consulta (' + zoneResponses.length + ') ==');
  zoneResponses.forEach(r => console.log('---', r.status, r.url, '\n', r.body, '\n'));

  await browser.close();
})().catch(e => { console.log('ERRO FATAL:', e.message.slice(0, 200)); process.exit(1); });

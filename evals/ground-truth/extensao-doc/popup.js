// popup.js — orquestra a coleta. Guarda tudo em chrome.storage.local ("itens").
const $ = id => document.getElementById(id);
const setStatus = (t) => { $('status').innerHTML = t; };
const getItens = async () => (await chrome.storage.local.get('itens')).itens || [];
const setItens = async (itens) => chrome.storage.local.set({ itens });
const chaveDe = (o) => (o.declaracao || '') + '|' + (o.termo || '') + '|' + (o.sql_contribuinte || '') + '|' + (o.processo || '');

async function refreshCount() { const it = await getItens(); $('count').textContent = it.length; }

async function addItem(o) {
  if (!o || !o._relevante) return false;
  const itens = await getItens();
  const k = chaveDe(o);
  const i = itens.findIndex(x => chaveDe(x) === k);
  if (i >= 0) itens[i] = { ...itens[i], ...o }; else itens.push(o);
  await setItens(itens); await refreshCount(); return true;
}

async function abaAtiva() { const [t] = await chrome.tabs.query({ active: true, currentWindow: true }); return t; }

// --- 1) Extrair a publicação aberta ---
$('extrair').onclick = async () => {
  try {
    const t = await abaAtiva();
    const o = await chrome.tabs.sendMessage(t.id, { tipo: 'extrair' });
    const ok = await addItem(o);
    setStatus(ok ? `✓ Extraído: m²=${o.m2_transferivel || '—'} · SQL=${o.sql_contribuinte || '—'} · zona=${o.zona || '—'}\nColetados: <span id="count">${(await getItens()).length}</span>`
                 : 'Esta página não parece uma publicação de TDC (sem m²/declaração/termo). Abra a matéria e tente de novo.');
  } catch (e) { setStatus('Erro: ' + e.message + '\n(Abra uma página do Diário Oficial primeiro.)'); }
};

// --- 2) Varrer os resultados da busca (fetch de cada matéria, sem abrir abas) ---
$('varrer').onclick = async () => {
  try {
    const t = await abaAtiva();
    const { links } = await chrome.tabs.sendMessage(t.id, { tipo: 'links' });
    if (!links || !links.length) { setStatus('Nenhum link de resultado encontrado nesta página. Faça a busca no Diário Oficial e rode aqui.'); return; }
    let ok = 0, i = 0;
    for (const url of links) {
      i++; setStatus(`Varrendo ${i}/${links.length}… coletados relevantes: ${ok}`);
      try {
        const r = await fetch(url, { credentials: 'include' });
        const html = await r.text();
        const doc = new DOMParser().parseFromString(html, 'text/html');
        const texto = doc.body ? doc.body.innerText || doc.body.textContent : '';
        const o = window.extrairDeTexto(texto, url, doc.title);
        if (await addItem(o)) ok++;
      } catch (_) { /* segue */ }
    }
    setStatus(`✓ Varredura terminada. Relevantes coletados nesta rodada: ${ok}.\nTotal: <span id="count">${(await getItens()).length}</span>`);
  } catch (e) { setStatus('Erro: ' + e.message + '\n(Rode na página de RESULTADOS da busca.)'); }
};

// --- exportar ---
function baixar(nome, conteudo, mime) {
  const blob = new Blob([conteudo], { type: mime });
  const url = URL.createObjectURL(blob);
  chrome.downloads.download({ url, filename: nome, saveAs: true });
}
const COLS = ['termo', 'declaracao', 'processo', 'sql_contribuinte', 'm2_transferivel', 'zona', 'resolucao', 'matricula', 'endereco', 'titulo', 'url'];
$('csv').onclick = async () => {
  const it = await getItens(); if (!it.length) return setStatus('Nada coletado ainda.');
  const esc = v => '"' + String(v == null ? '' : v).replace(/"/g, '""') + '"';
  const linhas = [COLS.join(',')].concat(it.map(o => COLS.map(c => esc(o[c])).join(',')));
  baixar('gabaritos-doc.csv', '﻿' + linhas.join('\n'), 'text/csv;charset=utf-8');
};
$('json').onclick = async () => {
  const it = await getItens(); if (!it.length) return setStatus('Nada coletado ainda.');
  baixar('gabaritos-doc.json', JSON.stringify(it, null, 2), 'application/json');
};
$('limpar').onclick = async () => { await setItens([]); await refreshCount(); setStatus('Coleta limpa. Coletados: <span id="count">0</span>'); };

// --- 3) Refinar com IA (opcional, "prompt bom") ---
const PROMPT_IA = `Você extrai dados de uma publicação do Diário Oficial de São Paulo sobre Transferência de Potencial Construtivo (TDC / imóvel tombado ZEPEC).
Do TEXTO abaixo, devolva SOMENTE um objeto JSON com estas chaves (use null quando ausente; NÃO invente):
- m2_transferivel: número em m² do potencial construtivo TRANSFERÍVEL/passível (ex.: 717.60, ponto decimal), o valor oficial da Declaração SMUL/DEUSO;
- sql_contribuinte: SQL do imóvel no formato 000.000.0000-0;
- processo: número do processo administrativo (ex.: 6025.2024/0013449-9);
- declaracao: número da Declaração de Potencial Construtivo SMUL/DEUSO (ex.: 0539/23);
- termo: número do Termo de Compromisso CONPRESP (ex.: 006/2026) se houver;
- zona: sigla da zona de uso citada (ex.: ZEPEC-BIR, ZC, ZM) se houver;
- endereco, matricula, resolucao: se citados.
Regra de ouro: o m² é o VALOR OFICIAL do documento; se o texto trouxer vários números em m², escolha o rotulado como transferível/passível de transferência. Responda só o JSON.`;

$('ia').onclick = async () => {
  const key = $('apikey').value.trim();
  if (!key) return setStatus('Cole a chave Claude para usar a IA (ou use só o regex).');
  const itens = await getItens(); if (!itens.length) return setStatus('Nada para reprocessar.');
  let ok = 0;
  for (let i = 0; i < itens.length; i++) {
    setStatus(`IA reprocessando ${i + 1}/${itens.length}…`);
    try {
      const resp = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: { 'content-type': 'application/json', 'x-api-key': key, 'anthropic-version': '2023-06-01', 'anthropic-dangerous-direct-browser-access': 'true' },
        body: JSON.stringify({ model: 'claude-haiku-4-5-20251001', max_tokens: 500, messages: [{ role: 'user', content: PROMPT_IA + '\n\nTEXTO:\n' + (itens[i].texto_bruto || itens[i].trecho || '') }] })
      });
      const data = await resp.json();
      const txt = (data.content && data.content[0] && data.content[0].text) || '';
      const j = JSON.parse(txt.slice(txt.indexOf('{'), txt.lastIndexOf('}') + 1));
      itens[i] = { ...itens[i], ...j, _ia: true };
      ok++;
    } catch (_) { /* mantém regex */ }
  }
  await setItens(itens);
  setStatus(`✓ IA reprocessou ${ok}/${itens.length}. Baixe o CSV/JSON.`);
};

refreshCount();

// content.js — roda DENTRO da página do Diário Oficial (sessão do dono → sem bloqueio).
// Usa extractor.js (extrairDeTexto). Responde a dois pedidos do popup:
//   'extrair' → campos da publicação aberta;  'links' → links de resultados p/ varredura.
(() => {
  function linksDeResultados() {
    const sel = 'a[href*="materia"], a[href*="detalhe"], a[href*="md_epubli"], a[href*="visualiza"], .resultado a, .sumario a, li a';
    const hrefs = [...document.querySelectorAll(sel)].map(a => a.href)
      .filter(h => h && /prefeitura\.sp\.gov\.br|imprensaoficial/.test(h) && !/#$/.test(h));
    return [...new Set(hrefs)];
  }
  chrome.runtime.onMessage.addListener((msg, _s, sendResponse) => {
    if (msg.tipo === 'extrair') sendResponse(window.extrairDeTexto(document.body && document.body.innerText, location.href, document.title));
    else if (msg.tipo === 'links') sendResponse({ links: linksDeResultados() });
    return true;
  });
})();

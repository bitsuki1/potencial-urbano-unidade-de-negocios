// extractor.js — extração pura (texto → campos do gabarito TDC). Fonte ÚNICA usada tanto
// pelo content script (página aberta) quanto pelo popup (fetch dos resultados). Só regex,
// resiliente a layout. A camada "IA" (opcional) roda depois, sobre texto_bruto.
(function (root) {
  const RX = {
    m2: [
      /potencial\s+construtivo[^.]{0,140}?([\d.]{1,7},\d{2})\s*m[²2]/i,
      /transfer[ií]ve[l][^.]{0,140}?([\d.]{1,7},\d{2})\s*m[²2]/i,
      /([\d.]{1,7},\d{2})\s*m[²2][^.]{0,80}?(?:transfer|potencial)/i,
      /área?\s+(?:construída\s+)?(?:total\s+)?(?:transfer[ií]vel|pass[íi]vel)[^.]{0,80}?([\d.]{1,7},\d{2})\s*m[²2]/i
    ],
    sql_contrib: [/\b(\d{3}\.\d{3}\.\d{4}-\d)\b/],
    processo: [/\b(6\d{3}\.\d{4}\/\d{7}-\d)\b/, /\b(\d{2}-\d{3}\.\d{3}-\d{2}\*?\d{0,2})\b/],
    declaracao: [/DEUSO[^\d]{0,20}(\d{3,4}\/\d{2,4})/i, /Declara[çc][ãa]o[^\d]{0,30}?(?:n[º°.]?\s*)?(\d{3,4}\/\d{2,4})/i],
    termo: [/Termo\s+de\s+Compromisso[^\d]{0,20}(\d{1,4}\/\d{4})/i],
    resolucao: [/Resolu[çc][ãa]o[^\d]{0,20}(\d{1,3}\/[A-Z]{0,8}\/?\d{4})/i],
    matricula: [/matr[íi]cula[^\d]{0,30}?(?:n[º°.]?\s*)?([\d.]{3,10})/i],
    zona: [/\b(ZEPEC[_ -][A-Z-]{2,10}|ZEIS[- ]?\d?|ZEU[Pa]?|ZEM[P]?|ZC[a]?|ZCOR[- ]?\d?|ZM[ISa]*|ZPI[- ]?\d?|ZOE|ZPDS[ru]?|ZER[- ]?\d?a?)\b/],
    endereco: [/(?:Rua|Avenida|Av\.|Travessa|Pra[çc]a|Alameda|Largo)\s+[^,;\n]{3,60}?,?\s*n?[º°.]?\s*\d{1,5}/i]
  };
  const first = (t, arr) => { for (const rx of arr) { const m = t.match(rx); if (m) return (m[1] || m[0]).trim(); } return null; };

  function extrairDeTexto(textoRaw, url, titulo) {
    const texto = (textoRaw || '').replace(/ /g, ' ');
    const o = {
      m2_transferivel: first(texto, RX.m2),
      sql_contribuinte: first(texto, RX.sql_contrib),
      processo: first(texto, RX.processo),
      declaracao: first(texto, RX.declaracao),
      termo: first(texto, RX.termo),
      resolucao: first(texto, RX.resolucao),
      matricula: first(texto, RX.matricula),
      zona: first(texto, RX.zona),
      endereco: first(texto, RX.endereco),
      url: url || '', titulo: titulo || '',
      trecho: (() => { const i = texto.search(/potencial\s+construtivo|transfer[ií]ve/i); return i >= 0 ? texto.slice(Math.max(0, i - 300), i + 500) : texto.slice(0, 800); })(),
      texto_bruto: texto.slice(0, 12000)
    };
    o._relevante = !!(o.m2_transferivel || o.declaracao || o.termo);
    return o;
  }
  root.extrairDeTexto = extrairDeTexto;
})(typeof window !== 'undefined' ? window : this);

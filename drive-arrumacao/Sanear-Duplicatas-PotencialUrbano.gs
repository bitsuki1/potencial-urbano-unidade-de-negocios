/**
 * ============================================================================
 *  SANEAR DUPLICATAS — POTENCIAL URBANO (IPTU / TDC)
 *  Companion do Arrumar-Drive-PotencialUrbano.gs. Gerado pela Auditoria
 *  triplo-limpo do Escritório do MOU — 2026-06-20. Decisão do MOU: EXCLUIR.
 *
 *  O QUE FAZ: manda para a LIXEIRA (setTrashed = recuperável ~30 dias) as
 *  cópias duplicadas, mantendo SEMPRE 1 cópia canônica de cada grupo.
 *
 *  SEGURANÇA:
 *   - DRY_RUN=true por padrão: só LOGA o que faria. Rode 1×, leia o Log
 *     (Ver > Logs), confira, então mude para false e rode de novo p/ executar.
 *   - FASE 1 (explícita): só apaga IDs verificados na auditoria, e SÓ depois de
 *     confirmar que a cópia canônica (KEEP) do grupo existe e é legível.
 *   - FASE 2 (genérica, dedup por nome+tamanho na pasta de despejo): só apaga
 *     quando nome E tamanho batem com uma cópia já mantida (duplicata real).
 *     Ignora arquivos Google-nativos (Sheets/Docs — tamanho não confiável) e
 *     NUNCA apaga um arquivo único (grupo de 1).
 *   - VACINA: não mexe em shapefiles únicos; o conjunto SIRGAS_SHP_LOTES só é
 *     tocado se houver duplicata exata (nome+tamanho) — 1 cópia sempre fica.
 * ============================================================================
 */

var DRY_RUN = true;                 // <-- mude para false p/ EXECUTAR de verdade
var RODAR_FASE_2 = true;            // dedup genérico por nome+tamanho no despejo
var DESPEJO_ID = '1grhqYgttj7KnJmiu9U73z-lXFHnFthov'; // "01 — _entrada (despejo)"

// FASE 1 — grupos explícitos da auditoria (KEEP = manter; TRASH = lixeira)
var GRUPOS = [
  { nome: 'socios.csv',   keep: '1gftoKzFaD-NyKClBg3SH8Eo0FYncQYvt',
    trash: ['1Lffz6w6OvS-5KqakDT71ZqIzsudRLnoI','1ncSTA-P2GfV2cPN-y1f2cnjqFDGSqa9e'] },
  { nome: 'empresas.csv', keep: '1uRWg7wA4KuppJ1TSdEwRmV3H06fTXlnj',
    trash: ['18Q-_8iD5ZihVh-UnmD4itZ8WEa19g02a','1u0ZaQCqfG0Moq2eroL-8_E1njnHJbgP5'] },
  { nome: 'IPTU_2026.csv', keep: '1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM',
    trash: ['1oX6BDTF_MJhrt8es4xh3N-cFtDbeoNGt','1EubfSLtbGNF5G2MLS9eT_DiAsVCtv0fM',
            '1A3NK8K6wAn4ZjGCl5rqb2mCB8j50t0Pl','1GOBf3pOYrDATCTOfMHLdbG1Iv82kV7Qt',
            '1Uvb9CYQNomG00MJo0kLAgOL3F2Xb8ay-'] },
  { nome: 'holdings.csv', keep: '1BrBRzC3G4atGZ8JqRZhGp4OnvBZTjOgr',
    trash: ['1lBfWs1FCsxCTgpAu_5WzbZJ8WnLodxi9','1LGUIQysj-1_8deN8AeQi5ChwORjyoWHR',
            '17WdJjyVAg6macYZ9DjM-xIiR5bEFqjQo','1fdabbNncuOexRrmIEvP1N2L-oNyZmk-j',
            '1H3-gburttjEyLYmBBUH1qM7DH1fxUEZL'] },
  { nome: 'Arrumacao (planilhas intermediárias)', keep: '1Wt2eFe-05D5fU8FsjeH0UiGFyokBcAa6U-sqDxFx0k8',
    trash: ['1mFJdqwz3MCKdSuxXkOmZMO1aKR1dzU_MhejGNXL3lzQ','15GmJ2Nku9Rwv3n7m7cMqqI90kO6BAUNbyBb-3oaQx3w',
            '1Bcyd37AcNSZfT2tti2jA1nZobM4b8dUx5_D9PDiimSE','1LgVwo5xajrJab1nJZJRkKpkCmDD0pndKE8RytaQOFLc',
            '13V2r0oSnEjJjnRLfuPjWsDYeKel7xA5BLHlFGPjc1nc','1rYAJMQoIIW20WLniCX8N0fNBqUGi6itTARnUUbjIFk4',
            '1-u2l3VKidnibTCXOkblFj6E3-S4e0wRWuDRbjO5DfQI'] },
  { nome: 'Arrumacao CSV dup (67.586 B)', keep: '1Cp1Fl7QSR_Vr34wOvtIv7yVu_IIvkvIl',
    trash: ['1nRkAywkknccPHIRM8ve1PFh3eJUiKCwh'] }
];

function existeLegivel_(id) {
  try { var f = DriveApp.getFileById(id); f.getName(); return f; } catch (e) { return null; }
}

function sanearFase1_() {
  var apagados = 0, pulados = 0;
  for (var i = 0; i < GRUPOS.length; i++) {
    var g = GRUPOS[i];
    var keep = existeLegivel_(g.keep);
    if (!keep) { Logger.log('[PULA grupo "%s"] canônica KEEP %s não encontrada — NÃO apago nada deste grupo.', g.nome, g.keep); pulados += g.trash.length; continue; }
    Logger.log('[GRUPO %s] mantendo canônica: %s (%s)', g.nome, keep.getName(), g.keep);
    for (var j = 0; j < g.trash.length; j++) {
      var f = existeLegivel_(g.trash[j]);
      if (!f) { Logger.log('   - %s já não existe (ok)', g.trash[j]); continue; }
      if (DRY_RUN) { Logger.log('   - [DRY-RUN] APAGARIA %s (%s)', f.getName(), g.trash[j]); }
      else { f.setTrashed(true); Logger.log('   - LIXEIRA: %s (%s)', f.getName(), g.trash[j]); }
      apagados++;
    }
  }
  Logger.log('FASE 1: %s %s, %s pulados.', (DRY_RUN ? 'apagaria' : 'apagados'), apagados, pulados);
  return apagados;
}

function sanearFase2_() {
  var pasta = existeLegivel_(DESPEJO_ID);
  if (!pasta) { Logger.log('FASE 2 PULADA: despejo %s não acessível.', DESPEJO_ID); return 0; }
  var vistos = {}, apagados = 0;
  // só nível raiz do despejo (onde a auditoria viu as duplicatas .txt/ITBI/etc.)
  var it = DriveApp.getFolderById(DESPEJO_ID).getFiles();
  var lista = [];
  while (it.hasNext()) { lista.push(it.next()); }
  // ordena por data desc para manter o mais recente
  lista.sort(function(a, b){ return b.getLastUpdated() - a.getLastUpdated(); });
  for (var k = 0; k < lista.length; k++) {
    var f = lista[k];
    var mime = f.getMimeType();
    if (mime.indexOf('application/vnd.google-apps') === 0) continue; // nativos: tamanho não confiável
    var sz = f.getSize();
    if (!sz) continue;
    var chave = f.getName() + '|' + sz;
    if (vistos[chave]) {
      if (DRY_RUN) { Logger.log('   - [DRY-RUN] DUP APAGARIA %s (%s B) id=%s', f.getName(), sz, f.getId()); }
      else { f.setTrashed(true); Logger.log('   - LIXEIRA DUP: %s (%s B) id=%s', f.getName(), sz, f.getId()); }
      apagados++;
    } else { vistos[chave] = f.getId(); }
  }
  Logger.log('FASE 2 (dedup nome+tamanho, raiz do despejo): %s %s.', (DRY_RUN ? 'apagaria' : 'apagados'), apagados);
  return apagados;
}

/** PONTO DE ENTRADA — rode esta função. */
function sanearDuplicatas() {
  Logger.log('=== SANEAR DUPLICATAS — DRY_RUN=%s ===', DRY_RUN);
  var t = sanearFase1_();
  if (RODAR_FASE_2) t += sanearFase2_();
  Logger.log('=== FIM — total %s %s. %s ===', (DRY_RUN ? 'a apagar' : 'apagados'), t,
             (DRY_RUN ? 'Confira o Log; mude DRY_RUN=false e rode de novo p/ executar.' : 'Recuperável na Lixeira do Drive ~30 dias.'));
}

/**
 * ============================================================================
 *  TRASH FOLLOW-UP DUPLICATAS — roda na conta do DONO (eduardo@saobentoservicos.com.br)
 *  PU 18 · 2026-07-06. Segunda leva: cópias vivas dos 4 arquivos pesados que a lista
 *  auditada de 20/06 NÃO cobria (achadas na verificação por busca do assistente).
 *  Mesmo padrão do Trash-13-Duplicatas: roda COMO VOCÊ, ensaio primeiro, re-confere tamanho.
 *
 *  Mantém SEMPRE a canônica (em "03 — Tabelas & Engines" 1v4H2Ys...), que NÃO está aqui:
 *    socios   MANTÉM 1gftoKzFaD-NyKClBg3SH8Eo0FYncQYvt
 *    empresas MANTÉM 1uRWg7wA4KuppJ1TSdEwRmV3H06fTXlnj
 *    IPTU     MANTÉM 1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM
 *    holdings MANTÉM 1BrBRzC3G4atGZ8JqRZhGp4OnvBZTjOgr
 *
 *  COMO USAR: script.google.com > Novo projeto > cole > rode  trashFollowup  com
 *  DRY_RUN=true, confira o Log, depois DRY_RUN=false e rode de novo. Libera ~24,9 GB.
 * ============================================================================
 */
var DRY_RUN = true;   // <-- mude para false para EXCLUIR de verdade (lixeira)

// [ id , grupo , tamanho_esperado ] — 13 cópias duplicadas vivas (fora da lista de 20/06)
var DUPS = [
  ['1EHBkDFTe22aRhc7jmRg2GXucBqQgYjxR', 'socios.csv',   3435677749],
  ['1p5giYIRpQtM2zmzyZSls71QQenpJotvO', 'socios.csv',   3435677749],
  ['1DFvAppJBecfMpv7kvsIoDKOb6B_6F5tI', 'socios.csv',   3435677749],
  ['1nSocQSg8LCe662rEHLKbEdLhMETX_0jz', 'socios.csv',   3435677749],
  ['1egHmFkiSsSE2t9vbAUWo--kNJwNm1qyg', 'empresas.csv', 2269763986],
  ['1GdXiaUnZjSkYZnr71Nu09rEPSYR27Vb6', 'empresas.csv', 2269763986],
  ['1EXjuCh12Jct39FruLLQ8Gsd_uOvC8uvp', 'empresas.csv', 2269763986],
  ['1NjfCVyRjI80II9rwEdmMPoYZT98-Pdc3', 'empresas.csv', 2269763986],
  ['1fEKDvP89EfC3vOkB10QLyIsJMA5UTR44', 'holdings.csv',   60233422],
  ['1M_cVOxKPDuvBGVzXZ-U08Fj-XIIU5BWP', 'holdings.csv',   60233422],
  ['19EbR5e5DYFBvR8C-lb4JcZzun9Qgj0do', 'holdings.csv',   60233422],
  ['1GOBf3pOYrDATCTOfMHLdbG1Iv82kV7Qt', 'IPTU_2026.csv', 937865216],
  ['1xrsWBHU6BFnuy305lWG3BTDQSxl64vno', 'IPTU_2026.csv', 937865216]
];

function trashFollowup() {
  var apagados = 0, pulados = 0, ganho = 0;
  Logger.log((DRY_RUN ? '[ENSAIO] ' : '[EXCLUINDO] ') + DUPS.length + ' duplicatas (follow-up)');
  for (var i = 0; i < DUPS.length; i++) {
    var id = DUPS[i][0], grupo = DUPS[i][1], size_esp = DUPS[i][2];
    var f;
    try { f = DriveApp.getFileById(id); } catch (e) {
      Logger.log('PULA ' + grupo + '/' + id + ': não encontrado (' + e + ')'); pulados++; continue;
    }
    var size = f.getSize();
    if (size !== size_esp) {
      Logger.log('PULA ' + grupo + '/' + id + ': tamanho ' + size + ' != esperado ' + size_esp +
                 ' — NÃO é a duplicata esperada (não apago)'); pulados++; continue;
    }
    if (f.isTrashed()) { Logger.log('JA_NA_LIXEIRA ' + grupo + '/' + id); pulados++; continue; }
    if (DRY_RUN) {
      Logger.log('DRYRUN trash ' + grupo + ' « ' + f.getName() + ' » (' + size + ' B)');
      apagados++; ganho += size; continue;
    }
    f.setTrashed(true);
    Logger.log('TRASHED ' + grupo + ' « ' + f.getName() + ' » (' + size + ' B)');
    apagados++; ganho += size;
  }
  Logger.log('=== FIM === modo=' + (DRY_RUN ? 'DRYRUN' : 'REAL') +
             ' para_lixeira=' + apagados + ' pulados=' + pulados +
             ' ganho=' + (ganho / 1073741824).toFixed(2) + ' GB');
}

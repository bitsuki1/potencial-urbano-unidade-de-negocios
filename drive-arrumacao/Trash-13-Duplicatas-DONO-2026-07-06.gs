/**
 * ============================================================================
 *  TRASH 13 DUPLICATAS — roda na conta do DONO (eduardo@saobentoservicos.com.br)
 *  PU 18 · 2026-07-06. Companion do saneamento: o robô (Editor) recebeu HTTP 403
 *  ao tentar mandar para a lixeira (só o DONO pode excluir arquivos que possui).
 *  Este script roda COMO VOCÊ e faz o setTrashed nos 13 confirmados pelo ensaio.
 *
 *  SEGURANÇA (trava dupla):
 *   - DRY_RUN=true por padrão: só LISTA (nome+tamanho), não apaga nada. Rode 1×,
 *     confira o Log (Ver > Registros), então mude para false e rode de novo.
 *   - RE-CONFERE O TAMANHO: só manda para a lixeira se o tamanho do arquivo bater
 *     com o esperado (duplicata real). Se um ID estiver stale/errado, PULA e avisa.
 *   - Só toca nestes 13 IDs. NENHUMA canônica está aqui (as canônicas ficam):
 *       socios   MANTÉM 1gftoKzFaD-NyKClBg3SH8Eo0FYncQYvt
 *       empresas MANTÉM 1uRWg7wA4KuppJ1TSdEwRmV3H06fTXlnj
 *       IPTU     MANTÉM 1HPvwPOkjRwlC4dfgEYpYkfyDJ5l94tNM
 *       holdings MANTÉM 1BrBRzC3G4atGZ8JqRZhGp4OnvBZTjOgr
 *
 *  COMO USAR:
 *   1. script.google.com > Novo projeto > cole este arquivo inteiro.
 *   2. Rode  trashDuplicatas  com DRY_RUN=true (autorize o Drive na 1ª vez).
 *      Leia Ver > Registros: confira os 13 nomes/tamanhos. Nada foi apagado.
 *   3. Aprovou? Mude DRY_RUN para false, rode de novo. Vai para a LIXEIRA
 *      (recuperável ~30 dias). Libera ~15,5 GB.
 * ============================================================================
 */
var DRY_RUN = true;   // <-- mude para false para EXCLUIR de verdade (lixeira)

// [ id , grupo , tamanho_esperado_em_bytes ] — 13 duplicatas confirmadas no ensaio de 2026-07-06
var DUPS = [
  ['1Lffz6w6OvS-5KqakDT71ZqIzsudRLnoI', 'socios.csv',   3435677749],
  ['1ncSTA-P2GfV2cPN-y1f2cnjqFDGSqa9e', 'socios.csv',   3435677749],
  ['18Q-_8iD5ZihVh-UnmD4itZ8WEa19g02a', 'empresas.csv', 2269763986],
  ['1u0ZaQCqfG0Moq2eroL-8_E1njnHJbgP5', 'empresas.csv', 2269763986],
  ['1oX6BDTF_MJhrt8es4xh3N-cFtDbeoNGt', 'IPTU_2026.csv', 937865216],
  ['1EubfSLtbGNF5G2MLS9eT_DiAsVCtv0fM', 'IPTU_2026.csv', 937865216],
  ['1A3NK8K6wAn4ZjGCl5rqb2mCB8j50t0Pl', 'IPTU_2026.csv', 937865216],
  ['1Uvb9CYQNomG00MJo0kLAgOL3F2Xb8ay-', 'IPTU_2026.csv', 937865216],
  ['1lBfWs1FCsxCTgpAu_5WzbZJ8WnLodxi9', 'holdings.csv',   60233422],
  ['1LGUIQysj-1_8deN8AeQi5ChwORjyoWHR', 'holdings.csv',   60233422],
  ['17WdJjyVAg6macYZ9DjM-xIiR5bEFqjQo', 'holdings.csv',   60233422],
  ['1fdabbNncuOexRrmIEvP1N2L-oNyZmk-j', 'holdings.csv',   60233422],
  ['1H3-gburttjEyLYmBBUH1qM7DH1fxUEZL', 'holdings.csv',   60233422]
];

function trashDuplicatas() {
  var apagados = 0, pulados = 0, ganho = 0;
  Logger.log((DRY_RUN ? '[ENSAIO] ' : '[EXCLUINDO] ') + DUPS.length + ' duplicatas');
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

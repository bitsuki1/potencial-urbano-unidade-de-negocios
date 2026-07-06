/**
 * ============================================================================
 *  TRASH QUARENTENA — roda na conta do DONO (eduardo@saobentoservicos.com.br)
 *  PU 18 · 2026-07-06. Passo FINAL do dedup escopado ao Potencial Urbano.
 *
 *  O robô (conta de serviço, Editor) já MOVEU as 2.082 duplicatas para a pasta única
 *  "99 — DUPLICATAS-A-EXCLUIR" (id abaixo) — provado pelo log da Action dedup-quarentena
 *  (run 28803222539): "para_quarentena=2082 erros=0, grupos=417, ~41,52 GB". O robô NÃO pode
 *  mandar arquivo de outro dono para a lixeira (403) — só VOCÊ pode. Este script faz isso:
 *  manda TODOS os filhos da pasta de quarentena para a lixeira. Libera ~41,52 GB.
 *
 *  As 4 canônicas (socios/empresas/IPTU/holdings, em "03 — Tabelas & Engines" 1v4H2Ys...)
 *  NÃO estão nesta pasta — foram verificadas VIVAS e fora da quarentena. Este script só
 *  toca o que está DENTRO da pasta 99, então não há risco de apagar canônica.
 *
 *  COMO USAR: script.google.com > Novo projeto > cole > rode  trashQuarentena  com
 *  DRY_RUN=true, confira o Log (deve listar ~2082), depois DRY_RUN=false e rode de novo.
 *  Depois esvazie a Lixeira do Drive para recuperar o espaço de fato.
 * ============================================================================
 */
var DRY_RUN = true;   // <-- mude para false para EXCLUIR de verdade (manda p/ lixeira)

var QUARENTENA_ID = '1tk7qx26pBLj7p0Gvxx4VNC53LlzdhUcl';  // "99 — DUPLICATAS-A-EXCLUIR"

function trashQuarentena() {
  var pasta;
  try { pasta = DriveApp.getFolderById(QUARENTENA_ID); } catch (e) {
    Logger.log('ERRO: pasta de quarentena ' + QUARENTENA_ID + ' não encontrada (' + e + ')'); return;
  }
  Logger.log((DRY_RUN ? '[ENSAIO] ' : '[EXCLUINDO] ') + 'esvaziando « ' + pasta.getName() + ' »');
  var it = pasta.getFiles();
  var apagados = 0, pulados = 0, ganho = 0;
  while (it.hasNext()) {
    var f = it.next();
    if (f.isTrashed()) { pulados++; continue; }
    var size = f.getSize();
    if (DRY_RUN) {
      if (apagados < 5) Logger.log('DRYRUN trash « ' + f.getName() + ' » (' + size + ' B)');
      apagados++; ganho += size; continue;
    }
    f.setTrashed(true);
    apagados++; ganho += size;
  }
  Logger.log('=== FIM === modo=' + (DRY_RUN ? 'DRYRUN' : 'REAL') +
             ' para_lixeira=' + apagados + ' ja_na_lixeira=' + pulados +
             ' ganho=' + (ganho / 1073741824).toFixed(2) + ' GB');
  if (DRY_RUN) Logger.log('(ensaio: nada foi apagado. Confirme o total ~2082 e rode com DRY_RUN=false.)');
  else Logger.log('(feito. Agora ESVAZIE A LIXEIRA do Drive para recuperar o espaço.)');
}

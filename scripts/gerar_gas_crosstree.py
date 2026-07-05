#!/usr/bin/env python3
"""
gerar_gas_crosstree.py — Gera o Apps Script que QUARENTENA as duplicatas cross-tree (R9).

O reconciliador detecta cópias byte-idênticas ENTRE árvores (_entrada × lago) e emite
`inventario/cross-tree-dups.csv` (hash_md5,canonico_id,dup_id,dup_status,motivo). Estas extras já
foram FISICAMENTE colocadas em pastas-tipo (pelo Organizar/Sanear) — para removê-las sem perder nada,
este script gera `drive-arrumacao/Quarentenar-CrossTree.gs` com os `dup_id` embutidos, que MOVE cada um
para `98 — _LEGADO/_quarentena-<data>` (nunca lixeira). A canônica (maior oficialidade) FICA.

Fecha o loop do R9: detectar (reconciliar) → gerar (aqui) → dono roda o GAS → re-reconciliar (o dup
sai de 'moved' e vira 'quarentena'; o cross-tree-dups.csv esvazia).

Uso:  python3 scripts/gerar_gas_crosstree.py     # lê cross-tree-dups.csv -> emite o .gs (ou avisa que não há dup)
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CROSS = RAIZ / "inventario" / "cross-tree-dups.csv"
SAIDA = RAIZ / "drive-arrumacao" / "Quarentenar-CrossTree.gs"

CABECALHO = '''/**
 * ============================================================================
 *  QUARENTENAR DUPLICATAS CROSS-TREE — POTENCIAL URBANO — GERADO por gerar_gas_crosstree.py
 *  Fecha o R9: move as cópias byte-idênticas (mesmo md5 de uma canônica em outra árvore) para a
 *  quarentena datada. NADA vai para a lixeira; a canônica de maior oficialidade FICA.
 *  DRY_RUN=true por padrão. Rode `quarentenarCrossTree`, confira o Log, DRY_RUN=false, rode de novo.
 *  Depois: re-rode reconciliar_arrumacao.py p/ o índice refletir (dup vira 'quarentena').
 * ============================================================================
 */
var DRY_RUN = true;
var PROJETO_RAIZ_ID = '';                     // id da raiz "Potencial Urbano" (vazio = Meu Drive; avisa)
var QUARENTENA_RAIZ_NOME = '98 — _LEGADO';

// [dup_id, canonico_id, motivo] — gerado do inventario/cross-tree-dups.csv
var DUPS = [
'''

RODAPE = '''];

function _getOrCreatePasta_(mae, nome) {
  var it = mae.getFoldersByName(nome);
  return it.hasNext() ? it.next() : mae.createFolder(nome);
}
function _quarentena_() {
  var mae;
  if (PROJETO_RAIZ_ID) { try { mae = DriveApp.getFolderById(PROJETO_RAIZ_ID); } catch (e) {} }
  if (!mae) { Logger.log('AVISO: PROJETO_RAIZ_ID vazio — quarentena vai sob o Meu Drive.'); mae = DriveApp.getRootFolder(); }
  var data = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd');
  return _getOrCreatePasta_(_getOrCreatePasta_(mae, QUARENTENA_RAIZ_NOME), '_quarentena-cross-' + data);
}
function _pais_(id) { var it = DriveApp.getFileById(id).getParents(), n = 0; while (it.hasNext()) { it.next(); n++; } return n; }

function quarentenarCrossTree() {
  Logger.log('=== QUARENTENAR CROSS-TREE — DRY_RUN=%s — %s dups ===', DRY_RUN, DUPS.length);
  var quarent = _quarentena_(), movidos = 0, multiPai = 0, sumidos = 0;
  Logger.log('CSV_INICIO drive_id,md5,acao,canonico_id');
  for (var i = 0; i < DUPS.length; i++) {
    var did = DUPS[i][0], canon = DUPS[i][1];
    var f; try { f = DriveApp.getFileById(did); f.getName(); } catch (e) { sumidos++; continue; }
    if (_pais_(did) > 1) { Logger.log('CSV_LINHA %s,,MULTI_PAI_MANUAL,%s', did, canon); multiPai++; continue; }
    Logger.log('CSV_LINHA %s,,%s,%s', did, (DRY_RUN ? 'QUARENTENA_DRYRUN' : 'QUARENTENA'), canon);
    if (!DRY_RUN) { try { f.moveTo(quarent); } catch (e) { Logger.log('  ! falha %s: %s', did, e); continue; } }
    movidos++;
  }
  Logger.log('CSV_FIM');
  Logger.log('=== FIM — %s %s p/ quarentena; %s multi-pai; %s sumidos ===',
             (DRY_RUN ? 'moveria' : 'movidos'), movidos, multiPai, sumidos);
}
'''


def _js_str(s):
    return "'" + (s or "").replace("\\", "\\\\").replace("'", "\\'") + "'"


def main():
    if not CROSS.exists() or not (dups := list(csv.DictReader(open(CROSS, encoding="utf-8")))):
        if SAIDA.exists():
            SAIDA.unlink()      # sem dups (arquivo ausente OU vazio) → remove o .gs obsoleto (idempotência)
        print("gerar_gas_crosstree: nenhuma dup cross-tree — nada a gerar "
              "(rode reconciliar_arrumacao.py com os logs do GAS primeiro).")
        return 0
    linhas = ",\n".join(
        f"  [{_js_str(d['dup_id'])}, {_js_str(d['canonico_id'])}, {_js_str(d.get('motivo',''))}]"
        for d in dups)
    SAIDA.write_text(CABECALHO + linhas + "\n" + RODAPE, encoding="utf-8")
    print(f"gerar_gas_crosstree: {len(dups)} dup(s) -> {SAIDA.relative_to(RAIZ)} "
          f"(rode no Apps Script; DRY_RUN primeiro).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

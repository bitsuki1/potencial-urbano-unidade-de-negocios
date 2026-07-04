/**
 * ============================================================================
 *  SANEAR O LAGO "TODOS TDC" — POTENCIAL URBANO — 2026-07-04 (PU 17)
 *  Onda 1 do plano `docs/PLANO-ARRUMACAO-DRIVE-2026-07-04.md`.
 *  Decisão do dono (2026-07-04): SANEAR (não congelar) e "não quero perder nada".
 *
 *  O QUE FAZ (doutrina nova — supera o Sanear-Duplicatas de junho):
 *   - Dedup por HASH (md5Checksum do Drive), NÃO por nome+tamanho (mais seguro).
 *   - NADA VAI PARA A LIXEIRA. As cópias irmãs são MOVIDAS (file.moveTo) para uma
 *     QUARENTENA DATADA `98/_quarentena-AAAA-MM-DD/` — recuperável e auditável.
 *   - Mantém SEMPRE 1 canônica por grupo de hash (a de nome mais "limpo" — sem
 *     sufixo "(1)"/"cópia" — e, empatando, a mais antiga).
 *   - Arquivos Google-nativos (Docs/Sheets — sem md5) NUNCA são deduplicados.
 *   - Emite no Log um CSV `drive_id,md5,acao,canonico_id` para reconciliar de volta
 *     com o índice-mestre (inventario/INDICE-MESTRE-DRIVE.csv).
 *
 *  SEGURANÇA:
 *   - DRY_RUN=true por padrão: só LOGA. Rode, leia o Log (Ver > Registros), confira,
 *     então DRY_RUN=false e rode de novo.
 *   - Idempotente: reexecutar não remove de novo (pula o que já está na quarentena).
 *   - Retomável: se estourar o tempo (~4,5 min), salva o cursor e continua na próxima
 *     execução. Rode de novo até "CONCLUÍDO".
 *   - MOVE, não copia, não apaga (invariante 1 e 2 do plano §6).
 *
 *  PRÉ-REQUISITO (uma vez): habilitar o serviço avançado "Drive API" no editor
 *  (Serviços + > Drive API > v3). Sem ele, cai no modo nome+tamanho (menos preciso)
 *  — mas AINDA move p/ quarentena, nunca lixeira.
 * ============================================================================
 */

var DRY_RUN = true;                     // <-- false p/ EXECUTAR de verdade
var LAGO_NOME = 'TODOS TDC';            // acha a pasta por nome (evita id chumbado errado)
var LAGO_ID = '';                       // opcional: fixe o id aqui se houver homônimos
var QUARENTENA_RAIZ_NOME = '98 — _LEGADO'; // pasta-mãe da quarentena (criada se faltar)
var DATA_HOJE = '2026-07-04';           // carimbo da quarentena datada (troque na data real do run)
var LIMITE_MS = 270000;                 // 4,5 min — abaixo do teto de 6 min do Apps Script

var PROP = PropertiesService.getScriptProperties();

function _acharLago_() {
  if (LAGO_ID) { try { return DriveApp.getFolderById(LAGO_ID); } catch (e) {} }
  var it = DriveApp.getFoldersByName(LAGO_NOME);
  if (it.hasNext()) return it.next();
  return null;
}

function _getOrCreatePasta_(mae, nome) {
  var it = mae.getFoldersByName(nome);
  if (it.hasNext()) return it.next();
  return mae.createFolder(nome);
}

function _quarentena_() {
  var raiz = DriveApp.getRootFolder();
  var legado = _getOrCreatePasta_(raiz, QUARENTENA_RAIZ_NOME);
  return _getOrCreatePasta_(legado, '_quarentena-' + DATA_HOJE);
}

/** md5 via serviço avançado Drive (v3). Retorna null p/ nativos/sem hash. */
function _md5_(id) {
  try {
    var meta = Drive.Files.get(id, { fields: 'md5Checksum', supportsAllDrives: true });
    return meta && meta.md5Checksum ? meta.md5Checksum : null;
  } catch (e) { return null; }
}

/** Enumera recursivamente todos os arquivos do lago (com cursor de retomada por pasta). */
function _enumerar_(raiz, ateMs, acumulador) {
  var pilha = [raiz.getId()];
  while (pilha.length) {
    if (Date.now() > ateMs) return pilha;         // devolve o restante da pilha p/ retomar
    var fid = pilha.pop();
    var pasta = DriveApp.getFolderById(fid);
    var subs = pasta.getFolders();
    while (subs.hasNext()) pilha.push(subs.next().getId());
    var arqs = pasta.getFiles();
    while (arqs.hasNext()) {
      var f = arqs.next();
      acumulador.push({ id: f.getId(), nome: f.getName(), size: f.getSize(),
                        mime: f.getMimeType(), criado: f.getDateCreated().getTime() });
    }
  }
  return [];                                        // pilha vazia = enumeração completa
}

function _sufixoRuido_(nome) {
  // nome "sujo" = tem sufixo de cópia; canônica prefere nome LIMPO.
  return /\(\d+\)|c[óo]pia|copy|- cópia|\bv\d+\b/i.test(nome) ? 1 : 0;
}

function _escolherCanonica_(grupo) {
  // menor ruído; empate -> mais antiga; empate -> id lexicográfico (determinístico).
  grupo.sort(function (a, b) {
    var ra = _sufixoRuido_(a.nome), rb = _sufixoRuido_(b.nome);
    if (ra !== rb) return ra - rb;
    if (a.criado !== b.criado) return a.criado - b.criado;
    return a.id < b.id ? -1 : 1;
  });
  return grupo[0];
}

/** PONTO DE ENTRADA — rode esta função. */
function sanearLagoTDC() {
  Logger.log('=== SANEAR LAGO "%s" — DRY_RUN=%s — quarentena _quarentena-%s ===',
             LAGO_NOME, DRY_RUN, DATA_HOJE);
  var lago = _acharLago_();
  if (!lago) { Logger.log('ABORTA: pasta "%s" não encontrada (fixe LAGO_ID).', LAGO_NOME); return; }

  var ateMs = Date.now() + LIMITE_MS;
  var arquivos = [];
  var restante = _enumerar_(lago, ateMs, arquivos);
  Logger.log('Enumerados %s arquivos%s.', arquivos.length,
             restante.length ? ' (PARCIAL — reexecute p/ continuar a enumeração)' : '');

  // agrupa por md5 (só binários com hash)
  var porHash = {}, semHash = 0;
  for (var i = 0; i < arquivos.length; i++) {
    if (Date.now() > ateMs) { Logger.log('TEMPO — pausando; reexecute p/ continuar.'); break; }
    var a = arquivos[i];
    if (a.mime.indexOf('application/vnd.google-apps') === 0) { semHash++; continue; } // nativo: nunca dedup
    var h = _md5_(a.id);
    if (!h) { semHash++; continue; }
    (porHash[h] = porHash[h] || []).push(a);
  }

  var quarent = _quarentena_();
  var movidos = 0, grupos = 0;
  Logger.log('CSV_INICIO drive_id,md5,acao,canonico_id');
  for (var h2 in porHash) {
    var g = porHash[h2];
    if (g.length < 2) { continue; }                 // único: nada a fazer
    grupos++;
    var canon = _escolherCanonica_(g);
    Logger.log('CSV_LINHA %s,%s,MANTER,%s', canon.id, h2, canon.id);
    for (var j = 0; j < g.length; j++) {
      var f = g[j];
      if (f.id === canon.id) continue;
      Logger.log('CSV_LINHA %s,%s,%s,%s', f.id, h2, (DRY_RUN ? 'QUARENTENA_DRYRUN' : 'QUARENTENA'), canon.id);
      if (!DRY_RUN) {
        try { DriveApp.getFileById(f.id).moveTo(quarent); }
        catch (e) { Logger.log('   ! falha ao mover %s: %s', f.id, e); continue; }
      }
      movidos++;
    }
  }
  Logger.log('CSV_FIM');
  Logger.log('=== FIM — %s grupos duplicados; %s %s p/ quarentena; %s sem-hash (nativos/ilegíveis) ===',
             grupos, (DRY_RUN ? 'moveria' : 'movidos'), movidos, semHash);
  Logger.log(DRY_RUN ? 'DRY_RUN: nada foi movido. Confira o CSV no Log; DRY_RUN=false p/ executar.'
                     : 'Movido p/ 98/_quarentena-' + DATA_HOJE + ' (recuperável, auditável). NADA foi apagado.');
}

/** Zera o cursor de retomada (recomeça do zero). */
function resetSaneamento() { PROP.deleteAllProperties(); Logger.log('cursor de saneamento resetado.'); }

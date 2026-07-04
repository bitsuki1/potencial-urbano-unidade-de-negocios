/**
 * ============================================================================
 *  SANEAR O LAGO "TODOS TDC" — POTENCIAL URBANO — 2026-07-04 (PU 17)
 *  Onda 1 do plano `docs/PLANO-ARRUMACAO-DRIVE-2026-07-04.md`.
 *  Decisão do dono (2026-07-04): SANEAR (não congelar) e "não quero perder nada".
 *  Revisado pela lente adversarial de segurança (achados F1–F10 incorporados).
 *
 *  ESCOPO (só isto): DEDUPLICAR por hash. Mover as CÓPIAS IRMÃS idênticas para uma
 *  QUARENTENA DATADA. NÃO organiza por tipo (isso é a onda 3 / Organizar-Entrada) —
 *  a canônica FICA onde está; só as duplicatas exatas saem.
 *
 *  GARANTIAS (perda zero no caminho normal):
 *   - Dedup por HASH (md5Checksum), nunca por nome+tamanho (não confunde arquivos
 *     de mesmo nome/tamanho e conteúdo diferente).
 *   - NADA vai para a lixeira. Irmãs → `98 — _LEGADO/_quarentena-AAAA-MM-DD/` (move, recuperável).
 *   - A canônica (grupo[0]) NUNCA é movida.
 *   - Só deduplica APÓS enumerar E hashear TUDO (trava F5) — nunca sobre grupo incompleto.
 *   - Arquivo com MÚLTIPLOS PAIS não é movido (F3): vai para o CSV como MULTI_PAI_MANUAL
 *     (decisão humana em `99`), para não arrancá-lo de uma pasta boa.
 *   - RETOMÁVEL DE VERDADE (F1): os md5 já calculados ficam num cache JSON no Drive
 *     (`98 — _LEGADO/_saneamento-cache.json`); re-execução pula o que já hasheou.
 *
 *  PRÉ-REQUISITO (uma vez): Serviços + > Drive API > v3. Sem ele o script ABORTA (F2)
 *  com mensagem clara — NÃO finge "0 duplicados".
 *
 *  COMO RODAR:
 *   1. DRY_RUN=true (padrão). Rode `sanearLagoTDC`. Leia o Log (Ver > Registros).
 *   2. Se disser "hashing incompleto, reexecute", rode de novo até "ENUM+HASH COMPLETOS".
 *   3. Confira o CSV no Log. DRY_RUN=false e rode de novo p/ mover de verdade.
 * ============================================================================
 */

var DRY_RUN = true;                          // <-- false p/ EXECUTAR de verdade
var LAGO_NOME = 'TODOS TDC';                 // acha a pasta por nome
var LAGO_ID = '';                            // opcional: fixe o id se houver homônimos
var QUARENTENA_RAIZ_NOME = '98 — _LEGADO';   // pasta-mãe (criada se faltar) — DEVE ficar FORA do lago
var PROJETO_RAIZ_ID = '';                    // R14: id da raiz "Potencial Urbano"; vazio = Meu Drive (avisa)
var CACHE_NOME = '_saneamento-cache.json';   // cache de md5 (retomada real)
var LIMITE_MS = 270000;                      // 4,5 min (teto do Apps Script é 6)

/** md5 via serviço avançado Drive (v3). Retorna null p/ nativos/sem hash. */
function _md5_(id) {
  try {
    var meta = Drive.Files.get(id, { fields: 'md5Checksum', supportsAllDrives: true });
    return meta && meta.md5Checksum ? meta.md5Checksum : null;
  } catch (e) { return null; }
}

function _acharLago_() {
  if (LAGO_ID) { try { return DriveApp.getFolderById(LAGO_ID); } catch (e) {} }
  var it = DriveApp.getFoldersByName(LAGO_NOME);
  return it.hasNext() ? it.next() : null;
}

function _getOrCreatePasta_(mae, nome) {
  var it = mae.getFoldersByName(nome);
  return it.hasNext() ? it.next() : mae.createFolder(nome);
}

function _legado_() {
  // R14 — ancora a quarentena sob a raiz do PROJETO, não sob o Meu Drive inteiro (vazamento de escopo).
  var mae;
  if (PROJETO_RAIZ_ID) { try { mae = DriveApp.getFolderById(PROJETO_RAIZ_ID); } catch (e) {} }
  if (!mae) { Logger.log('AVISO (R14): PROJETO_RAIZ_ID vazio — quarentena vai sob o Meu Drive. Fixe o id da raiz.'); mae = DriveApp.getRootFolder(); }
  return _getOrCreatePasta_(mae, QUARENTENA_RAIZ_NOME);
}

function _quarentena_() {
  var data = Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd'); // F7
  return _getOrCreatePasta_(_legado_(), '_quarentena-' + data);
}

/** F8 — a quarentena/legado NÃO pode ser descendente do lago (senão movidos re-entram na enumeração). */
function _validarEscopo_(lago, legado) {
  var p = legado.getParents();
  while (p.hasNext()) { if (p.next().getId() === lago.getId()) return false; }
  return legado.getId() !== lago.getId();
}

// ---- cache de md5 (retomada real, F1) ----
function _cacheFile_() {
  var leg = _legado_();
  var it = leg.getFilesByName(CACHE_NOME);
  return it.hasNext() ? it.next() : leg.createFile(CACHE_NOME, '{}', 'application/json');
}
function _carregarCache_() {
  try { return JSON.parse(_cacheFile_().getBlob().getDataAsString()); } catch (e) { return {}; }
}
function _salvarCache_(c) { _cacheFile_().setContent(JSON.stringify(c)); }

/** Enumera recursivamente todos os arquivos do lago (barato; roda inteiro a cada run). */
function _enumerar_(raiz) {
  var pilha = [raiz.getId()], out = [];
  while (pilha.length) {
    var pasta = DriveApp.getFolderById(pilha.pop());
    var subs = pasta.getFolders();
    while (subs.hasNext()) pilha.push(subs.next().getId());
    var arqs = pasta.getFiles();
    while (arqs.hasNext()) {
      var f = arqs.next();
      out.push({ id: f.getId(), nome: f.getName(), size: f.getSize(),
                 mime: f.getMimeType(), criado: f.getDateCreated().getTime() });
    }
  }
  return out;
}

function _sufixoRuido_(nome) { return /\(\d+\)|c[óo]pia|copy/i.test(nome) ? 1 : 0; }

function _escolherCanonica_(grupo) {
  // Irmãs têm md5 IDÊNTICO (byte-a-byte): a escolha é cosmética (não há perda).
  // menor ruído de nome → mais antiga → id (determinístico).
  grupo.sort(function (a, b) {
    var ra = _sufixoRuido_(a.nome), rb = _sufixoRuido_(b.nome);
    if (ra !== rb) return ra - rb;
    if (a.criado !== b.criado) return a.criado - b.criado;
    return a.id < b.id ? -1 : 1;
  });
  return grupo[0];
}

function _pais_(id) {
  var it = DriveApp.getFileById(id).getParents(), n = 0;
  while (it.hasNext()) { it.next(); n++; }
  return n;
}

/** PONTO DE ENTRADA — rode esta função. */
function sanearLagoTDC() {
  // F2 — sem o serviço avançado, ABORTA (não finge "0 duplicados").
  if (typeof Drive === 'undefined' || !Drive.Files) {
    Logger.log('ABORTA (F2): serviço avançado "Drive API" v3 não está ligado. '
             + 'Editor > Serviços + > Drive API > adicionar. Sem ele NÃO é seguro deduplicar.');
    return;
  }
  var lago = _acharLago_();
  if (!lago) { Logger.log('ABORTA: pasta "%s" não encontrada (fixe LAGO_ID).', LAGO_NOME); return; }
  var quarent = _quarentena_();
  if (!_validarEscopo_(lago, _legado_())) {
    Logger.log('ABORTA (F8): a quarentena "%s" está DENTRO do lago — mova-a p/ fora antes.', QUARENTENA_RAIZ_NOME);
    return;
  }
  Logger.log('=== SANEAR LAGO "%s" — DRY_RUN=%s ===', LAGO_NOME, DRY_RUN);

  var ateMs = Date.now() + LIMITE_MS;
  var arquivos = _enumerar_(lago);                 // enumeração é barata; roda inteira
  Logger.log('Enumerados %s arquivos no lago.', arquivos.length);

  // ---- hashing com cache (F1): pula o que já foi hasheado; para no orçamento ----
  var cache = _carregarCache_();
  var nativos = 0, faltam = 0, hasheadosAgora = 0;
  for (var i = 0; i < arquivos.length; i++) {
    var a = arquivos[i];
    if (a.mime.indexOf('application/vnd.google-apps') === 0) { nativos++; continue; } // F9: nativo ≠ falha
    if (cache[a.id] !== undefined) continue;       // já hasheado numa run anterior
    if (Date.now() > ateMs) { faltam++; continue; } // sem orçamento agora
    cache[a.id] = _md5_(a.id);                      // string md5 ou null (binário sem hash)
    hasheadosAgora++;
    if (hasheadosAgora % 50 === 0) _salvarCache_(cache); // persiste em lotes
  }
  _salvarCache_(cache);
  // faltam = binários ainda não hasheados nesta run (orçamento estourou)
  var pendentes = arquivos.filter(function (a) {
    return a.mime.indexOf('application/vnd.google-apps') !== 0 && cache[a.id] === undefined; }).length;
  if (pendentes > 0) {                              // F5 — NÃO deduplica sobre hashing incompleto
    Logger.log('Hashing INCOMPLETO: %s hasheados nesta run, %s binários pendentes. '
             + 'REEXECUTE p/ continuar (o cache guarda o progresso).', hasheadosAgora, pendentes);
    return;
  }
  Logger.log('ENUM+HASH COMPLETOS: %s arquivos, %s nativos (não-dedup).', arquivos.length, nativos);

  // ---- dedup por md5 (só agora, com tudo hasheado) ----
  var porHash = {}, semHashBin = 0;
  for (var k = 0; k < arquivos.length; k++) {
    var f = arquivos[k];
    if (f.mime.indexOf('application/vnd.google-apps') === 0) continue;
    var h = cache[f.id];
    if (!h) { semHashBin++; continue; }            // binário que a API não hasheou (raro) — não dedup
    (porHash[h] = porHash[h] || []).push(f);
  }

  var movidos = 0, grupos = 0, multiPai = 0;
  Logger.log('CSV_INICIO drive_id,md5,acao,canonico_id');
  for (var h2 in porHash) {
    var g = porHash[h2];
    if (g.length < 2) continue;
    grupos++;
    var canon = _escolherCanonica_(g);
    Logger.log('CSV_LINHA %s,%s,MANTER,%s', canon.id, h2, canon.id);
    for (var j = 0; j < g.length; j++) {
      var d = g[j];
      if (d.id === canon.id) continue;
      if (_pais_(d.id) > 1) {                       // F3 — multi-pai: não arranca de pasta boa
        Logger.log('CSV_LINHA %s,%s,MULTI_PAI_MANUAL,%s', d.id, h2, canon.id);
        multiPai++; continue;
      }
      Logger.log('CSV_LINHA %s,%s,%s,%s', d.id, h2, (DRY_RUN ? 'QUARENTENA_DRYRUN' : 'QUARENTENA'), canon.id);
      if (!DRY_RUN) {
        try { DriveApp.getFileById(d.id).moveTo(quarent); }
        catch (e) { Logger.log('   ! falha ao mover %s: %s', d.id, e); continue; }
      }
      movidos++;
    }
  }
  Logger.log('CSV_FIM');
  Logger.log('=== FIM — %s grupos duplicados; %s %s p/ quarentena; %s multi-pai p/ decisão manual (99); '
           + '%s binários sem-hash ===', grupos, (DRY_RUN ? 'moveria' : 'movidos'), movidos, multiPai, semHashBin);
  Logger.log(DRY_RUN ? 'DRY_RUN: nada movido. Confira o CSV; DRY_RUN=false p/ executar.'
                     : 'Movido p/ 98/_quarentena-* (recuperável, auditável). NADA foi apagado.');
}

/** Zera SÓ o cache/cursor deste saneamento (F10 — não toca props de outros scripts). */
function resetSaneamento() {
  var leg = _legado_(), it = leg.getFilesByName(CACHE_NOME);
  while (it.hasNext()) it.next().setTrashed(true);
  Logger.log('cache de saneamento (%s) resetado.', CACHE_NOME);
}

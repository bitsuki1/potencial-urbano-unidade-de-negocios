/**
 * ============================================================================
 *  SANEAR SUFIXO " (N)" + RUÍDO DE SESSÃO — POTENCIAL URBANO (IPTU / TDC)
 *  Companion do Sanear-Duplicatas-PotencialUrbano.gs. Trazido pelo Escritório
 *  do MOU — 2026-06-28 (varredura completa do Drive a pedido do MOU).
 *
 *  POR QUE EXISTE (o gap que o Sanear-Duplicatas NÃO cobre):
 *   - A FASE 1 daquele script apaga os ARQUIVÕES dup por ID (socios/empresas/
 *     IPTU_2026/holdings — ver LISTA-APAGAR-script.csv, ~7 GB).
 *   - A FASE 2 dedupa por NOME IDÊNTICO + tamanho.
 *   - MAS o Drive, ao re-subir um arquivo de mesmo nome, cria "nome (1).ext",
 *     "nome (2).ext" — NOME DIFERENTE do original. A FASE 2 NÃO pega isso.
 *     Estes são os dezenas de `stf-tema-1084 (1).txt`, `stf-sumula-589 (2)`, etc.
 *   - E há "ruído de sessão": notas de saída de IA salvas como .txt no despejo
 *     (`## Extração concluída…`, `Todas as 7 páginas renderizaram…`).
 *
 *  O QUE FAZ: manda para a LIXEIRA (recuperável ~30 dias) (a) cópias com sufixo
 *  " (N)" QUANDO o original existe E tem o MESMO tamanho; (b) arquivos de ruído
 *  de sessão. SEMPRE preserva o original.
 *
 *  SEGURANÇA (AUD-02):
 *   - DRY_RUN=true por padrão: só LOGA. Rode 1×, leia o Log (Ver > Execuções/
 *     Logs), confira, então mude para false e rode de novo p/ executar.
 *   - Sufixo " (N)" só vira lixeira se o ORIGINAL (sem o sufixo) existir E o
 *     tamanho BATER. Tamanho diferente = versão diferente → marca INCERTO, NÃO apaga.
 *   - Original sem par claro → INCERTO, NÃO apaga.
 *   - Ruído: só títulos que casam padrões EXPLÍCITOS e pequenos (.txt). Nomes
 *     truncados/ambíguos (`s.txt`, `r que.txt`) → INCERTO, NÃO apaga.
 *   - Ignora arquivos Google-nativos (tamanho não confiável) e NUNCA mexe em
 *     shapefiles/PDF/CSV de norma (não casam os padrões).
 *   - RECURSE=true varre subpastas; o critério é o mesmo (sufixo/ruído).
 * ============================================================================
 */

var DRY_RUN   = true;   // <-- mude para false p/ EXECUTAR de verdade
var RECURSE   = true;   // varrer subpastas também
var DESPEJO_ID = '1grhqYgttj7KnJmiu9U73z-lXFHnFthov';  // pasta-mãe do despejo do PU

// Padrões de RUÍDO DE SESSÃO (nota de saída de IA, não documento). Conservador.
var RUIDO_REGEX = /(renderizaram|Extração concluída|arquivos gerados|baixados com sucesso|foram baixados)/i;
var RUIDO_PREFIXO = '#';            // título começa com '#'/'##'
var RUIDO_TAM_MAX = 20000;         // só trata como ruído se for pequeno (<20 KB)

// Regex do sufixo do Drive: "base (N).ext"  ou  "base (N)"  (N = dígitos).
var SUFIXO_REGEX = /^(.*?) \((\d+)\)(\.[^.\/]+)?$/;

function _vivo(id) { try { var f = DriveApp.getFileById(id); f.getName(); return f; } catch (e) { return null; } }

// Coleta todos os arquivos da pasta (e subpastas se RECURSE) -> [{file, name, size, mime}].
function _coletar_(folder, acc) {
  var it = folder.getFiles();
  while (it.hasNext()) {
    var f = it.next();
    acc.push({ file: f, name: f.getName(), size: (f.getMimeType().indexOf('application/vnd.google-apps') === 0 ? -1 : f.getSize()), mime: f.getMimeType() });
  }
  if (RECURSE) {
    var sub = folder.getFolders();
    while (sub.hasNext()) _coletar_(sub.next(), acc);
  }
  return acc;
}

// FASE 3 — duplicatas com sufixo " (N)" (Drive auto-rename) cujo original existe c/ mesmo tamanho.
function sanearFase3_sufixoN_(arquivos) {
  // index por (nome|tamanho) e por nome -> existe original?
  var porNomeTam = {}, porNome = {};
  arquivos.forEach(function (a) {
    porNomeTam[a.name + '|' + a.size] = true;
    (porNome[a.name] = porNome[a.name] || []).push(a);
  });
  var apaga = 0, incerto = 0;
  arquivos.forEach(function (a) {
    var m = SUFIXO_REGEX.exec(a.name);
    if (!m) return;                                  // não tem sufixo " (N)"
    if (a.size < 0) return;                           // Google-nativo: pula
    var base = m[1] + (m[3] || '');                  // "stf-tema-1084" + ".txt"
    if (!porNome[base]) { Logger.log('   ? INCERTO (sufixo sem original): %s — NÃO apago', a.name); incerto++; return; }
    if (!porNomeTam[base + '|' + a.size]) { Logger.log('   ? INCERTO (original existe mas TAMANHO difere): %s — NÃO apago', a.name); incerto++; return; }
    if (DRY_RUN) Logger.log('   - [DRY-RUN] APAGARIA dup "%s" (orig "%s", %s B) id=%s', a.name, base, a.size, a.file.getId());
    else { a.file.setTrashed(true); Logger.log('   - LIXEIRA dup: %s (orig %s) id=%s', a.name, base, a.file.getId()); }
    apaga++;
  });
  Logger.log('FASE 3 (sufixo " (N)"): %s %s; %s incertos (preservados).', (DRY_RUN ? 'apagaria' : 'apagou'), apaga, incerto);
  return apaga;
}

// FASE 4 — ruído de sessão (nota de saída de IA salva como .txt). Conservador.
function sanearFase4_ruido_(arquivos) {
  var apaga = 0;
  arquivos.forEach(function (a) {
    if (a.size < 0 || a.size > RUIDO_TAM_MAX) return;
    var ehRuido = (a.name.charAt(0) === RUIDO_PREFIXO) || RUIDO_REGEX.test(a.name);
    if (!ehRuido) return;
    if (DRY_RUN) Logger.log('   - [DRY-RUN] APAGARIA ruído "%s" (%s B) id=%s', a.name, a.size, a.file.getId());
    else { a.file.setTrashed(true); Logger.log('   - LIXEIRA ruído: %s id=%s', a.name, a.file.getId()); }
    apaga++;
  });
  Logger.log('FASE 4 (ruído de sessão): %s %s.', (DRY_RUN ? 'apagaria' : 'apagou'), apaga);
  return apaga;
}

/** PONTO DE ENTRADA — rode esta função. */
function sanearSufixoNeRuido() {
  Logger.log('=== SANEAR SUFIXO " (N)" + RUÍDO — DRY_RUN=%s, RECURSE=%s ===', DRY_RUN, RECURSE);
  var raiz = _vivo(DESPEJO_ID);
  if (!raiz) { Logger.log('ABORTA: despejo %s não acessível.', DESPEJO_ID); return; }
  var arquivos = _coletar_(DriveApp.getFolderById(DESPEJO_ID), []);
  Logger.log('Varridos %s arquivos (RECURSE=%s).', arquivos.length, RECURSE);
  var t = sanearFase3_sufixoN_(arquivos) + sanearFase4_ruido_(arquivos);
  Logger.log('=== FIM — total %s %s. %s ===', (DRY_RUN ? 'a apagar' : 'apagados'), t,
             (DRY_RUN ? 'Confira o Log; mude DRY_RUN=false e rode de novo p/ executar.' : 'Recuperável na Lixeira do Drive ~30 dias.'));
}

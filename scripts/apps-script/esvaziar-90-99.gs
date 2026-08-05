/**
 * esvaziar-90-99.gs — Apps Script para ESVAZIAR as pastas "90 — Material bruto (só ideias)"
 * e "99 — APAGAR (duplicados e descarte)" da POTENCIAL URBANO.
 *
 * Move o CONTEÚDO dessas pastas para a LIXEIRA do Drive (reversível por ~30 dias) —
 * não faz delete permanente. As pastas em si ficam (vazias). Ao final, o selo do robô
 * volta a mostrar 90=0 e 99=0, destravando o "índice-mestre pós-exclusão".
 *
 * COMO USAR:
 *  1. Abra https://script.google.com → Novo projeto → cole este arquivo.
 *  2. Rode a função `contar()` primeiro (menu Executar). Autorize o acesso ao Drive.
 *     Veja no Log (Ctrl+Enter) quantos arquivos há em cada pasta e se achou as pastas certas.
 *  3. Confirmados os números, rode `esvaziar()`. Ele move o conteúdo para a lixeira em lotes,
 *     logando o progresso. Pode rodar de novo se o tempo de execução estourar (6 min) — é
 *     retomável (só sobra o que ainda não foi para a lixeira).
 *  4. (Opcional) para excluir de vez, esvazie a lixeira do Drive depois — aí sim é definitivo.
 */

// Nomes EXATOS das pastas (conforme o selo do robô). Ajuste aqui se o nome no seu Drive diferir.
var NOMES_ALVO = [
  '90 — Material bruto (só ideias)',
  '99 — APAGAR (duplicados e descarte)'
];

function _acharPastas_() {
  var achadas = [];
  for (var i = 0; i < NOMES_ALVO.length; i++) {
    var it = DriveApp.getFoldersByName(NOMES_ALVO[i]);
    var n = 0;
    while (it.hasNext()) {
      var f = it.next();
      achadas.push(f);
      n++;
      Logger.log('achei: "%s"  (id %s)', f.getName(), f.getId());
    }
    if (n === 0) Logger.log('AVISO: nenhuma pasta com o nome exato "%s"', NOMES_ALVO[i]);
    if (n > 1)  Logger.log('AVISO: %s pastas com o nome "%s" — confira os ids antes de esvaziar', n, NOMES_ALVO[i]);
  }
  return achadas;
}

/** Passo 1 — só CONTA (não move nada). */
function contar() {
  var pastas = _acharPastas_();
  var total = 0;
  for (var i = 0; i < pastas.length; i++) {
    var c = 0;
    var it = pastas[i].getFiles();
    while (it.hasNext()) { it.next(); c++; }
    Logger.log('  "%s": %s arquivos (filhos diretos)', pastas[i].getName(), c);
    total += c;
  }
  Logger.log('TOTAL a mover para a lixeira: %s arquivos. Rode esvaziar() para executar.', total);
}

/** Passo 2 — MOVE o conteúdo para a lixeira (reversível). Retomável. */
function esvaziar() {
  var pastas = _acharPastas_();
  var movidos = 0;
  var LIMITE_TEMPO_MS = 5 * 60 * 1000; // para antes dos 6 min do Apps Script
  var inicio = new Date().getTime();
  for (var i = 0; i < pastas.length; i++) {
    var it = pastas[i].getFiles();
    while (it.hasNext()) {
      if (new Date().getTime() - inicio > LIMITE_TEMPO_MS) {
        Logger.log('PAUSA por tempo — %s movidos até agora. Rode esvaziar() de novo p/ continuar.', movidos);
        return;
      }
      var arq = it.next();
      arq.setTrashed(true); // vai para a lixeira do Drive (recuperável)
      movidos++;
      if (movidos % 200 === 0) Logger.log('  ... %s movidos', movidos);
    }
    Logger.log('pasta "%s" esvaziada.', pastas[i].getName());
  }
  Logger.log('FIM: %s arquivos movidos para a lixeira. (Esvazie a lixeira do Drive p/ excluir de vez.)', movidos);
}

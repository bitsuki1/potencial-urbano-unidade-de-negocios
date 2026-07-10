/**
 * Potencial Urbano — sobe arquivos do Google Drive para o Supabase Storage.
 * FASE A (oficiais, primeira leva: arquivos PEQUENOS < ~45 MB).
 *
 * COMO USAR (1 vez):
 *  1) Pegue sua chave: Supabase > Project Settings > API > "service_role" (secret).
 *     -> É uma chave de acesso TOTAL. NUNCA compartilhe, não cole em e-mail/chat, não suba no git.
 *  2) script.google.com > Novo projeto > cole este arquivo inteiro.
 *  3) Preencha SERVICE_KEY abaixo.
 *  4) Rode a função  subirParaSupabase  (botão ▶). Autorize o acesso ao Drive quando pedir.
 *  5) Veja o resultado em  Ver > Registros (Logs). Espera-se "HTTP 200" em cada linha.
 *
 * Arquivos GRANDES (IPTU_2026 937MB, série ITBI, shapefiles, socios/empresas) NÃO vão por aqui
 * (o Apps Script trava em ~50MB / 6min). Esses vão por outro caminho — o Claude te passa depois.
 */

const SUPABASE_URL = 'https://csnalylpvysjvejgsymr.supabase.co';
const SERVICE_KEY  = 'COLE_AQUI_SUA_SERVICE_ROLE_KEY';   // <-- Supabase > Settings > API > service_role (SECRETO)

// Lista de oficiais PEQUENAS (drive_id -> destino no balde 'dados-produto/oficiais/')
const ARQUIVOS = [
  { driveId: '1Q499wCFws3H1d3w0jY1PFYOkCD5PjieF', dest: 'q14/ano=2025/Atualizacacao_Q14_anoref2025.csv' },        // Quadro 14 (valor m2, vigente 2025)
  { driveId: '1KPeSlCXVtWyuFr52gr0Wg4uzPqymbVaD', dest: 'q14/ano=2013/PDE2013_SUBST2_Quadro_14_cadastro.csv' },     // Quadro 14 (base histórica)
  { driveId: '17j94xkgVk4eberaRpRLK2j_ekz480Lny', dest: 'zepec-bir/ano=2025-08/lista_declaracoes_ZEPEC-BIR_agosto-2025.xlsx' },
  { driveId: '1en2WC2A-Wd21NNDhZ8ThheAyHmODIOl-', dest: 'zepec-bir/ano=2025-08/lista_certidao_ZEPEC-BIR_agosto-2025.xlsx' },
  { driveId: '1_w_WLS1P6QXsgBLF50roxL4gZ8vZzjIM', dest: 'outorga-onerosa/ano=2002-2014/oo_2002-2014.xlsx' },                          // Outorga Onerosa
  { driveId: '1Z04ZHyuy0epwhg10SsVTAoZwG5cmiaK1', dest: 'outorga-onerosa/ano=2014-2023/oo_2014-2023.xlsx' },
  { driveId: '1IvHck6ce6VwuSHd_EWVa9RmnJW0nWF8j', dest: 'outorga-onerosa/ano=2024-2025/OODC_2024-2025.xlsx' },                        // OODC detalhada (proprietário)
  { driveId: '1ifKnqSFZcNF8zdc-CHpUfj56NyY-DlZE', dest: 'outorga-onerosa/ano=consolidado/OUTORGA_ONEROSA.xlsx' },
  { driveId: '17AgTa3aSavPSZyhkzq8cUClOHpYamT94', dest: 'alvaras/ano=2022/ANUAL-2022-alvaras.xlsx' },                    // Alvarás (proprietário + SQL)
  { driveId: '1rN_fsOefqdvDU8icHG-ptHGMemzX72NA', dest: 'fundurb/ano=2025-12/fila_tdc_5pct_fundurb_dez2025.csv' },
];

const BUCKET = 'dados-produto';
const PASTA  = 'oficiais/';
const LIMITE_BYTES = 45 * 1024 * 1024; // 45 MB

function subirParaSupabase() {
  if (SERVICE_KEY.indexOf('COLE_AQUI') === 0) {
    Logger.log('!! Preencha SERVICE_KEY antes de rodar.');
    return;
  }
  let ok = 0, falhou = 0, pulou = 0;
  ARQUIVOS.forEach(function (a) {
    try {
      const file = DriveApp.getFileById(a.driveId);
      const blob = file.getBlob();
      const bytes = blob.getBytes().length;
      if (bytes > LIMITE_BYTES) {
        pulou++;
        Logger.log('PULADO (%s MB, grande p/ Apps Script): %s', Math.round(bytes / 1048576), a.dest);
        return;
      }
      const url = SUPABASE_URL + '/storage/v1/object/' + BUCKET + '/' + encodeURIComponent(PASTA + a.dest);
      const resp = UrlFetchApp.fetch(url, {
        method: 'post',
        contentType: blob.getContentType() || 'application/octet-stream',
        headers: { Authorization: 'Bearer ' + SERVICE_KEY, 'x-upsert': 'true' },
        payload: blob.getBytes(),
        muteHttpExceptions: true,
      });
      const code = resp.getResponseCode();
      if (code >= 200 && code < 300) { ok++; Logger.log('OK  %s  (HTTP %s)', a.dest, code); }
      else { falhou++; Logger.log('FALHA %s  HTTP %s: %s', a.dest, code, resp.getContentText().slice(0, 160)); }
    } catch (e) {
      falhou++;
      Logger.log('ERRO %s: %s', a.dest, e.message);
    }
  });
  Logger.log('--- FIM: %s OK, %s falha, %s pulado ---', ok, falhou, pulou);
}

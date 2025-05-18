const { exec } = require("child_process");
const path = require("path");

// Função para executar comandos no terminal
function executeCommand(command) {
  return new Promise((resolve, reject) => {
    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Erro: ${error}`);
        reject(error);
        return;
      }
      resolve(stdout);
    });
  });
}

// Função principal que será executada a cada 5 minutos
async function main() {
  try {
    // Executa o index.js
    console.log("Executando index.js...");
    await executeCommand("node index.js");

    // Espera 30 segundos
    console.log("Aguardando 30 segundos...");
    await new Promise((resolve) => setTimeout(resolve, 30000));

    // Comandos do Git
    console.log("Realizando commit e push...");
    await executeCommand("git add .");
    await executeCommand('git commit -m "feat(MESSAGES): Ranking update"');
    await executeCommand("git push");

    console.log("Processo completado com sucesso!\n");
  } catch (error) {
    console.error("Erro durante o processo:", error);
  }
}

// Executa imediatamente pela primeira vez
main();

// Agenda a execução para cada 5 minutos (300000 ms)
setInterval(main, 300000);

const { exec } = require("child_process");

exec("node index.js", (err, stdout, stderr) => {
  if (err) {
    console.error("Erro ao executar index.js:", err);
    return;
  }
  console.log("index.js executado com sucesso.");
  console.log(stdout);

  exec("git add .", (err) => {
    if (err) {
      console.error("Erro no git add:", err);
      return;
    }
    console.log("git add concluído.");

    exec('git commit -m "update(messages.txt)"', (err, stdout) => {
      if (err) {
        console.error("Erro no git commit:", err);
        return;
      }
      console.log("git commit realizado.");
      console.log(stdout);

      exec("git push", (err, stdout) => {
        if (err) {
          console.error("Erro no git push:", err);
          return;
        }
        console.log("git push concluído.");
        console.log(stdout);
      });
    });
  });
});

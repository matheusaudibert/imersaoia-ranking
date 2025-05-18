const { Client } = require("discord.js-selfbot-v13");
require("dotenv").config();

const client = new Client({
  checkUpdate: false,
});

client.on("ready", async () => {
  console.log(`Logado como ${client.user.tag}`);

  try {
    const channel = await client.channels.fetch("1369193716434337849");
    console.log("Coletando mensagens...");

    const messages = [];
    let lastId;

    while (true) {
      const options = { limit: 100 };
      if (lastId) {
        options.before = lastId;
      }

      const fetchedMessages = await channel.messages.fetch(options);

      if (fetchedMessages.size === 0) break;

      fetchedMessages.forEach((msg) => {
        if (msg.embeds && msg.embeds.length > 0) {
          msg.embeds.forEach((embed) => {
            let content = [];

            // Processa os campos da embed
            if (embed.fields) {
              let nome = "";
              let desc = [];
              let discord = "";

              embed.fields.forEach((field) => {
                if (field.name === "Nome") {
                  nome = field.value;
                } else if (field.name === "Descrição do projeto") {
                  desc.push(field.value);
                } else if (field.name === "Nome de usuário no Discord") {
                  discord = field.value;
                }
              });

              // Conta total de reações na mensagem
              const totalReactions = msg.reactions.cache.reduce(
                (acc, reaction) => acc + reaction.count,
                0
              );

              // Formata a saída
              if (nome) content.push(`Nome: ${nome}`);
              content.push(`Votos: ${totalReactions}`);

              // Adiciona o link do github logo após os votos
              embed.fields.forEach((field) => {
                if (field.name === "Link do github com o projeto") {
                  content.push(`Link: ${field.value}`);
                }
              });

              if (desc.length > 0) content.push(`Descrição: ${desc.join(" ")}`);
              if (discord) content.push(`Usuário: ${discord}`);
            }

            if (content.length > 0) {
              messages.push(content.join("\n"));
            }
          });
        }
      });

      lastId = fetchedMessages.last().id;

      console.log(`Coletadas ${messages.length} mensagens até agora...`);

      // Pequeno delay para evitar rate limits
      await new Promise((resolve) => setTimeout(resolve, 1000));
    }

    const fs = require("fs");
    fs.writeFileSync("messages.txt", messages.join("\n\n---\n\n"));

    console.log(`Total de ${messages.length} mensagens salvas!`);
    client.destroy();
  } catch (error) {
    console.error("Erro:", error);
    client.destroy();
    process.exit(1);
  }
});

client.login(process.env.DISCORD_TOKEN);

async function handler(client, config, logger, logging) {
    client.once("ready", async () => await client.commands.get("ready").execute(client, logger, logging));
    client.on("message", async (message) => await client.commands.get("message").execute(message, config, logger, logging));
    client.on("error", async (error) => await client.commands.get("error").execute(client, error, logger, logging));
}

module.exports = {handler};
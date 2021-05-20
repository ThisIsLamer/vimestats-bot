const Discord = require("discord.js");
const client = new Discord.Client();

const config = require("./config.json");

// добавление коллекции команд
client.commands = new Discord.Collection();

// Утилиты
const logger = require("./utils/logger.js");
const import_modules = require("./utils/import_modules.js").execute;

// обработчик событий
const event_handler = require("./event_handler.js").handler;

async function main(logging=true) {
    import_modules(client, "src/commands", logger, logging);
    import_modules(client, "src/events", logger, logging);

    await event_handler(client, config, logger, logging);

    client.login(config.SERVER.TOKEN).then(() => {
        client.user.setPresence({
            activity: {name: "+ | +help"},
            status: "online"
        })
    });
}

main();
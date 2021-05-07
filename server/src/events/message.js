const { check_guild, get_prefix } = require("../database/prefix_database");

module.exports = {
    name: "message",
    description: "Обработчик сообщений",
    command: false,
    async execute(msg, config) {
        // обьявление префикса и id гильдии, если есть в списке кастомных префиксов
        const guild_id = check_guild(msg.guild.id);
        const prefix = await get_prefix(msg.guild.id, config.SERVER.PREFIX);

        // проверка на вызов без префикса, ботом, в ДМ сообщениях
        if (msg.author.bot) return;
        if (msg.channel.type === "dm") return;
        if (msg.guild.id === guild_id) {
            if (!(msg.content.startsWith(prefix))) return;
        } else {
            if (!(msg.content.startsWith(prefix))) return;
        }

        // определение обьектов команды, аргументов
        const command_body = msg.content.slice(prefix.length);
        const args = command_body.split(" ");
        const command = args.shift().toLowerCase();
        const cmd = msg.client.commands.get(command);

        // запускаем команду
        if (cmd) cmd.execute(msg.client, msg, args);
    }
}
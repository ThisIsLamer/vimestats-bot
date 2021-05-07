const Discord = require("discord.js");

module.exports = {
    name: "help",
    description: "Помощь по командам",
    command: true,
    async execute(client, ctx, args) {
        let embed = new Discord.MessageEmbed({
            title: "Помощь по командам",
            description: "Информация по всем командам бота",
            color: 0x00AA00,
            footer: {
                text: "• Канал поддержки бота: https://discord.gg/GV9ez9Z9dz\n• Официальный сайт бота: https://thisislamer.000webhostapp.com/"
            }
        })

        for (let i of client.commands) {
            if (i[1].command) {
                embed.addField(
                    "• "+i[1].name,
                    i[1].description,
                    true
                )
            }
        }
        await ctx.channel.send(embed);
    }
}
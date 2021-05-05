const Discord = require("discord.js");

const switch_embeds = require(process.cwd() + "/src/utils/switch_embeds.js");

const { get_player_nick } = require(process.cwd() + "/src/vimeapi.js");

module.exports = {
    name: "ping",
    description: "test command",
    async execute(client, message, args) {
        const embed1 = new Discord.MessageEmbed({
            title: "page1",
            description: "body text page1"
        })
        const embed2 = new Discord.MessageEmbed({
            title: "page2",
            description: "body text page2"
        })
        const embed3 = new Discord.MessageEmbed({
            title: "page3",
            description: "body text page3"
        })
        const embed4 = new Discord.MessageEmbed({
            title: "page4",
            description: "body text page4"
        })

        const embeds = [embed1, embed2, embed3, embed4];

        const emojis = [
            client.emojis.cache.get("839462684000387072"),
            client.emojis.cache.get("839462684197912576")
        ]

        await switch_embeds.start(client, embeds, message, emojis);
    }
}
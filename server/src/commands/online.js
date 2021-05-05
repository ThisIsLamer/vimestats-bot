const Discord = require("discord.js");

const { get_online, get_staff_online } = require(process.cwd() + "/src/vimeapi.js");

module.exports = {
    name: "online",
    description: "Просмотр онлайна проекта",
    async execute(client, msg, args) {
        const message = await msg.channel.send("Загрузка...");

        const online = await get_online();
        const staff_online = await get_staff_online();

        async function generate_staff_field(staff) {
            let text = "";
            for (let i of staff) {
                if (i.guild === null) text += `*${i.username}*\n`;
                else {
                    if (i.guild.tag === null) text += `*${i.username}*\n`;
                    else text += `**[${i.guild.tag}]** *${i.username}*\n`;
                } 
            }
            return text;
        }

        async function arcade(online) {
            const modes = ["ann", "bb", "bp", "bw", "cp", "dr", "duels", "gg", "hg", "kpvp", "lobby", "mw", "prison", "sw"];

            let online_modes = 0;
            for (let mod of modes) {
                online_modes += online.separated[mod];
            }
            return online.total-online_modes;
        }

        const embed = new Discord.MessageEmbed({
            fields: [
                {
                    name: "Онлайн",
                    value: `**• Annihilation**
                    *${online.separated.ann}*
                    **• BuildBattle**
                    *${online.separated.bb}*
                    **• BlockParty**
                    *${online.separated.bp}*
                    **• BedWars**
                    *${online.separated.bw}*
                    **• ClashPoint**
                    *${online.separated.cp}*
                    **• DeathRun**
                    *${online.separated.dr}*
                    **• Duels**
                    *${online.separated.duels}*`,
                    inline: true
                },
                {
                    name: online.total,
                    value: `**• GunGame**
                    *${online.separated.gg}*
                    **• HungerGames**
                    *${online.separated.hg}*
                    **• KitPvP**
                    *${online.separated.kpvp}*
                    **• MobWars**
                    *${online.separated.mw}*
                    **• Prison**
                    *${online.separated.prison}*
                    **• SkyWars**
                    *${online.separated.sw}*
                    **• Arcade**
                    *${await arcade(online)}*`,
                    inline: true
                }
            ]
        })
        if (!(staff_online.length === 0)) {
            embed.addField(
                `Персонал: ${staff_online.length}`,
                await generate_staff_field(staff_online),
                true
            )
        }

        await message.edit("", embed);
    }
}
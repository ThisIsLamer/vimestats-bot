const Discord = require("discord.js");

const { get_guild } = require(process.cwd() + "/src/vimeapi.js");

module.exports = {
    name: "guild",
    description: "Позволяет просматривать информацию о клане",
    command: true,
    async execute(client, ctx, args) {
        const message = await ctx.channel.send("Загрузка...");
        let guild;

        if (!Number(args[0])) {guild = await get_guild({name: args.join(" ")}); console.log(1)}
        else {guild = await get_guild({id: args[0]}); console.log(2)}

        if (guild.error) return await message.edit("Гильдия не найдена, проверьте правильность ввода");

        const embed = new Discord.MessageEmbed({
            title: guild.name,
            fields: [
                {
                    name: "Общее",
                    value: `**• id**
                    *${guild.id}*
                    **• Тег**
                    *${guild.tag}*
                    **• Уровень**
                    *${guild.level}*
                    **• Прогресс**
                    *${(guild.levelPercentage*100).toFixed(2)}%*`,
                    inline: true
                },
                {
                    name: "Прочее",
                    value: `**• Всего опыта**
                    *${guild.totalExp}*
                    **• Всего монет**
                    *${guild.totalCoins}*
                    **• Дата создания**
                    *${new Date(guild.created*1000).toLocaleDateString()}*
                    **• Участников**
                    *${guild.members.length}*`,
                    inline: true
                }
            ],
            thumbnail: {
                url: guild.avatar_url
            },
        })

        await message.edit("", embed);
    }
}
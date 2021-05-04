const Discord = require("discord.js");

const embed_guild_color = {
    "&0": 0x000000, "&1": 0x0000AA, "&2": 0x00AA00, "&3": 0x00AAAA,
    "&4": 0xAA0000, "&5": 0XAA00AA, "&6": 0xFFAA00, "&7": 0xAAAAAA,
    "&8": 0x555555, "&9": 0x5555FF, "&a": 0x55FF55, "&b": 0x55FFFF,
    "&c": 0xFF5555, "&d": 0xFF55FF, "&e": 0xFFFF55, "&f": 0xFFFFFF
}

const embed_rate_color = {
    0: 0xA60000, 30: 0xFF7F00, 70: 0xFFEC00, 95: 0x878600,
    130: 0x0ACF00, 150: 0xC400AB, 190: 0xE667AF, 220: 0x34C6CD
}

const { get_player_nick, get_player_stats, get_player_status, get_player_friends, get_leaderboard, get_player_head, get_player_page } = require(process.cwd() + "/src/vimeapi.js");

module.exports = {
    name: "stats",
    description: "Вывод статистики игрока",
    async execute(client, message, args) {
        let user = await get_player_nick(args[0]);
        user = user[0];
        let stats = await get_player_stats(user.id);
        stats = stats.stats.ARC.global;
        let leaderboard = await get_leaderboard("arc", 1000);
        leaderboard = leaderboard.records;
        let friends = await get_player_friends(user.id);
        friends = friends.friends.length;
        
        async function color(rate) {
            let i = 0;
            let rate_color = Object.keys(embed_rate_color);
            while(Number(rate_color[++i]) <= Number(rate)) {}
            return embed_rate_color[rate_color[--i]];
        }
        async function status(id) {
            let _status = await get_player_status(id);
            _status = _status.online.value;
            if (_status) return "Онлайн";
            else return "Оффлайн";
        }
        async function rank(user) {
            let rank = user.rank.toLowerCase();
            return rank[0].toUpperCase() + rank.substring(1);
        }
        async function rating(stats, leaderboard) {
            let total_stats = {kills: 0, deaths: 0, wins: 0, games: 0};
            
            for (let player of leaderboard) {
                for (let item of Object.keys(total_stats)) {
                    total_stats[item] += player[item];
                }
            }

            total_stats = (total_stats.kills/total_stats.deaths)*((total_stats.wins*100)/total_stats.games);
            user_stats = (stats.kills/stats.deaths)*((stats.wins*100)/stats.games);

            return ((user_stats/total_stats)*100).toFixed(2);
        }

        let var_rate = await rating(stats, leaderboard);

        const embed = new Discord.MessageEmbed({
            author: {name: args[0], iconURL: await get_player_head(args[0]), url: await get_player_page(args[0])},
            fields: [
                {
                    name: "Описание",
                    value: `**• Статус**
                    *${await status(user.id)}*
                    **• Ранг**
                    *${await rank(user)}*
                    **• Уровень**
                    *${user.level}*
                    **• Прогресс**
                    *${(user.levelPercentage*100).toFixed(2)}%*
                    **• Играл**
                    *${(user.playedSeconds/3600).toFixed(0)} ч.*
                    **• Друзей**
                    *${friends}*`,
                    inline: true
                },
                {
                    name: "Аркады",
                    value: `**• У/с**
                    *${(stats.kills/stats.deaths).toFixed(2)}*
                    **• Побед**
                    *${((100*stats.wins)/stats.games).toFixed(2)}%*
                    **• Всего игр**
                    *${stats.games}*
                    **• Убийств**
                    *${stats.kills}*
                    **• Смертей**
                    *${stats.deaths}*
                    **• Рейтинг**
                    *${var_rate}*`,
                    inline: true
                }
            ],
            color: await color(var_rate)
        });

        if (!(user.guild === null)) {
            embed.addField(
                "Гильдия",
                `**• Название**
                *${user.guild.name}*
                **• Тег**
                *${user.guild.tag}*
                **• Уровень**
                *${user.guild.level}*
                **• Прогресс**
                *${(user.guild.levelPercentage*100).toFixed(2)}*
                **• Цвет**
                *${user.guild.color}*
                **• id**
                *${user.guild.id}*`,
                true
            ).setThumbnail(
                user.guild.avatar_url
            ).setColor(embed_guild_color[user.guild.color])
        }

        await message.channel.send(embed);
    }
}
const Discord = require("discord.js");
const { YoutubeDataAPI  } = require("youtube-v3-api");
const API_KEY = require(process.cwd() + "/src/config.json").YOUTUBEAPI.TOKEN;

const api = new YoutubeDataAPI(API_KEY);

const switch_embeds = require(process.cwd() + "/src/utils/switch_embeds.js");

const { get_streams, get_player_page, get_player_head, get_player_status } = require(process.cwd() + "/src/vimeapi.js");

module.exports = {
    name: "streams",
    description: "Вывод всех активных стримов",
    async execute(client, msg, args) {
        const message = await msg.channel.send("Загрузка...");

        const streams = await get_streams();
        if (streams.length === 0) 
            return await message.edit("В данный момент стримы отсутствуют");
        

        await api.searchVideo("d-DRZysMel4")
            .then((data) => {
                console.log(data.items[0].snippet);
            })
            .catch((err) => {
                console.log(err);
            })

        async function impressor_collector(stream) {
            const user_session = await get_player_status(stream.user.id).online;

            function user_status_session(session) {
                if (session.online.value) return "Онлайн";
                return "Оффлайн";
            }

            let youtube;
            await api.searchVideo(stream.url.replace("https://youtu.be/", ""))
                .then((data) => {
                    this.youtube = data;
                })

            const viewers = stream.viewers;
            const duration = stream.duration/60;
            const likes = youtube.items[0].statistics.likeCount;
            const dislikes = youtube.items[0].statistics.dislikeCount;
            const preview = youtube.items[0].snippet.thumbnails.maxres.url;

            const embed = new Discord.MessageEmbed({
                author: {
                    name: stream.user.username,
                    url: await get_player_page(stream.user.username),
                    iconURL: await get_player_head(stream.user.username)
                },
                title: stream.title,
                description: `• Зрителей: ${viewers} • Продолжительность: ${duration}ч | 👍 ${likes} / 👎 ${dislikes}`,
                fields: [
                    {
                        name: "Общее",
                        valie: `**• Уровень**\n*${stream.user.level}*\n**• Играл**\n*${stream.user.playedSeconds/3600} ч.*`,
                        inline: true
                    },
                    {
                        name: "Активность",
                        description: `**• Статус**\n*${user_status_session(user_session)}*\n**• Подробнее**\n*${user_session.online.message}*`,
                        inline: true
                    }
                ],
                image: {
                    url: preview
                }
            })

            if ((stream.user.guild === null)) {
                embed.addField(
                    "Гильдия",
                    `**• Название**\n*${stream.user.guild.name}*\n**• Уровень**\n*${stream.user.guild.level}*`,
                    true
                );
            }
            return embedl
        }
        
        if (streams.length === 1)
            return await message.edit("", await impressor_collector(streams[0]));
        else {
            let embeds = [];
            for (stream of streams) {
                embeds.push(await impressor_collector(stream));
            }
            await message.delete();
            await switch_embeds.start(client, embeds, msg)
        }
    }
}
from discord.ext import commands
import discord, json

from youtube_api import YoutubeDataApi
from googletrans import Translator
from Cybernator import Paginator

from loguru import logger

from assets import VimeApi as vime
from assets import TotalStats


class CustomCommands(commands.Cog):

    def __init__(self, client):
        with open("config.json", "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.client = client
        self.yt = YoutubeDataApi(self.config["yt_token"])

        # Цвета внедрителя модуля вывода достижений
        self.color = {"Глобальные": 0xFFAA00, "Лобби": 0xFFD700, "SkyWars": 0x3CA0D0,
            "BedWars": 0xFF0700, "GunGame": 0x1B1BB3, "MobWars": 0x00C90D,
            "DeathRun": 0x8B42D6, "KitPvP": 0xFF3500, "BlockParty": 0x00AE68,
            "Annihilation": 0x9B001C, "HungerGames": 0xFFE800, "BuildBattle": 0x3216B0,
            "ClashPoint": 0xABF000, "Дуэли": 0xCE0071, "Prison": 0xA63400}

        # Цвета внедрителя модуля вывода статистики
        self.ColorList = {"&0": discord.Colour(value=0x000000), "&1": discord.Colour.dark_blue(), "&2": discord.Colour.dark_green(), "&3": discord.Colour.dark_teal(),
            "&4": discord.Colour.dark_red(), "&5": discord.Colour.dark_purple(), "&6": discord.Colour.gold(), "&7": discord.Colour.greyple(), "&8": discord.Colour.dark_gray(),
            "&9": discord.Colour.blue(), "&a": discord.Colour.green(), "&b": discord.Colour(value=0x55FFFF), "&c": discord.Colour.red(), "&d": discord.Colour.purple(),
            "&e": discord.Colour(value=0xFFFF55), "&f": discord.Colour(value=0xFFFFFF)}

    '''
    Команда которая выводит статистику пользователя, имеет несколько применений в зависимости от запроса.
    1) Пример: !stat nic -  выведется обычная статистика игрока с информацией об аккаунте/гильдии и статистикой в аркадах
    2) Пример: !stat nic1 nic2 arc - выведется статистика обоих пользователей, с расчётом эффективности одного игрока над другим
    3) Пример: !stat nic arc -  выведется статистика в выбранном режиме

    >>> ctx - обьект сообщения который передаёт пользователь,
    >>> name - ник пользователя по которому будет найдена статистика,
    >>> arg - аргумент передаёт аргументы пользователя, может быть nic, может быть id режима
    '''
    @commands.command(aliases=["stat", "stats", "стата", "статистика"])
    async def _UserStat(self, ctx, name, arg=None):
        message = await ctx.send(content="Загрузка ...")

        if ~(name.isdigit()):
            id = vime.GetPlayersName(names=name).replace("[", "").replace("]", "")
            name = str(json.loads(id)["id"])

        def GuildCheck(guild):
            if guild is None:
                return "*...*"
            else:
                return guild['name']

        def FlagMessageGeneration(UserStat):
            def GlobalSessionStat(stat):
                translator = Translator()
                data = ""
                items = list(stat.keys())
                for item in items:
                    '''
                    
                    АПИ СЕРВИСА ГУГЛ ПЕРЕВОДЧИК НЕ РАБОТАЕТ
                    
                    >>> для реальзации функции нужно добавить json файл в котором будут
                    записаны русифицированные ключи
                    
                    '''
                    data += f"{translator.translate(text=str(item), dest='ru')}\n{stat[item]}"
                return data

            emb = discord.Embed()
            
            emb.add_field(name="Глобальная", value=GlobalSessionStat(stat=UserStat["global"]))
            emb.add_field(name="Сезонная", value=GlobalSessionStat(stat=UserStat["session"]))

            return emb

        def MainMessageGeneration(UserStats):
            def FunctionGetStatistics(stats):
                items = {"kills": 0, "deaths": 0, "wins": 0, "games": 0}

                for i in items:
                    items[i] += stats["ARC"]["global"][i]

                wins = (items["wins"] * 100) / items["games"]
                kd = items["kills"] / items["deaths"]

                user = kd * wins

                total = TotalStats.TotalStats()
                for item in total[0]:
                    total[0][item] = total[0][item] / total[1]

                total = total[0]
                total = (total["kills"]/total["deaths"]) * ((total["wins"]*100)/total["games"])

                rate = user / total

                return kd, wins, items["games"], items["kills"], items["deaths"], float('{0:.2f}'.format(rate*100))

            def GuildField(guild):
                return f"**• Название**\n *{guild['name']}*\n\
                    **• Тег**\n *{guild['tag']}*\n\
                    **• Уровень**\n *{guild['level']}*\n\
                    **• Прогресс**\n *{float('{0:.2f}'.format(guild['levelPercentage']*100))}%*\n\
                    **• Цвет**\n *{guild['color']}*\n\
                    **• id**\n *{guild['id']}*"

            getStatistics = FunctionGetStatistics(stats=UserStats["stats"])

            description = f"**• id**\n *{UserStats['user']['id']}*\n\
                **• Уровень**\n *{UserStats['user']['level']}*\n\
                **• Прогресс**\n *{'%.2f' % ((UserStats['user']['levelPercentage'])*100)}%*\n\
                **• Ранг**\n *{(UserStats['user']['rank']).lower()}*\n\
                **• Наиграно часов**\n *{'%.2f' % ((UserStats['user']['playedSeconds'])/3600)}*\n\
                **• Клан**\n *{GuildCheck(UserStats['user']['guild'])}*"
            
            averageStatistics = f"**• У/с**\n *{'%.2f' % getStatistics[0]}*\n\
                **• Побед**\n *{'%.2f' % getStatistics[1]}%*\n\
                **• Всего игр**\n *{getStatistics[2]}*\n\
                **• Убийств**\n *{getStatistics[3]}*\n\
                **• Смертей**\n *{getStatistics[4]}*\n\
                **• Рейтинг**\n *{getStatistics[5]}*"

            if UserStats["user"]["guild"] is None:
                rate = getStatistics[5]
                if rate < 30:
                    color = 0xA60000
                elif rate > 30 and rate < 70:
                    color = 0xFF7F00
                elif rate > 70 and rate < 95:
                    color = 0xFFEC00
                elif rate > 95 and rate < 130:
                    color = 0x078600
                elif rate > 130 and rate < 150:
                    color = 0x0ACF00
                elif rate > 150 and rate < 190:
                    color = 0xC400AB
                elif rate > 190 and rate < 220:
                    color = 0xE667AF
                elif rate > 220:
                    color = 0x34C6CD

                emb = discord.Embed(color = color)
            else:
                emb = discord.Embed(colour = self.ColorList[UserStats["user"]["guild"]["color"]])
                if UserStats["user"]["guild"]["avatar_url"] is None:
                    pass
                else:
                    emb.set_thumbnail(url=UserStats["user"]["guild"]["avatar_url"])
            
            emb.add_field(name="Описание", value=description)
            emb.add_field(name="Аркады", value=averageStatistics)
            
            if UserStats["user"]["guild"] is None:
                pass
            else:
                emb.add_field(name="Гильдия", value=GuildField(guild=UserStats["user"]["guild"]))

            emb.set_author(name=UserStats["user"]["username"], icon_url=f"https://skin.vimeworld.ru/head/{UserStats['user']['username']}.png")
            return emb

        stats = json.loads(vime.GetPlayerStats(id=name).replace("[", "").replace("]", ""))

        if arg is None:
            await message.edit(content=None, embed=MainMessageGeneration(stats))
        else:
            arg = arg.upper()
            await message.edit(content=None, embed=FlagMessageGeneration(stats["stats"][arg]))

    '''
    Команда онлайн выводит весь онлайн по всем минииграм на сервере,
    а так же онлайн по отдельным минииграм, и онлайн персонала

    >>> ctx - обьект сообщения который передаёт пользователь
    '''
    @commands.command(aliases=["online", "онлайн"])
    async def _online(self, ctx):
        def GenerationText(online, staff, NameGames):
            data=data1=data2=name = ""
            i=arc = 0
            for item in online["separated"].keys():
                if item == "lobby":
                    pass
                else:
                    if item.upper() in ["BRIDGE", "JUMPLEAGUE", "MURDER", "PAINTBALL", "SHEEP", "TURFWARS", "TNTTAG", "TNTRUN", "LUCKYWARS", "ZOMBIECLAUS"]:
                        arc += online["separated"][item]
                    else:
                        for j in NameGames:
                            if j["id"].lower() == item:
                                name = j["name"]

                        if i < 7:
                            data += f"**• {name}**\n*{online['separated'][item]}*\n"
                        else:
                            data1 += f"**• {name}**\n*{online['separated'][item]}*\n"
                        i += 1

            for i in range(len(staff)):
                if "name" in staff[i]['guild']:
                    guildname = staff[i]['guild']['name']
                else:
                    guildname = None
                data2 += f"**◉ {staff[i]['username']}**\n*{guildname}*\n"

            return data, data1, data2, arc

        online = json.loads(vime.Online())
        staff = json.loads(vime.OnlineStaff())

        gentext = GenerationText(
            online=online,
            staff=staff,
            NameGames=json.loads(vime.GetMiscGames())
        )

        emb = discord.Embed()

        emb.add_field(name="Онлайн", value=gentext[0])
        emb.add_field(name=online["total"], value=gentext[1]+f"**Arcade**\n{gentext[3]}")
        emb.add_field(name=f"Персонал: {len(staff)}", value=gentext[2])

        await ctx.send(embed=emb)


    '''
    Команде streams передаёт список активных стримов и выводит в чат в виде Embed, если стримов нет, выводится предупреждение
    о отсутствие стримов, если стрим один выводится данный стрим, если несколько, то стримы сортируются во уменьшению зрителей
    на стриме, и внедрители можно мереключать между собой использую соответствующие эмодзи.

    >>> ctx - обьект сообзения которое отправляет юзер
    '''
    @commands.command(aliases=["streams", "стримы", "трансляции"])
    async def _streams(self, ctx):
        message = await ctx.send(content="Загрузка ...")
        streams = json.loads(vime.OnlineStreams())

        def Content(stream):
            def Activity(arg):
                try:
                    arg = arg["game"]
                    if arg == "LOBBY":
                        return "Находится в лобби"
                    else:
                        return f"Играет в {arg.lower()}"
                except:
                    return "Онлайн"

            if stream["platform"] == "YouTube":
                colour = discord.Colour.red()
            elif stream["platform"] == "Twitch":
                colour = discord.Colour.purple()
            else:
                colour = discord.Colour.default()

            video = self.yt.get_video_metadata(video_id=stream["url"].replace("https://youtu.be/", ""))
            online = json.loads(vime.GetPlayersSession(id=str(stream["user"]["id"])))["online"]

            emb = discord.Embed(
                title=video["video_title"],
                description=f"• Зрителей: {stream['viewers']}  • Продолжительность: {float('{0:.2f}'.format(stream['duration']/3600))}ч \
                    | 👍 {video['video_like_count']} / 👎 {video['video_dislike_count']}",
                url=stream["url"],
                colour=colour
            )
            emb.set_image(url=video["video_thumbnail"])
            emb.set_author(name=stream["owner"], icon_url=f"https://skin.vimeworld.ru/head/{stream['owner']}.png")

            emb.add_field(name="Общее", value=f"**• Уровень**\n *{stream['user']['level']}*\n\
                **• Наиграно часов**\n *{'%.2f' % ((stream['user']['playedSeconds'])/3600)}*")
            emb.add_field(name="Активность", value=f"**• Статус**\n*{Activity(online)}*\n\
                **• Подробнее**\n*{online['message']}*")

            if "guild" in stream["user"]:
                emb.add_field(name="Гильдия", value=f"**• Название**\n*{stream['user']['guild']['name']}*\n\
                    **• Уровень**\n*{stream['user']['guild']['level']}*")
            return emb
            
        if len(streams) == 0 :
            await message.edit(content="В данный момент стримы отсутствуют")
        elif len(streams) == 1:
            await message.edit(content=None, embed=Content(streams[0]))
        else:
            embeds = []
            spectators = []
            for stream in streams:
                spectators.append(stream["viewers"])
            spectators.sort(reverse=True)

            for stream in streams:
                for spectator in spectators:
                    if spectator == stream["viewers"]:
                        embeds.append(Content(stream=stream))

            await message.edit(content=None, embed=embeds[0])
            page = Paginator(self.client, message, only=ctx.author, use_more=False, embeds=embeds, timeout=9000)
            await page.start()


    '''
    Команда achievement выводит все возможные достижения из игры

    >>> ctx - обьект сообщения пользователя
    >>> arg - id нужного достижение которое нужно вывести
    '''
    @commands.command(aliases=["achievement", "достижения", "ачивки"])
    async def _achievement(self, ctx, arg=None):
        message = await ctx.send(content="Загрузка...")
        achievements = json.loads(vime.GetMiscAchievements())
        names = achievements.keys()

        def GeneratorEmbeds(achievement, name):
            emb = discord.Embed(title=achievement["title"], description=f"**id:** *{achievement['id']}*\n\
                **Приз:** *{achievement['reward']}*\n**Описание**\n{achievement['description'][0]}",
                color=self.color[name])

            emb.set_author(name=name)

            return emb

        try:
            arg = int(arg)
            for name in names:
                for i in achievements[name]:
                    if arg is i["id"]:
                        await message.edit(content=None, embed=GeneratorEmbeds(achievement=i, name=name))
        
        except:
            embeds = []
            for name in names:
                group = []
                for i in achievements[name]:
                    group.append(GeneratorEmbeds(achievement=i, name=name))

                embeds.append(group)

            await message.edit(content=None, embed=embeds[0][0])
            page = Paginator(self.client, message, only=ctx.author, use_more=True, embeds=embeds, timeout=16000)
            await page.start()

    '''
    Команда guild, гильдия - выводит информацию о гильдии и его создателе

    >>> ctx - обьект сообщения которое передаёт пользователь,
    >>> arg - аргумент - название, id, тег гильдии.
    '''
    @commands.command(aliases=["guild", "гильдия", "группа"])
    async def _guild(self, ctx, *, arg):
        message = await ctx.send(content="Загрузка...")

        try:
            int(arg)
            nameArg = "id"
        except:
            nameArg = "name"
            arg.replace(" ","%20")

        guild = json.loads(vime.GetGuild(arg=nameArg, data=arg))

        if "error" in guild:
            guild = vime.GetGuild("tag", data=arg)

            if "error" in guild:
                await message.edit(content="Гильдия не найдена, введите корректное название, или id.")
                return

        emb = discord.Embed(colour=self.ColorList[guild["color"]])

        if guild["avatar_url"] is None:
            pass
        else:
            emb.set_author(name=guild["name"], icon_url=guild["avatar_url"])

        emb.add_field(
            name="Гильдия",
            value=f"**• id**\n*{guild['id']}*\n\
                **• Тег**\n*{guild['tag']}*\n\
                **• Цвет**\n*{guild['color']}*\n\
                **• Уровень**\n*{guild['level']}*\n\
                **• Всего койнов**\n*{guild['totalCoins']}*\n\
                **• Всего участников**\n*{len(guild['members'])}*"
        )

        for leader in guild["members"]:
            if leader["status"] == "LEADER":
                emb.add_field(
                    name="Лидер",
                    value=f"**• id**\n*{leader['user']['id']}*\n\
                        **• Ник**\n*{leader['user']['username']}*\n\
                        **• Ранг**\n*{leader['user']['rank']}*\n\
                        **• Уровень**\n*{leader['user']['level']}*\n\
                        **• Вложил койнов**\n*{leader['guildCoins']}*\n\
                        **• Вложил опыта**\n*{leader['guildExp']}*"
                )

        await message.edit(content=None, embed=emb)


def setup(client):
    client.add_cog(CustomCommands(client))

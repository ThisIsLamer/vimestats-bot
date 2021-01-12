from discord.ext import commands
import discord, json

from googletrans import Translator
from loguru import logger

from assets import VimeApi as vime
from assets import TotalStats


class CustomCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

    '''
    Команда которая выводит статистику пользователя, имеет несколько применений в зависимости от запроса.
    1) Пример: !stat nic -  выведется обычная статистика игрока с информацией об аккаунте/гильдии и статистикой в аркадах
    2) Пример: !stat nic1 nic2 arc - выведется статистика обоих пользователей, с расчётом эффективности одного игрока над другим
    3) Пример: !stat nic arc -  выведется статистика в выбранном режиме

    >>> ctx - обьект сообщения который передаёт пользователь,
    >>> name - ник пользователя по которому будет найдена статистика,
    >>> arg - аргумент передаёт аргументы пользователя, может быть nic, может быть id режима
    '''
    @commands.command(aliases=["stat"])
    async def UserStat(self, ctx, name, arg=None):
        message = await ctx.send(content="Загрузка ...")

        ColorList = {"&0": discord.Colour(value=0x000000), "&1": discord.Colour.dark_blue(), "&2": discord.Colour.dark_green(), "&3": discord.Colour.dark_teal(),
            "&4": discord.Colour.dark_red(), "&5": discord.Colour.dark_purple(), "&6": discord.Colour.gold(), "&7": discord.Colour.greyple(), "&8": discord.Colour.dark_gray(),
            "&9": discord.Colour.blue(), "&a": discord.Colour.green(), "&b": discord.Colour(value=0x55FFFF), "&c": discord.Colour.red(), "&d": discord.Colour.purple(),
            "&e": discord.Colour(value=0xFFFF55), "&f": discord.Colour(value=0xFFFFFF)}

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
                emb = discord.Embed(colour = ColorList[UserStats["user"]["guild"]["color"]])
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
    @commands.command(aliases=["online"])
    async def _test(self, ctx):
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


def setup(client):
    client.add_cog(CustomCommands(client))

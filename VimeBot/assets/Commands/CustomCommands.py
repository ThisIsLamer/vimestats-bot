from discord.ext import commands
import discord, json

from loguru import logger

from assets import VimeApi as vime


class CustomCommands(commands.Cog):

    def __init__(self, client):
        self.client = client

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

        def MessageGeneration(UserStats):
            def FunctionGetStatistics(stats):
                kd=rate=games=wins=kills=death = 0

                for item in stats:
                    if "BRIDGE" in item:
                        break
                    else:
                        if "kills" in stats[item]["global"]:
                            if stats[item]["global"] != 0:
                                kills += stats[item]["global"]["kills"]

                        if "deaths" in stats[item]["global"]:
                            if stats[item]["global"] != 0:
                                death += stats[item]["global"]["deaths"]

                        if "games" in stats[item]["global"]:
                            if stats[item]["global"] != 0:
                                games += stats[item]["global"]["games"]

                        if "wins" in stats[item]["global"]:
                            if stats[item]["global"] != 0:
                                wins += stats[item]["global"]["wins"]

                wins = (wins * 100) / games
                kd = kills / death
                rate = int((kd * wins * games * kills * death) / 10000)

                return kd, wins, games, kills, death, rate

            def GuildField(guild):
                return f"**Название**\n *{guild['name']}*\n\
                    **Тег**\n *{guild['tag']}*\n\
                    **Уровень**\n *{guild['level']}*\n\
                    **Прогресс**\n *{float('{0:.2f}'.format(guild['levelPercentage']*100))}%*\n\
                    **Цвет**\n *{guild['color']}*\n\
                    **id**\n *{guild['id']}*"

            getStatistics = FunctionGetStatistics(stats=UserStats["stats"])

            description = f"**id**\n *{UserStats['user']['id']}*\n\
                **Уровень**\n *{UserStats['user']['level']}*\n\
                **Прогресс**\n *{'%.2f' % ((UserStats['user']['levelPercentage'])*100)}%*\n\
                **Ранг**\n *{(UserStats['user']['rank']).lower()}*\n\
                **Наиграно часов**\n *{'%.2f' % ((UserStats['user']['playedSeconds'])/3600)}*\n\
                **Клан**\n *{GuildCheck(UserStats['user']['guild'])}*"
            
            averageStatistics = f"**К/д**\n *{'%.2f' % getStatistics[0]}*\n\
                **Побед**\n *{'%.2f' % getStatistics[1]}%*\n\
                **Всего игр**\n *{getStatistics[2]}*\n\
                **Убийств**\n *{getStatistics[3]}*\n\
                **Смертей**\n *{getStatistics[4]}*\n\
                **Рейтинг**\n *{getStatistics[5]}*"

            if UserStats["user"]["guild"] is None:
                emb = discord.Embed()
            else:
                emb = discord.Embed(colour = ColorList[UserStats["user"]["guild"]["color"]])
                if UserStats["user"]["guild"]["avatar_url"] is None:
                    pass
                else:
                    emb.set_thumbnail(url=UserStats["user"]["guild"]["avatar_url"])
            
            emb.add_field(name="Описание", value=description)
            emb.add_field(name="Статистика", value=averageStatistics)
            
            if UserStats["user"]["guild"] is None:
                pass
            else:
                emb.add_field(name="Гильдия", value=GuildField(guild=UserStats["user"]["guild"]))

            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            return emb

        stats = vime.GetPlayerStats(id=name).replace("[", "").replace("]", "")
        await message.edit(content=None, embed=MessageGeneration(json.loads(stats)))



def setup(client):
    client.add_cog(CustomCommands(client))

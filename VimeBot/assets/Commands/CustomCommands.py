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
            print(id)
            name = str(json.loads(id)["id"])

        def GuildCheck(guild):
            if guild is None:
                return "*Не состоит в семье*"
            else:
                return f"|*Гильдия:* **{guild['name']}**\n|*id:* **{guild['id']}**\n|*Уровень:* **{guild['level']}**\n|*Прогресс:* **{'%.2f'%((guild['levelPercentage'])*100)}%**"

        def MessageGeneration(UserStats):
            data = f"> *id:* **{UserStats['user']['id']}**\n\
                > *Уровень:* **{UserStats['user']['level']}**\n\
                > *Прогресс:* **{'%.2f' % ((UserStats['user']['levelPercentage'])*100)}%**\n\
                > *Ранг:* **{(UserStats['user']['rank']).lower()}**\n\
                > *Наиграно часов:* **{'%.2f' % ((UserStats['user']['playedSeconds'])/3600)}**\n\
                > {GuildCheck(guild=UserStats['user']['guild'])}"

            if UserStats["user"]["guild"] is None:
                emb = discord.Embed(title=UserStats["user"]["username"], description=data)
            else:
                print(ColorList[UserStats["user"]["guild"]["color"]])
                emb = discord.Embed(title=UserStats["user"]["username"], description=data, colour = ColorList[UserStats["user"]["guild"]["color"]])
                if UserStats["user"]["guild"]["avatar_url"] is None:
                    pass
                else:
                    emb.set_thumbnail(url=UserStats["user"]["guild"]["avatar_url"])

            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            return emb

        stats = vime.GetPlayerStats(id=name).replace("[", "").replace("]", "")
        await message.edit(content=None, embed=MessageGeneration(json.loads(stats)))



def setup(client):
    client.add_cog(CustomCommands(client))

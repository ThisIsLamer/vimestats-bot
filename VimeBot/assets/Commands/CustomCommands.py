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

        with open("assets/Commands/MinecraftColorsInHex.json", "r", encoding="utf-8") as file:
            ColorList = json.load(file)

        if ~(name.isdigit()):
            name = json.load(vime.GetPlayersName(names=name))["username"]

        def GuildCheck(guild):
            if guild is None:
                return "*Не состоит в семье*"
            else:
                return f"|*Гильдия:* **{guild['name']}**\n|*id:* **{guild['id']}**\n|*Уровень:* **{guild['level']}**\n|*Прогресс:* **{(guild['levelPercentage'])/100}%**"

        def MessageGeneration(UserStats):
            data = f"> *id:* **{UserStats['user']['id']}**\n\
                > *Уровень:* **{UserStats['user']['level']}**\n\
                > *Прогресс:* **{(UserStats['user']['levelPercentage'])/100}%**\n\
                > *Ранг:* **{UserStats['user']['rank']}**\n\
                > *Наиграно часов:* **{(UserStats['user']['playedSeconds'])/3600}**\n\
                > {GuildCheck(guild=UserStats['user']['guild'])}"

            if "name" in UserStats["user"]["guild"]:
                emb = discord.Embed(title=UserStats["user"]["name"], description=data, color = ColorList[UserStats["user"]["guild"]["color"]])
                emb.set_thumbnail(url=UserStats["user"]["guild"]["avatar_url"])
            else:
                emb = discord.Embed(title=UserStats["user"]["name"], description=data)


            emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
            return emb

        print(vime.GetPlayerStats(id=name))
        await message.edit(embed=MessageGeneration(json.load(vime.GetPlayerStats(id=name))))



def setup(client):
    client.add_cog(CustomCommands(client))

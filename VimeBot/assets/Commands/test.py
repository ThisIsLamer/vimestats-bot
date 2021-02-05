from discord.ext import commands
import discord, sqlite3, json

from Cybernator import Paginator

from loguru import logger

from assets import VimeApi as vime

from assets.Database.userbind import start, add, remove


class test(commands.Cog):

    def __init__(self, client):
        self.client = client

        # userbind база данных
        self.base = start()
        self.db = self.base[0]
        self.sql = self.base[1]
        

    @commands.command(aliases=["ts"])
    async def _test(self, ctx, nick):
        if nick == "remove":
            color = discord.Colour.green()
            info = "Ник успешно отвязан"

            remove(sql=self.sql, db=self.db, id=ctx.author.id)
        else:
            player = json.loads(vime.GetPlayersName(nick))
            try:
                player[0]["id"]

                color = discord.Colour.green()
                info = "Ник успешно привязан"

                add(sql=self.sql, db=self.db, id=ctx.author.id, nick=nick)
            except:
                color = discord.Colour.red()
                info = "Ник не найден, проверьте правильность ввода."

        emb = discord.Embed(
            title="Привязка",
            description=info,
            colour=color
        )

        await ctx.send(embed=emb)


def setup(client):
    client.add_cog(test(client))

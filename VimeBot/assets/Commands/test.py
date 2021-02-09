from discord.ext import commands
import discord, sqlite3, json, yadisk

from loguru import logger


class test(commands.Cog):

    def __init__(self, client):
        self.client = client

        with open("config.json", "r", encoding="utf-8") as file:
            self.config = json.load(file)

        self.disk = yadisk.YaDisk(token=config["yt_token"])
        

    @commands.command(aliases=["ts"])
    async def _test(self, ctx, nick):
        pass


def setup(client):
    client.add_cog(test(client))

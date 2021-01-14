from discord.ext import commands
import discord, json, requests, io, os

from loguru import logger

from assets import VimeApi as vime


class test(commands.Cog):

    def __init__(self, client):
        self.client = client
        

    @commands.command(aliases=["ts"])
    async def _test(self, ctx, arg=None):
        pass


def setup(client):
    client.add_cog(test(client))

from discord.ext import commands
import discord

from loguru import logger


class DatabaseService(commands.Cog):

    def __init__(self, client):
        self.client = client


def setup(client):
    client.add_cog(DatabaseService(client))
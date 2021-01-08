from discord.ext import commands
import discord

from loguru import logger


class EventHandler(commands.Cog):

    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_ready(self):
        logger.add("debug.json", format="{time} {level} {message}",
        level="DEBUG", rotation="4mb", compression="zip", serialize=True)

        logger.info("Бот запущен")
        


def setup(client):
    client.add_cog(EventHandler(client))
from discord.ext import commands
import discord, json, requests, io

from loguru import logger
from PIL import Image

from assets import VimeApi as vime


class test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["test"])
    async def _test(self, ctx, id, arg=None):
        vime.GetSkin(id=id)

        img = Image.open("assets/TemporaryPictures/img.jpg")
        area = (8,8,16,16)
        img = img.crop(area)

        img = Image.open(io.BytesIO(img))

        img.save("assets/TemporaryPictures/img.jpg")

        await ctx.send(file=discord.File(fp="assets/TemporaryPictures/img.jpg"))

def setup(client):
    client.add_cog(test(client))

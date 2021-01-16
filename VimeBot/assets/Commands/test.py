from discord.ext import commands
import discord, json, requests, io, os

from Cybernator import Paginator

from loguru import logger

from assets import VimeApi as vime


class test(commands.Cog):

    def __init__(self, client):
        self.client = client
        

    @commands.command(aliases=["ts"])
    async def _test(self, ctx, arg=None):
        color = {"Глобальные": 0xFFAA00, "Лобби": 0xFFD700, "SkyWars": 0x3CA0D0,
        "BedWars": 0xFF0700, "GunGame": 0x1B1BB3, "MobWars": 0x00C90D,
        "DeathRun": 0x8B42D6, "KitPvP": 0xFF3500, "BlockParty": 0x00AE68,
        "Annihilation": 0x9B001C, "HungerGames": 0xFFE800, "BuildBattle": 0x3216B0,
        "ClashPoint": 0xABF000, "Дуэли": 0xCE0071, "Prison": 0xA63400}

        message = await ctx.send(content="Загрузка...")
        achievements = json.loads(vime.GetMiscAchievements())
        names = achievements.keys()

        def GeneratorEmbeds(achievement, name):
            emb = discord.Embed(title=achievement["title"], description=f"**id:** *{achievement['id']}*\n\
                **Приз:** *{achievement['reward']}*\n**Описание**\n{achievement['description']}",
                color=color[name])

            emb.set_author(name=name)

            return emb

        try:
            arg = int(arg)
            for name in names:
                for i in achievements[name]:
                    if arg is i["id"]:
                        await message.edit(content=None, embed=GeneratorEmbeds(achievement=i, name=name))
        
        except:
            embeds = []
            for name in names:
                group = []
                for i in achievements[name]:
                    group.append(GeneratorEmbeds(achievement=i, name=name))

                embeds.append(group)

            await message.edit(content=None, embed=embeds[0][0])
            page = Paginator(self.client, message, only=ctx.author, use_more=True, embeds=embeds, timeout=16000)
            await page.start()


def setup(client):
    client.add_cog(test(client))

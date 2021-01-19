from discord.ext import commands
import discord, json, requests, io, os

from Cybernator import Paginator

from loguru import logger

from assets import VimeApi as vime


class test(commands.Cog):

    def __init__(self, client):
        self.client = client
        

    @commands.command(aliases=["ts"])
    async def _test(self, ctx, arg):
        message = await ctx.send(content="Загрузка...")

        try:
            int(arg)
            nameArg = "id"
        except:
            nameArg = "name"
            arg.replace(" ","%")

        guild = vime.GetGuild(arg=nameArg, data=arg)

        if "error" in guild:
            guild = vime.GetGuild("tag", data=arg)

            if "error" in guild:
                await message.edit(content="Гильдия не найдена, введите корректное название, или id.")
                return
        
        emb = discord.Embed()

        emb.set_author(name=guild["name"], url=guild["avatar_url"])

        emb.add_field(
            name="Гильдия",
            value=f"**• id**\n*{guild['id']}*\n\
                **• Тег**\n*{guild['tag']}*\n\
                **• Цвет**\n*{guild['color']}*\n\
                **• Уровень**\n*{guild['level']}*\n\
                **• Всего койнов**\n*{guild['totalCoins']}*\n\
                **• Всего участников**\n*{len(guild['members'])}*"
        )

        for leader in guild["members"]:
            if leader["status"] == "LEADER":
                emb.add_field(
                    name="Лидер",
                    value=f"**• id**\n*{leader['user']['id']}*\n\
                        **• Ник**\n*{leader['user']['username']}*\n\
                        **• Ранг**\n*{leader['user']['rank']}*\n\
                        **• Уровень**\n*{leader['user']['level']}*\n\
                        **• Вложил монет**\n*{leader['guildCoins']}*\n\
                        **• Вложил опыта**\n*{leader['guildExp']}*"
                )
        perksLevel = []
        listPerks = {"arr": []}
        for perk in guild["perks"].keys():
            perksLevel.append(guild["perks"][perk]["level"])
        perksLevel.sort(reverse=True)

        i = 0
        for perk in guild["perks"].keys():
            if i == 5:
                break
            if perksLevel[0] in guild["perks"][perk]["level"]:
                listPerks["arr"].append({
                    "name": guild["perks"][perk]["name"],
                    "level": guild["perks"][perk]["level"]
                })
                perksLevel.pop(0)
                i += 1
        
        data = ""
        for perk in listPerks["arr"]:
            data += f"**• {perk['name']}**\n*{perk['level']}*\n"

        emb.add_field(
            name="Перки",
            value=data
        )

        await message.edit(content=None, embed=emb)


def setup(client):
    client.add_cog(test(client))

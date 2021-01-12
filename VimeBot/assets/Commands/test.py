from discord.ext import commands
import discord, json, requests, io

from loguru import logger

from assets import VimeApi as vime


class test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["test"])
    async def _test(self, ctx, arg=None):
        def GenerationText(online, staff, NameGames):
            data=data1=data2=name = ""
            i=arc = 0
            for item in online["separated"].keys():
                if item == "lobby":
                    pass
                else:
                    if item.upper() in ["BRIDGE", "JUMPLEAGUE", "MURDER", "PAINTBALL", "SHEEP", "TURFWARS", "TNTTAG", "TNTRUN", "LUCKYWARS", "ZOMBIECLAUS"]:
                        arc += online["separated"][item]
                    else:
                        for j in NameGames:
                            if j["id"].lower() == item:
                                name = j["name"]

                        if i < 7:
                            data += f"**• {name}**\n*{online['separated'][item]}*\n"
                        else:
                            data1 += f"**• {name}**\n*{online['separated'][item]}*\n"
                        i += 1

            for i in range(len(staff)):
                if "name" in staff[i]['guild']:
                    guildname = staff[i]['guild']['name']
                else:
                    guildname = None
                data2 += f"**◉ {staff[i]['username']}**\n*{guildname}*\n"

            return data, data1, data2, arc

        online = json.loads(vime.Online())
        staff = json.loads(vime.OnlineStaff())

        gentext = GenerationText(
            online=online,
            staff=staff,
            NameGames=json.loads(vime.GetMiscGames())
        )

        emb = discord.Embed()

        emb.add_field(name="Онлайн", value=gentext[0])
        emb.add_field(name=online["total"], value=gentext[1]+f"**Arcade**\n{gentext[3]}")
        emb.add_field(name=f"Персонал: {len(staff)}", value=gentext[2])

        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(test(client))

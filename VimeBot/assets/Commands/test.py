from discord.ext import commands
import discord, json

from loguru import logger

from assets import VimeApi as vime


class test(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["test"])
    async def _test(self, ctx, name, arg=None):
        def jj(name):
            kd=rate=games=wins=kills=death = 0

            id = vime.GetPlayersName(names=name).replace("[", "").replace("]", "")
            name = str(json.loads(id)["id"])

            stats = json.loads(vime.GetPlayerStats(id=name).replace("[", "").replace("]", ""))["stats"]
            for item in stats:
                if "BRIDGE" in item:
                    break
                else:
                    if "kills" in stats[item]["global"]:
                        if stats[item]["global"] != 0:
                            kills += stats[item]["global"]["kills"]

                    if "deaths" in stats[item]["global"]:
                        if stats[item]["global"] != 0:
                            death += stats[item]["global"]["deaths"]

                    if "games" in stats[item]["global"]:
                        if stats[item]["global"] != 0:
                            games += stats[item]["global"]["games"]

                    if "wins" in stats[item]["global"]:
                        if stats[item]["global"] != 0:
                            wins += stats[item]["global"]["wins"]

            wins = (wins * 100) / games
            kd = kills / death
            rate = int((kd * wins * games * kills * death) / 10000)

            return kd, wins, kills, death, rate

def setup(client):
    client.add_cog(test(client))

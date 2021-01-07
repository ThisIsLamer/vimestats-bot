from discord.ext import commands
import discord

import json, os

def main():
    client = commands.Bot(command_prefix=None)
    client.remove_command("help")

    for module in ...:
        for filename in os.listdir(f"assets/{module}"):
            if filename.endswith(".py"):
                client.load_extension(f"assets.{module}.{filename[:-3]}")

    token = ...
    client.run(token)
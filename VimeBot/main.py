from discord.ext import commands
import discord

from loguru import logger

import json, os


def main():
    client = commands.Bot(command_prefix=None)
    client.remove_command("help")

    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    for module in config["Components"]:
        for filename in os.listdir(f"assets/{module}"):
            if filename.endswith(".py"):
                client.load_extension(f"assets.{module}.{filename[:-3]}")

    token = config["token"]
    client.run(token)
    return "!!! Работа завершена !!!"

if __name__ == "__main__":
    logger.info(main())
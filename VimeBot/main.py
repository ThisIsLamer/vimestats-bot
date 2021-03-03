from discord.ext import commands
import discord

from loguru import logger

import json, os


@logger.catch
def main():
    with open("config.json", "r", encoding="utf-8") as file:
        config = json.load(file)

    client = commands.Bot(command_prefix=config["prefix"])
    client.remove_command("help")

    for module in config["Components"]:
        for filename in os.listdir(f"assets/{module}"):
            if filename.endswith(".py"):
                client.load_extension(f"assets.{module}.{filename[:-3]}")

    token = config["token"]
    client.run(token)
    return "!!! Работа завершена !!!"

if __name__ == "__main__":
    logger.warning(main())
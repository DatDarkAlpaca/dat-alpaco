from discord.ext import commands
import discord
import os

from utils.cog_utils import load_cogs
from bot import Bot


def main():
    bot = Bot(
        commands.when_mentioned_or('.'),
        intents=discord.Intents.default(),
        case_insensitive=True,
        help_command=None,
    )

    load_cogs(bot)
    bot.run(os.getenv('TOKEN'), reconnect=True)


if __name__ == '__main__':
    main()

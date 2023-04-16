import os

from discord import ApplicationCommand
from discord.ext import commands
from src.utils.logger import Logger


class Bot(commands.AutoShardedBot):
    async def register_command(self, command: ApplicationCommand, force: bool = True,
                               guild_ids: list[int] | None = None) -> None:
        pass

    def __init__(self, *args, **kwargs):
        super(Bot, self).__init__(*args, **kwargs)
        self.logger = Logger('bot', os.getenv('LOGGER_CONFIG_FILEPATH'))

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info(f"{self.user} is online.")
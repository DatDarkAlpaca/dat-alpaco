import os
import discord
import wavelink

from fnmatch import fnmatch

from wavelink.ext import spotify
from discord.ext import commands

from src.utils.logger import Logger


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents)

        self.logger = Logger('bot', os.getenv('LOGGER_CONFIG_FILEPATH'))
        self.load_cogs()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.setup_hook()
        self.logger.info(f"{self.user} is online.")

    async def setup_hook(self):
        spotify_client = spotify.SpotifyClient(
            client_id=os.getenv('SPOTIFY_CLIENT'),
            client_secret=os.getenv('SPOTIFY_SECRET'),
        )

        # node: wavelink.Node = wavelink.Node(uri=os.getenv('WAVELINK_URI'), password=os.getenv('WAVELINK_PASSWORD'))
        # await wavelink.NodePool.connect(client=self, nodes=[node], spotify=spotify_client)
        # self.logger.info('Wavelink node connected successfully.')

    def load_cogs(self):
        file_pattern = '*.py'
        any_cogs_found = False

        for path, subdirectories, files in os.walk('./cogs'):
            for cog in files:
                if cog.startswith('_'):
                    continue
                if fnmatch(cog, file_pattern):
                    cog_path = path.replace('\\', '.').replace('./', '') + '.' + cog[:-3]

                    try:
                        self.load_extension(cog_path)
                        self.logger.info(f"The cog '{cog[:-3]}' has been successfully loaded.")
                        any_cogs_found = True
                    except Exception as e:
                        self.logger.error(f"The cog '{cog[:-3]}' couldn't be loaded! | {e}")

        if not any_cogs_found:
            self.logger.info('Not cogs were detected.')

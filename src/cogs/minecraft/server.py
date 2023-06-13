import os
import aiomcrcon
from discord.ext import commands
from discord.commands import SlashCommandGroup

from src.utils.logger import Logger
from src.utils.context_utils import respond_ephemeral


class MinecraftServerCog(commands.Cog):
    minecraft = SlashCommandGroup(name='minecraft', description='Minecraft RCON related commands')

    def __init__(self, bot):
        self.timeout = 20
        self.logger = Logger('cog-minecraft')
        self.rcon_client = None
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.connect_rcon()

    async def connect_rcon(self):
        self.rcon_client = aiomcrcon.Client(
            os.getenv('RCON_HOST'),
            int(os.getenv('RCON_PORT')),
            os.getenv('RCON_PASSWORD')
        )

        try:
            await self.rcon_client.connect()
            self.logger.info('Connected to RCON')

        except aiomcrcon.RCONConnectionError:
            self.logger.error('An error occurred whilst connecting to the server.')
            return

        except aiomcrcon.IncorrectPasswordError:
            self.logger.error('The provided RCON password was incorrect.')
            return

    async def run_rcon_command(self, command: str) -> None:
        try:
            response, _ = await self.rcon_client.send_cmd(command, timeout=self.timeout)
        except aiomcrcon.ClientNotConnectedError:
            self.logger.error('The client is not connected to the RCON server.')
            return

        return response

    @minecraft.command(name='reload', description='Reloads the RCON connection')
    @commands.is_owner()
    async def reload(self, ctx) -> None:
        await self.run_rcon_command(f"/reload")
        await respond_ephemeral(ctx, 'Server reloading...')

    @minecraft.command(name='say', description='Reloads the RCON connection')
    @commands.is_owner()
    async def say(self, ctx, message: str) -> None:
        await self.run_rcon_command(f"/say {message}")
        await respond_ephemeral(ctx, 'Command execution succeeded.')

    @minecraft.command(name='list', description='Displays current members online')
    @commands.is_owner()
    async def list(self, ctx) -> None:
        response = await self.run_rcon_command(f"/list")
        await respond_ephemeral(ctx, f"{response}")


def setup(bot):
    bot.add_cog(MinecraftServerCog(bot))

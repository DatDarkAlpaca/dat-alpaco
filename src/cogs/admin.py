from discord.commands import SlashCommandGroup
from discord import ApplicationContext
from discord.ext import commands

from src.utils.logger import Logger


class AdminCog(commands.Cog):
    admin = SlashCommandGroup('admin', 'Useful commands for the bot owner.', checks=[commands.is_owner().predicate])

    def __init__(self, bot):
        self.logger = Logger('cog-admin')
        self.bot = bot

    @admin.command(name='reload', description='Reloads a cog')
    async def _reload_cog(self, _, *, cog_name: str):
        self.bot.reload_extension(cog_name)

    @admin.command(description='Shuts me down...')
    async def shutdown(self, ctx: ApplicationContext):
        await ctx.respond('Bye bye!')
        await self.bot.close()


def setup(bot):
    bot.add_cog(AdminCog(bot))

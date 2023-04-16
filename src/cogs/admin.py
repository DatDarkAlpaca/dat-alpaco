from discord.commands import SlashCommandGroup
from discord import ApplicationContext
from discord.ext import commands

from src.utils.logger import Logger


class Admin(commands.Cog):
    admin = SlashCommandGroup('admin', 'Useful commands for bot admins.', checks=[commands.is_owner().predicate])

    def __init__(self, bot):
        self.logger = Logger('cog-admin')
        self.bot = bot

    @admin.command(description='Shuts me down...')
    @commands.is_owner()
    async def shutdown(self, ctx: ApplicationContext):
        await ctx.respond('Shutting down... Bye bye!')
        self.logger.info('Shutting down.')
        await self.bot.close()


def setup(bot):
    bot.add_cog(Admin(bot))

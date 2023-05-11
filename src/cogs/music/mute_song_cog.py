import discord
import wavelink
from discord.ext import commands
from discord.commands import slash_command

from src.utils.context_utils import single_embed


class MuteSongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.previous_volume: dict = {}

    @slash_command(description='Mutes the player')
    async def mute(self, ctx):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        self.previous_volume[ctx.guild.id] = vc.volume

        await vc.set_volume(0)
        await single_embed(ctx, f"{ctx.user.mention} has muted the player.\n")

    @slash_command(description='Unmutes the player')
    async def unmute(self, ctx):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        previous = self.previous_volume.get(ctx.guild.id)
        if not previous:
            previous = 100

        await vc.set_volume(previous)
        await single_embed(ctx, f"{ctx.user.mention} has un-muted the player.\n")


def setup(bot):
    bot.add_cog(MuteSongCog(bot))

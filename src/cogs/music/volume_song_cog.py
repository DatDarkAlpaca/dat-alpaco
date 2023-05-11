import discord
import wavelink
from discord.ext import commands
from discord.commands import slash_command

from src.utils.context_utils import single_embed, respond_ephemeral


class VolumeSongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='Sets the player volume')
    async def volume(self, ctx, *, volume: discord.Option(int)):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        if not self.validate_volume(volume):
            return await respond_ephemeral(ctx, 'Please input a value between 0 and 1000.')

        await vc.set_volume(volume)
        await single_embed(ctx, f"{ctx.user.mention} has skipped the current song.\n")

    @staticmethod
    def validate_volume(volume: int) -> bool:
        return 0 <= volume <= 1000


def setup(bot):
    bot.add_cog(VolumeSongCog(bot))

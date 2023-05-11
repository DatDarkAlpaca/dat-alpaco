import discord
import wavelink
from discord.ext import commands

from src.utils.context_utils import single_embed, respond_ephemeral


class PauseSongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Pause the current playing track')
    async def pause(self, ctx):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').get_voice_channel(ctx)
        if not vc:
            return

        if not vc.current:
            return await respond_ephemeral(ctx, 'There are no songs playing.')

        if vc.is_paused():
            return await respond_ephemeral(ctx, 'My player is already paused!')

        await vc.pause()

        await single_embed(ctx, f"{ctx.user.mention} paused the song queue.\n"
                                f"Use the `/music resume` command to resume.")


def setup(bot):
    bot.add_cog(PauseSongCog(bot))

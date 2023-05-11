import discord
import wavelink
from discord.ext import commands

from src.utils.context_utils import single_embed, respond_ephemeral


class ResumeSongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Resume the current playing track from where it left')
    async def resume(self, ctx):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').get_voice_channel(ctx)
        if not vc:
            return

        if not vc.current:
            return await respond_ephemeral(ctx, 'There are no songs playing.')

        if not vc.is_paused():
            return await respond_ephemeral(ctx, 'There is already a music playing!')

        await vc.resume()

        await single_embed(ctx, f"{ctx.user.mention} resumed the song queue! :notes:\n"
                                f"Use the `/music pause` command to pause the queue.")


def setup(bot):
    bot.add_cog(ResumeSongCog(bot))

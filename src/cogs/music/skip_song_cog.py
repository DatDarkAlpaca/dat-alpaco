import wavelink
from discord.ext import commands
from discord.commands import slash_command

from src.utils.context_utils import single_embed, respond_ephemeral
from src.utils.player_utils import play_next


class SkipSongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='Skip to the next song in the queue')
    async def skip(self, ctx):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        if vc.queue.is_empty:
            if vc.current:
                await vc.stop()
                return await single_embed(ctx, f"{ctx.user.mention} has skipped the current song.\n")

            return await respond_ephemeral(ctx, "There is no more songs in the queue.")

        await play_next(vc)

        await single_embed(ctx, f"{ctx.user.mention} has skipped the current song.\n")


def setup(bot):
    bot.add_cog(SkipSongCog(bot))

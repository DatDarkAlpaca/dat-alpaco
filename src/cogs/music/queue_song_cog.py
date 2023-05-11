import discord
import wavelink
from discord.ext import commands, pages

from src.utils.context_utils import respond_ephemeral
from src.utils.embed_utils import queue_page_embed


class QueueSongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Displays the queue for the server')
    async def queue(self, ctx):
        vc: wavelink.Player = ctx.voice_client
        if not vc:
            return await respond_ephemeral(ctx, "I'm not in a voice channel.")

        if vc.queue.is_empty and not vc.current:
            return await respond_ephemeral(ctx, "I'm not playing anything.")

        paginator = pages.Paginator(pages=queue_page_embed(ctx, vc), show_disabled=False)
        await paginator.respond(ctx.interaction, ephemeral=False)


def setup(bot):
    bot.add_cog(QueueSongCog(bot))

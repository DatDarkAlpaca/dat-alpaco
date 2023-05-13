import wavelink
from discord import Option
from discord.ext import commands
from discord.commands import slash_command

from src.utils.context_utils import respond_ephemeral, single_embed


class JumpToSongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @slash_command(description='Jumps to a specific time period in the song')
    async def jump_to(self, ctx, *,
                      start_at: Option(str, description='You must provide a timeframe like this: 0:21:30')):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').get_voice_channel(ctx)
        if not vc:
            return

        if not vc.current:
            return await respond_ephemeral(ctx, 'I must be playing a song to execute this command')

        time_points = start_at.split(':')
        days, hours, minutes, seconds = [0] * 4

        if len(time_points) > 4:
            return await respond_ephemeral(ctx, 'You must provide a time stamp like: `0:00:00`')

        elif len(time_points) == 4:
            days = time_points[0]
            hours = time_points[1]
            minutes = time_points[2]
            seconds = time_points[3]

        elif len(time_points) == 3:
            hours = time_points[0]
            minutes = time_points[1]
            seconds = time_points[2]

        elif len(time_points) == 2:
            minutes = time_points[0]
            seconds = time_points[1]

        elif len(time_points) == 1:
            seconds = time_points[0]

        time_stamp = int(seconds) + int(minutes) * 60 + int(hours) * 3600 + int(days) * 86400
        await vc.seek(time_stamp * 1000)
        await single_embed(ctx, f'Aye! Skipped the current track to `{start_at}`.')


def setup(bot):
    bot.add_cog(JumpToSongCog(bot))

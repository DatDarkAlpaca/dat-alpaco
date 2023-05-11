import discord
import wavelink
from discord.ext import commands

from src.utils.embed_utils import embed_play
from src.utils.player_utils import play_next


class SearchTrackSelect(discord.ui.Select):
    def __init__(self, vc: wavelink.Player, tracks: list[wavelink.Playable]):
        self.vc = vc

        options = []
        for track in tracks:
            options.append(discord.SelectOption(label=track.title,
                                                description=f"Track from {track.author}",
                                                emoji='🎶',
                                                value=track.uri))

        super().__init__(placeholder='Choose a track', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        uri = self.values[0]

        track = await wavelink.YouTubeTrack.search(uri, return_first=True)
        self.vc.queue.put(track)

        if not self.vc.current:
            await self.vc.play(self.vc.queue.get())

        embed = embed_play(track)

        await interaction.response.send_message(embed=embed)


class SearchTrackView(discord.ui.View):
    def __init__(self, vc: wavelink.Player, tracks: list[wavelink.Playable]):
        super().__init__()
        self.add_item(SearchTrackSelect(vc, tracks))


class PlaySongCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):
        if payload.player:
            await play_next(payload.player)

    @discord.slash_command(description='Play a track')
    async def play(self, ctx, *, search_query: str):
        vc: wavelink.Player = await self.bot.get_cog('VoiceChannelCog').connect_and_get_voice_client(ctx)
        if not vc:
            return

        tracks = await wavelink.YouTubeTrack.search(search_query, return_first=False)
        await ctx.send('Choose a track!', view=SearchTrackView(vc, tracks))


def setup(bot):
    bot.add_cog(PlaySongCog(bot))

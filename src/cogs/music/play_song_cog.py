import discord
from discord.ext import commands

from src.utils.embed_utils import *
from src.utils.player_utils import play_next
from src.utils.context_utils import respond_ephemeral
from src.utils.string_utils import is_youtube_url, is_spotify_url, is_sound_cloud_url


class SearchTrackSelect(discord.ui.Select):
    def __init__(self, vc: wavelink.Player, tracks: list[wavelink.Playable]):
        self.vc = vc

        options = []
        for track in tracks:
            options.append(discord.SelectOption(label=track.title[0:100],
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

        await interaction.response.send_message(embed=embed_play(track))


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

        if is_youtube_playlist(search_query):
            return

        elif is_youtube_url(search_query):
            track = await wavelink.YouTubeTrack.search(search_query, return_first=True)
            await self.add_track_to_queue(vc, track)
            return await ctx.respond(embed=embed_play(track))

        elif is_spotify_url(search_query):
            return await self.handle_spotify(ctx, vc, search_query)

        elif is_sound_cloud_url(search_query):
            track = await wavelink.SoundCloudTrack.search(search_query, return_first=True)
            await self.add_track_to_queue(vc, track)
            return await ctx.respond(embed=embed_play(track))

        else:
            tracks = await wavelink.YouTubeTrack.search(search_query, return_first=False)
            await ctx.respond(':guitar: Choose a track: ', view=SearchTrackView(vc, tracks))

    # Helpers:
    @staticmethod
    async def add_track_to_queue(vc: wavelink.Player, track: wavelink.Playable):
        vc.queue.put(track)

        if not vc.current:
            await vc.play(vc.queue.get())

    async def handle_spotify(self, ctx, vc: wavelink.Player, search_query: str):
        decoded = spotify.decode_url(search_query)
        if not decoded:
            return await respond_ephemeral(ctx, 'Invalid spotify url')

        if decoded['type'] == spotify.SpotifySearchType.track:
            track = await spotify.SpotifyTrack.search(search_query)
            await self.add_track_to_queue(vc, track)
            return await ctx.respond(embed=embed_play_spotify(track))

        elif decoded['type'] == spotify.SpotifySearchType.unusable:
            return await respond_ephemeral(ctx, 'This URL yielded an unusable query type.')

        else:
            return await respond_ephemeral(ctx, 'This functionality is not available yet.')


def setup(bot):
    bot.add_cog(PlaySongCog(bot))

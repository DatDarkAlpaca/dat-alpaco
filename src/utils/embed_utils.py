from discord import Embed
import wavelink
from src.utils.time_utils import get_time_length
from src.utils.string_utils import get_video_thumbnail_url


# Music:
def embed_play(track: wavelink.Playable) -> Embed:
    embed = Embed(title="🎶 Alpacos' Player", color=0x38f2ff)

    track_name = track.title[0:100]
    embed.add_field(name='Track: ', value=f"[`{track_name}`]({track.uri})", inline=True)

    author = track.author[0:100]
    embed.add_field(name='Author: ', value=f"[`{author}`]({track.uri})", inline=True)

    embed.add_field(name='Duration: ', value=get_time_length(track.length / 1000), inline=True)

    embed.set_image(url=get_video_thumbnail_url(track.uri))

    return embed


def queue_page_embed(ctx, player: wavelink.Player) -> list[Embed]:
    pages = []
    guild_name = ctx.guild.name

    songs = len(player.queue)
    page_count = songs // 10 + 1
    songs_per_page = 10

    for i in range(page_count):
        description = ''

        main_video_uri = None
        if i == 0:
            main_video_uri = player.current.uri
            length = player.current.length / 1000
            description += f":drum: **Current Track:** `{player.current.title[0:100]}` [{get_time_length(length)}]\n\n"

        split_start = i * songs_per_page
        split_end = (i + 1) * songs_per_page

        for index, track in enumerate(list(player.queue)[split_start:split_end]):
            description += f":musical_note: `Track #{(index + 1 * (i * page_count))}`: `{track.title[0:100]}` " \
                           f"[[`{get_time_length(track.length / 1000)}`]({track.uri})]\n" \
                           f"`Author:` {track.author[0:100]}\n\n"

        embed = Embed(title=f"🎶 {guild_name}'s Queue", description=description, color=0x38f2ff)

        if main_video_uri:
            embed.set_image(url=get_video_thumbnail_url(main_video_uri))

        pages.append(embed)

    return pages

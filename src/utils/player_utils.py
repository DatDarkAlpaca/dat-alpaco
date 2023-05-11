import wavelink


async def play_next(player: wavelink.Player):
    if player.queue.is_empty:
        return

    track = player.queue.get()
    if track:
        await player.play(track)
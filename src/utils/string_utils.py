import re


def get_youtube_video_thumbnail_url(video_uri: str) -> str | None:
    if not video_uri.startswith('https://www.youtube.com/'):
        return None

    video_id = video_uri.split("watch?v=")[1].split("&")[0]
    return f"https://img.youtube.com/vi/{video_id}/0.jpg"


def get_spotify_video_thumbnail_url(images: list[str]) -> str:
    return images[0]


def get_spotify_track_url(spotify_uri: str) -> str:
    return f"https://open.spotify.com/track/{spotify_uri.split(':')[-1]}"


def is_youtube_playlist(url: str) -> bool:
    result = re.search("^.*(youtu.be\/|list=)([^#\&\?]*).*", url)
    return result is not None


def is_youtube_url(url: str) -> bool:
    result = re.search("^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|v\/)?)([\w\-]+)(\S+)?$", url)
    return result is not None


def is_spotify_url(url: str) -> bool:
    result = re.search("^(spotify:|https:\/\/[a-z]+\.spotify\.com\/)", url)
    return result is not None


def is_sound_cloud_url(url: str) -> bool:
    result = re.search("^https?:\/\/(soundcloud\.com|snd\.sc)\/(.*)$", url)
    return result is not None

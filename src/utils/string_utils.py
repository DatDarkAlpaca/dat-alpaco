import requests


def get_video_thumbnail_url(video_uri: str):
    if not video_uri.startswith('https://www.youtube.com/'):
        return None

    video_id = video_uri.split("watch?v=")[1].split("&")[0]
    return f"https://img.youtube.com/vi/{video_id}/0.jpg"


def is_youtube_url(url: str) -> bool:
    return len(requests.get(url).text) > 0

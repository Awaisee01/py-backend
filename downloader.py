
import yt_dlp
from flask import Response

def download_video(url, format="video"):
    try:
        ydl_opts = {
            "format": "best" if format == "video" else "bestaudio",
            "quiet": True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info["url"]  # Get direct streaming URL
        
        return video_url, None  # Return the direct link to video/audio

    except Exception as e:
        return None, str(e)  # Return error message

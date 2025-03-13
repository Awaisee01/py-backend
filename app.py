

import os
from flask import Flask, request, Response
import yt_dlp

app = Flask(__name__)

def download_progress(d):
    if d['status'] == 'downloading':
        percentage = d['_percent_str'].strip()
        print(f"Download progress: {percentage}")

        

@app.route('/download', methods=['GET'])
@app.route('/')
def home():
    return "Flask App is Running!"
def download():
    url = request.args.get("url")
    format_type = request.args.get("format", "video")

    if not url:
        return "Missing URL", 400

    ydl_opts = {
        'format': 'bestaudio' if format_type == 'audio' else 'best',
        'progress_hooks': [download_progress],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return Response("Download Complete", status=200)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))  # Get PORT from environment
    app.run(debug=True, host="0.0.0.0", port=port)


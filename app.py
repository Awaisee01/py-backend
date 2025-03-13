# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from downloader import download_video

# app = Flask(__name__)
# CORS(app)

# @app.route("/")
# def home():
#     return jsonify({"message": "YouTube Downloader API is running!"})
# @app.route("/download", methods=["GET"])
# def download():
#     url = request.args.get("url")
#     format_type = request.args.get("format", "video")

#     if not url:
#         return jsonify({"error": "URL is required"}), 400

#     download_url, error = download_video(url, format_type)
    
#     if error:
#         return jsonify({"error": "Failed to fetch video", "details": error}), 500

#     return jsonify({"download_url": download_url})

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)



from flask import Flask, request, Response
import yt_dlp

app = Flask(__name__)

def download_progress(d):
    if d['status'] == 'downloading':
        percentage = d['_percent_str'].strip()
        print(f"Download progress: {percentage}")

@app.route('/download', methods=['GET'])
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
    app.run(debug=True, host="0.0.0.0", port=8000)


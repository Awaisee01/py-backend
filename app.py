# import os
# import re
# import time
# import threading
# import tempfile  # ✅ Use system temp directory
# from flask import Flask, request, send_file, jsonify, after_this_request
# from flask_cors import CORS
# import yt_dlp
# import uuid  # ✅ Generate unique filenames

# app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})

# # ✅ Use system temporary directory instead of current directory
# TEMP_DIR = tempfile.gettempdir()

# @app.route("/download", methods=["GET"])
# def download():
#     url = request.args.get("url")
#     format_type = request.args.get("format", "video")

#     if not url:
#         return jsonify({"error": "Missing URL"}), 400

#     try:
#         # ✅ Extract video info without downloading
#         ydl_opts_info = {"quiet": True}
#         with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
#             info = ydl.extract_info(url, download=False)
#             video_title = info.get("title", "video").replace(" ", "_")

#         # ✅ Sanitize filename
#         video_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

#         # ✅ Generate unique filename
#         unique_id = uuid.uuid4().hex[:8]
#         filename = f"{video_title}_{unique_id}.mp4" if format_type == "video" else f"{video_title}_{unique_id}.mp3"
#         output_path = os.path.join(TEMP_DIR, filename)
#         ydl_opts = {
#             "format": "bestaudio" if format_type == "audio" else "best",
#             "outtmpl": output_path, 
#             "noplaylist": True,
#             "quiet": True,
#         }
      


#         # ✅ Download the file
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])

#         # ✅ Ensure file exists before sending
#         if not os.path.exists(output_path):
#             return jsonify({"error": "File not found"}), 500

#         print(f"File ready for download: {output_path}")

#         # ✅ Asynchronously delete file after response
#         @after_this_request
#         def remove_file(response):
#             def delete_file():
#                 time.sleep(10)  # Wait to ensure file is not locked
#                 try:
#                     os.remove(output_path)
#                     print(f"✅ Deleted file: {output_path}")
#                 except Exception as e:
#                     print(f"❌ Error deleting file: {e}")
                    

#             threading.Thread(target=delete_file, daemon=True).start()
#             return response

#         return send_file(output_path, as_attachment=True)

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000)) if os.environ.get("PORT") else 8000
#     app.run(debug=True, host="0.0.0.0", port=port)












import os
import re
import time
import threading
import tempfile
from flask import Flask, request, send_file, jsonify, after_this_request
from flask_cors import CORS
import yt_dlp
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Use system temporary directory
TEMP_DIR = tempfile.gettempdir()

@app.route("/download", methods=["GET"])
def download():
    url = request.args.get("url")
    format_type = request.args.get("format", "video")

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        # Extract video info without downloading
        ydl_opts_info = {"quiet": True}
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url, download=False)
            video_title = info.get("title", "video").replace(" ", "_")

        # Sanitize filename
        video_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

        # Generate unique filename
        unique_id = uuid.uuid4().hex[:8]
        filename = f"{video_title}_{unique_id}.mp4" if format_type == "video" else f"{video_title}_{unique_id}.mp3"
        output_path = os.path.join(TEMP_DIR, filename)

        # Download options
        ydl_opts = {
            "format": "bestaudio/best" if format_type == "audio" else "best",
            "outtmpl": output_path,
            "noplaylist": True,
            "quiet": True,
            "cookies": "cookies.txt",  # Add cookies to bypass bot detection
        }

        # Download the file
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Ensure file exists before sending
        if not os.path.exists(output_path):
            return jsonify({"error": "File not found"}), 500

        print(f"File ready for download: {output_path}")

        # Delete file after response
        @after_this_request
        def remove_file(response):
            def delete_file():
                time.sleep(10)  # Wait for the file to be fully sent
                try:
                    os.remove(output_path)
                    print(f"✅ Deleted file: {output_path}")
                except Exception as e:
                    print(f"❌ Error deleting file: {e}")

            threading.Thread(target=delete_file, daemon=True).start()
            return response

        return send_file(output_path, as_attachment=True, download_name=filename)

    except yt_dlp.utils.DownloadError as e:
        print(f"DownloadError: {e}")
        return jsonify({"error": f"Download failed: {str(e)}"}), 500
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) if os.environ.get("PORT") else 8000
    app.run(debug=True, host="0.0.0.0", port=port)
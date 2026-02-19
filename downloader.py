import yt_dlp
import os
import uuid

DOWNLOAD_FOLDER = "downloads"


def download_video(url: str) -> str:
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

    unique_id = str(uuid.uuid4())
    output_path = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.%(ext)s")

    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as e:
        raise RuntimeError(f"Failed to download video: {e}")

    # Fall back to mp4 if extension not present
    file_extension = info.get("ext") or "mp4"

    final_file = os.path.join(DOWNLOAD_FOLDER, f"{unique_id}.{file_extension}")

    if not os.path.exists(final_file):
        raise RuntimeError(f"Expected downloaded file not found: {final_file}")

    return final_file

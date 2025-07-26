from pytube import YouTube
from pathlib import Path
import re


def clean_and_convert_url(url):
    # Remove tracking parameters
    clean_url = url.split("&")[0].split("?")[0]

    # Convert youtu.be to full youtube link
    match = re.match(r"https?://youtu\.be/([a-zA-Z0-9_-]+)", clean_url)
    if match:
        video_id = match.group(1)
        return f"https://www.youtube.com/watch?v={video_id}"
    return clean_url


# Get Downloads folder
downloads_dir = Path.home() / "Downloads"

# Get URL from user
raw_url = input("Enter the URL of the video: ")
url = clean_and_convert_url(raw_url)

try:
    yt = YouTube(url)
    print(f"Downloading: {yt.title}")
    stream = yt.streams.get_highest_resolution()
    stream.download(output_path=downloads_dir)
    print(f"Downloaded to: {downloads_dir}")
except Exception as e:
    print("Error:", e)

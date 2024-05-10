#!/usr/bin/python3

import argparse
import os
from pathlib import Path

import requests
import yt_dlp

parser = argparse.ArgumentParser()
parser.add_argument("video_url", help="Path to a youtube video")
args = parser.parse_args()

ydl_opts = {
    "format": "m4a/bestaudio/best",
    # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
    "postprocessors": [
        {  # Extract audio using ffmpeg
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
        }
    ],
    "outtmpl": "audio.m4a",
}
URLS = [args.video_url]

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    error_code = ydl.download(URLS)

audio_file = Path("audio.m4a")
transcription = Path("transcription")
if not transcription.exists():
    print("Transcribing audio... %s" % args.audio_file)
    transcribe_url = "http://sgn.space:11000/transcribe"
    files = {"audio_file": open(audio_file, "rb")}
    response = requests.post(transcribe_url, files=files)
    with open("transcription", "w") as f:
        f.write(response.text)
else:
    print("Audio transcription already exists")

trimmed_transcription = Path("trimmed_transcription")
if not trimmed_transcription.exists():
    print("Trimming transcription...")
    trim_url = "http://localhost:8001/trim"
    files = {"transcription_file": open("transcription", "r")}
    response = requests.post(trim_url, files=files)
    with open("trimmed_transcription", "w") as f:
        f.write(response.text)
else:
    print("Trimmed transcription already exists")

chopped_audio = Path("chopped_audio.opus")
if not chopped_audio.exists():
    print("Chopping audio...")
    chop_url = "http://sgn.space:11001/chop"
    files = {
        "transcription_file": open("trimmed_transcription", "r"),
        "audio_file": open(audio_file, "rb"),
    }
    response = requests.post(chop_url, files=files)
    with open("chopped_audio.opus", "wb") as f:
        f.write(response.content)
else:
    print("Chopped audio already exists")

os.remove(audio_file)

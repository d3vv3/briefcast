#!/bin/bash

# Download the audio
# yt-dlp -x --audio-format mp3 -P /tmp/briefcast -o "podcast.mp3" "$@"

# Transcribe the audio
# curl \
#   -X POST "http://localhost:11000/transcribe?beam_size=5" \
#   -F audio_file=@/tmp/briefcast/podcast.mp3 \
#   -o /tmp/transcript.txt

# Trim the transcription
# curl \
#   -X POST "http://localhost:11000/trim" \
#   -F transcription_file=@/tmp/transcript.txt \
#   -o /tmp/trimmed_transcript.txt

# Chop the audio
curl \
  -X POST "http://localhost:11000/chop" \
  -F transcription_file=@/tmp/trimmed_transcript.txt \
  -F audio_file=@/tmp/briefcast/podcast.mp3 \
  -o /tmp/result.mp3

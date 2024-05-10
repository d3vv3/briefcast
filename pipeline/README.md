# Pipeline

## Description

This is a simple pipeline that downloads a video from YouTube and extracts the audio from it.
Then, it transcribes the audio to text with an API call.
Then, it selects the highlighted parts from it and saves them in a file.
Finally, it sends the trimmed_transcription and the original audio to a chopper,
generating a new audio file with only the highlighted parts.

Example:
```
./app.py https://youtu.be/bc6uFV9CJGg
```

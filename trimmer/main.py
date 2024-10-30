import os

from fastapi import FastAPI, UploadFile
import google.generativeai as genai

app = FastAPI()
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

prompt = """**Input**: A transcript file with timestamps (format: [start_time -> end_time] text)
**Task**: Filter out lines that are not relevant to the main topic of the podcast transcription, condensing the transcript to focus on the primary discussion.
**Objective**: Reduce the overall time of the transcription by removing:
    - Off-topic conversations
    - Unrelated tangents
    - Intro/outro segments (e.g., opening credits, closing remarks)
    - Unnecessary filler words (e.g., "um," "ah")
    - Any other non-essential content
**Output**: A condensed transcript file with timestamps (format: [start_time -> end_time] text), containing only the relevant lines that align with the main topic of the podcast.
**Example Input**:
```
[1,00s -> 3,00s] Hello and welcome to our podcast!
[4,00s -> 6,00s] Today we're discussing the impact of AI on society.
[7,00s -> 10,00s] Um, can you hear me okay?
[11,00s -> 15,00s] Absolutely, let's dive into the topic.
```

**Example Output**:
```
[4,00s -> 6,00s] Today we're discussing the impact of AI on society.
[11,00s -> 15,00s] Absolutely, let's dive into the topic.
```

**Note**: The output transcript should maintain the original timestamp format and only include the relevant lines that align with the main topic.
**Important**: Only output the condensed transcript file, without any additional text or explanations. The output should consist solely of the relevant lines with timestamps, formatted as shown above.

Input transcription:

{transcription}

Output:
"""

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/trim")
def trim(transcription_file: UploadFile):
    transcription_text = transcription_file.file.read().decode("utf-8")
    response = model.generate_content(prompt.format(transcription=transcription_text))
    return {"trimmed_transcription": response.text}

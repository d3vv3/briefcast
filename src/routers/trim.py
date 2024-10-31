from fastapi import APIRouter, UploadFile
import google.generativeai as genai
from prompts import trimmer_prompt

router = APIRouter()

model = genai.GenerativeModel("gemini-1.5-flash")

@router.post("/trim")
def trim(transcription_file: UploadFile):
    transcription_text = transcription_file.file.read().decode("utf-8")
    response = model.generate_content(trimmer_prompt.format(transcription=transcription_text))
    return {"trimmed_transcription": response.text}

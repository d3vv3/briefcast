import os

from fastapi import FastAPI, UploadFile
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory,
)
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

app = FastAPI()
llm = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)


prompt = PromptTemplate.from_template(
    """Here is the transcription file of a podcast.
Remove lines that are not too important to the main content of the podcast. Do not answer any other text.
The result should remain coherent and informative. Keep the original text. Do not add or change any information to the lines you decide to keep.
Transcription:
{transcription}"""
)

output_parser = StrOutputParser()
chain = prompt | llm | output_parser


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.post("/trim")
def trim(transcription_file: UploadFile):
    response = chain.invoke(
        {"transcription": transcription_file.file.read().decode("utf-8")}
    )
    return {"trimmed_transcription": response}

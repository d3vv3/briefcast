import os

from fastapi import FastAPI, UploadFile
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "https://ollama.example.org")

app = FastAPI()
llm = Ollama(base_url=OLLAMA_HOST, model=OLLAMA_MODEL)

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

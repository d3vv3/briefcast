import os

from fastapi import FastAPI, Response, UploadFile
from faster_whisper import WhisperModel
from loguru import logger

whisper_model = os.environ.get("WHISPER_MODEL", "large-v3")
device = os.environ.get("DEVICE", "auto")
compute_type = os.environ.get("COMPUTE_TYPE", "float16")

model = WhisperModel(
    whisper_model, device=device, compute_type=compute_type, download_root="models"
)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


# TODO: Make parameters adjustable with form-data or similar
@app.post("/transcribe")
async def transcribe(audio_file: UploadFile):
    logger.info(audio_file.filename)
    # audio_content = await audio_file.read()
    segments, info = model.transcribe(audio_file.file, beam_size=5)
    logger.info(
        "Detected language '%s' with probability %f"
        % (info.language, info.language_probability)
    )
    result = []
    for segment in segments:
        line = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
        logger.info(line)
        result.append(line)
    return Response(content="\n".join(result), media_type="text/plain")

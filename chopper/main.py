import mimetypes
import tempfile

import ffmpeg
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from loguru import logger

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/chop")
async def transcribe(
    audio_file: UploadFile, transcription_file: UploadFile
) -> FileResponse:
    logger.info("audio file name: %s" % audio_file.filename)
    logger.info("audio file content_type: %s" % audio_file.content_type)
    logger.info("transcription file name: %s" % transcription_file.filename)
    cuts = []
    for line in transcription_file.file.read().decode("utf-8").split("\n")[:-1]:
        start, end = line[1:].split("s]")[0].split("s -> ")
        cuts.append("between(t,%s,%s)" % (start, end))
    media_type = mimetypes.guess_type(audio_file.filename)[0]
    media_extension = ".%s" % audio_file.filename.split(".")[-1]
    logger.info("guessed media type: %s" % media_type)
    with tempfile.NamedTemporaryFile(suffix=media_extension, delete=False) as tmp_file:
        out_filename = tmp_file.name
        process = (
            ffmpeg.input("pipe:")
            .filter("aselect", "+".join(cuts))
            .filter("asetpts", "N/SR/TB")
            .output(out_filename)
            .overwrite_output()
            .run_async(pipe_stdin=True)
        )
        process.communicate(input=audio_file.file.read())
        return FileResponse(
            path=out_filename,
            media_type=media_type,
            filename="result%s" % media_extension,
        )

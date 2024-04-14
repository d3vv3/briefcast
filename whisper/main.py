import os
from datetime import datetime
from typing import Iterable, List, Optional, Tuple, Union

from fastapi import FastAPI, Response, UploadFile
from faster_whisper import WhisperModel
from faster_whisper.vad import VadOptions
from loguru import logger

WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "large-v3")
DEVICE = os.environ.get("DEVICE", "auto")
COMPUTE_TYPE = os.environ.get("COMPUTE_TYPE", "float16")

model = WhisperModel(
    WHISPER_MODEL,
    device=DEVICE,
    compute_type=COMPUTE_TYPE,
    download_root="models",
)

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.post("/transcribe")
async def transcribe(
    audio_file: UploadFile,
    language: str = None,
    beam_size: int = 5,
    best_of: int = 5,
    patience: float = 1,
    length_penalty: float = 1,
    repetition_penalty: float = 1,
    no_repeat_ngram_size: int = 0,
    temperature: Union[float, List[float], Tuple[float, ...]] = [
        0.0,
        0.2,
        0.4,
        0.6,
        0.8,
        1.0,
    ],
    compression_ratio_threshold: Optional[float] = 2.4,
    log_prob_threshold: Optional[float] = -1.0,
    no_speech_threshold: Optional[float] = 0.6,
    condition_on_previous_text: bool = True,
    prompt_reset_on_temperature: float = 0.5,
    initial_prompt: Optional[Union[str, Iterable[int]]] = None,
    prefix: Optional[str] = None,
    suppress_blank: bool = True,
    suppress_tokens: Optional[List[int]] = [-1],
    without_timestamps: bool = False,
    max_initial_timestamp: float = 1.0,
    word_timestamps: bool = False,
    prepend_punctuations: str = "\"'“¿([{-",
    append_punctuations: str = "\"'.。,，!！?？:：”)]}、",
    vad_filter: bool = False,
    vad_parameters: Optional[Union[dict, VadOptions]] = None,
    max_new_tokens: Optional[int] = None,
    chunk_length: Optional[int] = None,
    clip_timestamps: Union[str, List[float]] = "0",
    hallucination_silence_threshold: Optional[float] = None,
    language_detection_threshold: Optional[float] = None,
    language_detection_segments: int = 1,
) -> Response:
    """Transcribes an input file.

    Arguments:
      audio: Path to the input file (or a file-like object), or the audio waveform.
      language: The language spoken in the audio. It should be a language code such
        as "en" or "fr". If not set, the language will be detected in the first 30 seconds
        of audio.
      task: Task to execute (transcribe or translate).
      beam_size: Beam size to use for decoding.
      best_of: Number of candidates when sampling with non-zero temperature.
      patience: Beam search patience factor.
      length_penalty: Exponential length penalty constant.
      repetition_penalty: Penalty applied to the score of previously generated tokens
        (set > 1 to penalize).
      no_repeat_ngram_size: Prevent repetitions of ngrams with this size (set 0 to disable).
      temperature: Temperature for sampling. It can be a tuple of temperatures,
        which will be successively used upon failures according to either
        `compression_ratio_threshold` or `log_prob_threshold`.
      compression_ratio_threshold: If the gzip compression ratio is above this value,
        treat as failed.
      log_prob_threshold: If the average log probability over sampled tokens is
        below this value, treat as failed.
      no_speech_threshold: If the no_speech probability is higher than this value AND
        the average log probability over sampled tokens is below `log_prob_threshold`,
        consider the segment as silent.
      condition_on_previous_text: If True, the previous output of the model is provided
        as a prompt for the next window; disabling may make the text inconsistent across
        windows, but the model becomes less prone to getting stuck in a failure loop,
        such as repetition looping or timestamps going out of sync.
      prompt_reset_on_temperature: Resets prompt if temperature is above this value.
        Arg has effect only if condition_on_previous_text is True.
      initial_prompt: Optional text string or iterable of token ids to provide as a
        prompt for the first window.
      prefix: Optional text to provide as a prefix for the first window.
      suppress_blank: Suppress blank outputs at the beginning of the sampling.
      suppress_tokens: List of token IDs to suppress. -1 will suppress a default set
        of symbols as defined in the model config.json file.
      without_timestamps: Only sample text tokens.
      max_initial_timestamp: The initial timestamp cannot be later than this.
      word_timestamps: Extract word-level timestamps using the cross-attention pattern
        and dynamic time warping, and include the timestamps for each word in each segment.
      prepend_punctuations: If word_timestamps is True, merge these punctuation symbols
        with the next word
      append_punctuations: If word_timestamps is True, merge these punctuation symbols
        with the previous word
      vad_filter: Enable the voice activity detection (VAD) to filter out parts of the audio
        without speech. This step is using the Silero VAD model
        https://github.com/snakers4/silero-vad.
      vad_parameters: Dictionary of Silero VAD parameters or VadOptions class (see available
        parameters and default values in the class `VadOptions`).
      max_new_tokens: Maximum number of new tokens to generate per-chunk. If not set,
        the maximum will be set by the default max_length.
      chunk_length: The length of audio segments. If it is not None, it will overwrite the
        default chunk_length of the FeatureExtractor.
      clip_timestamps: Union[str, List[float]]
        Comma-separated list start,end,start,end,... timestamps (in seconds) of clips to
         process. The last end timestamp defaults to the end of the file.
         vad_filter will be ignored if clip_timestamps is used.
      hallucination_silence_threshold: Optional[float]
        When word_timestamps is True, skip silent periods longer than this threshold
         (in seconds) when a possible hallucination is detected
      language_detection_threshold: If the maximum probability of the language tokens is higher
       than this value, the language is detected.
      language_detection_segments: Number of segments to consider for the language detection.
    """
    logger.info(audio_file.filename)
    start = datetime.now()
    segments, info = model.transcribe(
        audio_file.file,
        beam_size=beam_size,
        best_of=best_of,
        patience=patience,
        length_penalty=length_penalty,
        repetition_penalty=repetition_penalty,
        no_repeat_ngram_size=no_repeat_ngram_size,
        temperature=temperature,
        compression_ratio_threshold=compression_ratio_threshold,
        log_prob_threshold=log_prob_threshold,
        no_speech_threshold=no_speech_threshold,
        condition_on_previous_text=condition_on_previous_text,
        prompt_reset_on_temperature=prompt_reset_on_temperature,
        initial_prompt=initial_prompt,
        prefix=prefix,
        suppress_blank=suppress_blank,
        suppress_tokens=suppress_tokens,
        without_timestamps=without_timestamps,
        max_initial_timestamp=max_initial_timestamp,
        word_timestamps=word_timestamps,
        prepend_punctuations=prepend_punctuations,
        append_punctuations=append_punctuations,
        vad_filter=vad_filter,
        vad_parameters=vad_parameters,
        max_new_tokens=max_new_tokens,
        chunk_length=chunk_length,
        clip_timestamps=clip_timestamps,
        hallucination_silence_threshold=hallucination_silence_threshold,
    )
    language_guess_end = datetime.now()
    logger.info("Language guess took %s seconds" % (language_guess_end - start).seconds)
    logger.info(
        "Detected language '%s' with probability %f"
        % (info.language, info.language_probability)
    )
    result = []
    for segment in segments:
        line = "[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text)
        logger.info(line)
        result.append(line)
    transcription_end = datetime.now()
    logger.info(
        "Transcription took %s seconds"
        % (transcription_end - language_guess_end).seconds,
    )
    logger.info(
        "Speed: x%s"
        % (info.duration / (transcription_end - language_guess_end).seconds)
    )
    return Response(content="\n".join(result), media_type="text/plain")

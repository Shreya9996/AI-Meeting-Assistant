import whisper
import os
from dotenv import load_dotenv

from utils.audio_processor import process_input

load_dotenv()


WHISPER_MODEL = os.getenv("WHISPER_MODEL","small")

_modle = None

def load_modle():
    global _modle

    if _modle is None:
        fp16=False
        print(f"Loading whisper modle .......")
        _modle = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded successfully ! ")

    return _modle


load_modle()

def transcribe_chunk(chunk_path : str,translate : bool = False) -> str:
    model = load_modle()
    task = "translate" if translate else "transcribe"
    result = model.transcribe(chunk_path,task=task,fp16=False)

    return result["text"]

def transcribe_all(chunks : list,translate:bool = False) ->str:
    full_transcript = " "

    for i ,chunk in enumerate(chunks):
        print(f"Transcribing chunk {i+1}")
        text = transcribe_chunk(chunk , translate=translate)

        full_transcript += text + "  "

    print("Transcripation Completed ! ")

    return full_transcript




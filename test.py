from utils.audio_processor import process_input
from core.transcriber import transcribe_all


source = "https://youtu.be/Ty8gcCKuwNI?si=MxuDt9D7TavU-gkw"

chunks = process_input(source)

transcribe_text = transcribe_all(chunks)

print(transcribe_text)


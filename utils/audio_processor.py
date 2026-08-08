import yt_dlp
from pydub import AudioSegment
import os

DOWNLOAD_DIR = "downloades"
os.makedirs(DOWNLOAD_DIR,exist_ok=True)


def download_youtube_audio(url : str)->str:
    output_path = os.path.join(DOWNLOAD_DIR,"%(title)s.%(ext)s")

    ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": output_path,
    
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }
    ],
}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url,download=True)

            filename = ydl.prepare_filename(info).replace(".webm",".wav").replace(".m4a",".wav")

    return filename


# data = download_youtube_audio("https://youtu.be/Ty8gcCKuwNI?si=MxuDt9D7TavU-gkw")


def convert_to_wav(input_path: str) -> str:
    """
    Convert any audio/video file to mono 16 kHz WAV.
    """

    output_path = os.path.splitext(input_path)[0] + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = audio.set_channels(1).set_frame_rate(16000)

    audio.export(output_path, format="wav")

    return output_path



def chunk_audio(wav_path:str,chunk_mintues : int = 10)->list:

     audio = AudioSegment.from_wav(wav_path)
     chunk_ms = chunk_mintues * 60 * 1000
     chunks = []

     for i,start in enumerate(range(0,len(audio),chunk_ms)):
          chunk = audio[start:start+chunk_ms]
          chunk_path = f"{wav_path}_chunk_{i}.wav"
          chunk.export(chunk_path,format="wav")

          chunks.append(chunk_path)


     return chunks


def process_input(source : str)->list:

     if source.startswith("http://") or source.startswith("https://"):
          print("Detected Youtube Url .......Downloading audion .....")

          wav_path = download_youtube_audio(source)

     else :
          print("Detected loacal file .....converting to wav ......")
          wav_path = convert_to_wav(source)

     print("Chunking Audion .....")
     chunks = chunk_audio(wav_path)
     print(f"Audio ready - {len(chunks)} chunks created . ")


     return chunks

# print(process_input("https://youtu.be/Ty8gcCKuwNI?si=MxuDt9D7TavU-gkw"))

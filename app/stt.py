import whisper
import os

MODEL_NAME = "medium"

model = whisper.load_model(MODEL_NAME)

def transcribe_audio(audio_path):
    """
    Transcribe audio menggunakan Whisper
    """

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio tidak ditemukan: {audio_path}")

    result = model.transcribe(audio_path, language="id")

    transcript = result["text"].strip()

    return transcript
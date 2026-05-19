import pyttsx3
import os

engine = pyttsx3.init()

engine.setProperty('rate', 150)


def text_to_speech(text, output_path="outputs/response.wav"):
    """
    Convert text menjadi speech
    """

    os.makedirs("outputs", exist_ok=True)

    engine.save_to_file(text, output_path)
    engine.runAndWait()

    return output_path
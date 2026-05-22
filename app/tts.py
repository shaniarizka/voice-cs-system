import pyttsx3
import os


def text_to_speech(text, output_path="outputs/response.wav"):

    """
    Convert text menjadi speech
    """

    os.makedirs("outputs", exist_ok=True)

    try:

        engine = pyttsx3.init()

        engine.setProperty("rate", 150)

        engine.save_to_file(text, output_path)
        engine.runAndWait()

        engine.stop()

        print(f"[TTS SAVED] {output_path}")

        return output_path

    except Exception as e:

        print("TTS ERROR:", e)

        return None
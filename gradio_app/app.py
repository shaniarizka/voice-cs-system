import gradio as gr
import sys
import os

# =========================
# ROOT PATH
# =========================

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.insert(0, ROOT_DIR)

# =========================
# IMPORT MODULE
# =========================

from app.stt import transcribe_audio
from app.llm import generate_response
from app.tts import text_to_speech

# =========================
# MAIN PIPELINE
# =========================

def voice_chat(audio_path, mode):

    # =========================
    # STT
    # =========================

    transcript = transcribe_audio(audio_path)

    # =========================
    # LLM
    # =========================

    llm_result = generate_response(
        transcript,
        mode=mode
    )

    response_text = llm_result["text"]

    # =========================
    # TTS
    # =========================

    output_audio = "outputs/gradio_response.wav"

    text_to_speech(
        response_text,
        output_audio
    )

    return (
        transcript,
        response_text,
        output_audio
    )

# =========================
# GRADIO INTERFACE
# =========================

demo = gr.Interface(

    fn=voice_chat,

    inputs=[

        gr.Audio(
            type="filepath",
            label="Upload Audio"
        ),

        gr.Dropdown(
            choices=[
                "preserve",
                "normalize"
            ],
            value="preserve",
            label="Response Mode"
        )
    ],

    outputs=[

        gr.Textbox(label="Transcript"),

        gr.Textbox(label="LLM Response"),

        gr.Audio(label="Speech Output")
    ],

    title="Code-Switching Speech-to-Speech System",

    description=(
        "Pipeline multilingual:\n"
        "Speech → STT → LLM → TTS\n"
        "Mendukung Bahasa Indonesia, English, dan Arabic."
    )
)

# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    demo.launch()
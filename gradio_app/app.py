import gradio as gr
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from app.stt import transcribe_audio
from app.llm import generate_response
from app.tts import text_to_speech


def voice_chat(audio_path):

    # STEP 1 — STT
    transcript = transcribe_audio(audio_path)

    # STEP 2 — LLM
    response = generate_response(
        transcript,
        mode="preserve"
    )

    # STEP 3 — TTS
    output_audio = text_to_speech(response)

    return transcript, response, output_audio


demo = gr.Interface(
    fn=voice_chat,
    inputs=gr.Audio(type="filepath"),
    outputs=[
        gr.Textbox(label="Transcript"),
        gr.Textbox(label="LLM Response"),
        gr.Audio(label="Speech Output")
    ],
    title="Code-Switching Speech-to-Speech System",
    description="STT → LLM → TTS pipeline untuk Bahasa Indonesia, English, dan Arabic."
)

demo.launch(share=True)
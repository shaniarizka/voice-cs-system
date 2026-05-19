from app.stt import transcribe_audio
from app.llm import generate_response
from app.tts import text_to_speech

audio_path = "data/corpus/audio/2367_audio1.wav"

# STEP 1 — STT
transcript = transcribe_audio(audio_path)

print("\n=== TRANSCRIPT ===")
print(transcript)

# STEP 2 — LLM
response = generate_response(transcript, mode="preserve")

print("\n=== RESPONSE ===")
print(response)

# STEP 3 — TTS
audio_output = text_to_speech(response)

print("\n=== OUTPUT AUDIO ===")
print(audio_output)
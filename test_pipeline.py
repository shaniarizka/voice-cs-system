from app.stt import transcribe_audio
from app.llm import generate_response

audio_path = "data/corpus/audio/2367_audio1.wav"

# STT
transcript = transcribe_audio(audio_path)

print("\n=== TRANSCRIPT ===")
print(transcript)

# LLM
response = generate_response(transcript, mode="preserve")

print("\n=== RESPONSE ===")
print(response)
from app.stt import transcribe_audio

audio_path = "data/corpus/audio/2367_audio1.wav"

result = transcribe_audio(audio_path)

print("\n=== HASIL TRANSKRIP ===")
print(result)
import os
import json
import time
import pandas as pd

from jiwer import wer, cer
from app.tts import text_to_speech
from app.stt import transcribe_audio
from app.llm import generate_response

# =========================
# PATH
# =========================

AUDIO_DIR = "data/corpus/audio"
GROUND_TRUTH_PATH = "data/corpus/transcripts/ground_truth.json"

# =========================
# CONFIG
# =========================

USE_LLM = True
USE_TTS = True
LLM_MODE = "normalize"

# =========================
# LOAD GROUND TRUTH
# =========================

with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
    ground_truth_data = json.load(f)

results = []

success_count = 0
failed_count = 0

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# LOOP SEMUA AUDIO 
# =========================

for filename in os.listdir(AUDIO_DIR):

    # hanya proses file wav
    if not filename.lower().endswith(".wav"):
        continue

    print(f"\nProcessing: {filename}")

    audio_path = os.path.join(AUDIO_DIR, filename)


    try:

        raw_id = filename.split("_", 1)[1].replace(".wav", "")

        # lowercase agar Audio/audio/AUDIO sama
        raw_id = raw_id.lower()

        # ambil angka saja
        number = ''.join(filter(str.isdigit, raw_id))

        # jika tidak ada angka
        if not number:

            print("FORMAT NAMA FILE INVALID:", filename)
            continue

        # format jadi audio01, audio02, dst
        audio_id = f"audio{int(number):02d}"

    except Exception as e:

        print("ERROR PARSING FILENAME:", filename)
        print(e)
        continue

    # =========================
    # AMBIL GROUND TRUTH
    # =========================

    ground_truth = ground_truth_data.get(audio_id, "")

    print("GROUND TRUTH :", ground_truth)

    if not ground_truth:

        print("GROUND TRUTH TIDAK DITEMUKAN:", filename)

    # =========================
    # START TIMER
    # =========================

    start_time = time.time()

    # =========================
    # STT
    # =========================

    try:

        transcript = transcribe_audio(audio_path)

    except Exception as e:

        print("STT Error:", e)
        transcript = ""
        failed_count += 1

    print("TRANSCRIPT   :", transcript)

    if transcript.strip():
        success_count += 1
    else:
        failed_count += 1

    if not transcript.strip():
        print("TRANSCRIPT KOSONG, skip file.")
        continue    

    # =========================
    # EVALUASI
    # =========================

    try:

        wer_score = wer(ground_truth, transcript)
        cer_score = cer(ground_truth, transcript)

    except Exception as e:

        print("EVALUATION ERROR:", e)

        wer_score = 1.0
        cer_score = 1.0

    # =========================
    # LLM
    # =========================

    if USE_LLM:

        try:

            llm_result = generate_response(
                transcript,
                mode=LLM_MODE
            )

            response = llm_result["text"]
            llm_source = llm_result["source"]

        except Exception as e:

            response = f"LLM Error: {e}"
            llm_source = "error"

    else:

        response = "[LLM DISABLED]"

    print("RESPONSE     :", response)
    print("LLM SOURCE   :", llm_source)

    # =========================
    # TTS
    # =========================

    if USE_TTS:

        base_name = os.path.splitext(filename)[0]
        output_audio_path = os.path.join(
            OUTPUT_DIR,
            f"{base_name}_{LLM_MODE}_response.wav"
        )

        try:

            text_to_speech(
                response,
                output_audio_path
            )

        except Exception as e:

            print("TTS Error:", e)

    # =========================
    # LATENCY
    # =========================

    end_time = time.time()
    latency = end_time - start_time

    print(f"LATENCY      : {latency:.2f} sec")

    # =========================
    # SAVE RESULT
    # =========================

    results.append({

        "filename": filename,
        "audio_id": audio_id,

        "ground_truth": ground_truth,
        "transcript": transcript,

        "wer": round(wer_score, 3),
        "cer": round(cer_score, 3),
        "latency": round(latency, 2),
        "response": response,
        "llm_source": llm_source,
        "llm_mode": LLM_MODE,
        "llm_enabled": USE_LLM
    })

# =========================
# SAVE CSV
# =========================

os.makedirs("logs", exist_ok=True)

results_df = pd.DataFrame(results)

output_csv = f"logs/evaluation_{LLM_MODE}.csv"

results_df.to_csv(
    output_csv,
    index=False,
    encoding="utf-8-sig"
)

results_df["response_length"] = (
    results_df["response"]
    .astype(str)
    .apply(len)
)
avg_response_length = results_df["response_length"].mean()
print(f"Average Response Length: {avg_response_length:.2f}")

# =========================
# SUMMARY
# =========================

print("\n=== SELESAI ===")
print(f"Hasil evaluasi disimpan ke: {output_csv}")

if len(results_df) > 0:

    avg_wer = results_df["wer"].mean()
    avg_cer = results_df["cer"].mean()
    avg_latency = results_df["latency"].mean()

    print(f"\nAverage WER: {avg_wer:.3f}")
    print(f"Average CER: {avg_cer:.3f}")
    print(f"Average Latency: {avg_latency:.2f} sec")

    print(f"Successful files: {success_count}")
    print(f"Failed files    : {failed_count}")
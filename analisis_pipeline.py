import os
import json
import pandas as pd

from jiwer import wer, cer

from app.stt import transcribe_audio
from app.llm import generate_response

# =========================
# PATH
# =========================

AUDIO_DIR = "data/corpus/audio"
GROUND_TRUTH_PATH = "data/corpus/transcripts/ground_truth.json"

# =========================
# LOAD GROUND TRUTH
# =========================

with open(GROUND_TRUTH_PATH, "r", encoding="utf-8") as f:
    ground_truth_data = json.load(f)

results = []

# =========================
# LOOP ALL AUDIO FILES
# =========================

for filename in os.listdir(AUDIO_DIR):

    # hanya proses file wav
    if not filename.lower().endswith(".wav"):
        continue

    print(f"\nProcessing: {filename}")

    audio_path = os.path.join(AUDIO_DIR, filename)

    # =========================
    # EXTRACT AUDIO ID
    # =========================
    # contoh:
    # 2305_audio18.wav
    # 2306_Audio01.wav
    # 999_AUDIO7.wav
    # -> audio18 / audio01 / audio07

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
    # STT
    # =========================

    try:

        transcript = transcribe_audio(audio_path)

    except Exception as e:

        print("STT Error:", e)
        transcript = ""

    print("TRANSCRIPT   :", transcript)

    # =========================
    # EVALUATION
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

    try:

        response = generate_response(
            transcript,
            mode="preserve"
        )

    except Exception as e:

        response = f"LLM Error: {e}"

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

        "response": response
    })

# =========================
# SAVE CSV
# =========================

os.makedirs("logs", exist_ok=True)

results_df = pd.DataFrame(results)

output_csv = "logs/evaluation_results.csv"

results_df.to_csv(
    output_csv,
    index=False,
    encoding="utf-8-sig"
)

# =========================
# SUMMARY
# =========================

print("\n=== SELESAI ===")
print(f"Hasil evaluasi disimpan ke: {output_csv}")

if len(results_df) > 0:

    avg_wer = results_df["wer"].mean()
    avg_cer = results_df["cer"].mean()

    print(f"\nAverage WER: {avg_wer:.3f}")
    print(f"Average CER: {avg_cer:.3f}")
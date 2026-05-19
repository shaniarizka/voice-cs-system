import os
import pandas as pd
from jiwer import wer, cer

from app.stt import transcribe_audio
from app.llm import generate_response

# =========================
# PATH
# =========================

AUDIO_DIR = "data/corpus/audio"
GROUND_TRUTH_PATH = "data/corpus/transcripts/ground_truth.csv"

# =========================
# LOAD GROUND TRUTH
# =========================

df_gt = pd.read_csv(GROUND_TRUTH_PATH)

results = []

# =========================
# PROCESS ALL AUDIO
# =========================

for index, row in df_gt.iterrows():

    filename = row["filename"]
    ground_truth = row["transcript"]

    audio_path = os.path.join(AUDIO_DIR, filename)

    print(f"\nProcessing: {filename}")

    # cek file ada
    if not os.path.exists(audio_path):

        print("Audio tidak ditemukan.")
        continue

    # =========================
    # STT
    # =========================

    try:

        transcript = transcribe_audio(audio_path)

    except Exception as e:

        print("STT Error:", e)

        transcript = ""

    # =========================
    # EVALUATION
    # =========================

    try:

        wer_score = wer(ground_truth, transcript)
        cer_score = cer(ground_truth, transcript)

    except:

        wer_score = 1.0
        cer_score = 1.0

    # =========================
    # LLM RESPONSE
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

print("\n=== SELESAI ===")
print(f"Hasil evaluasi disimpan ke: {output_csv}")

# =========================
# SUMMARY
# =========================

if len(results_df) > 0:

    avg_wer = results_df["wer"].mean()
    avg_cer = results_df["cer"].mean()

    print(f"\nAverage WER: {avg_wer:.3f}")
    print(f"Average CER: {avg_cer:.3f}")
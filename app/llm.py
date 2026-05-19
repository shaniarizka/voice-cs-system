import google.generativeai as genai
from dotenv import load_dotenv
import os

# =========================
# LOAD ENV
# =========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# =========================
# CONFIG GEMINI
# =========================

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

# =========================
# FALLBACK RESPONSE
# =========================

def fallback_response(user_text):

    text = user_text.lower()

    # flight
    if "flight" in text or "fly" in text or "jeddah" in text:

        return (
            "Baik, aku bisa bantu arrange flight "
            "ke Jeddah minggu depan."
        )

    # visa
    elif "visa" in text:

        return (
            "Untuk visa Saudi, biasanya diperlukan "
            "paspor aktif dan dokumen umrah."
        )

    # transport
    elif "transport" in text or "madinah" in text:

        return (
            "Baik, aku bisa bantu carikan transport "
            "dari Jeddah ke Madinah."
        )

    # hotel
    elif "hotel" in text or "makkah" in text:

        return (
            "Aku bisa bantu rekomendasikan hotel "
            "dekat Haram sesuai budget."
        )

    # default
    else:

        return "Maaf, saya belum memahami permintaan tersebut."

# =========================
# GENERATE RESPONSE
# =========================

def generate_response(user_text, mode="preserve"):

    """
    Generate response dari Gemini
    """

    if mode == "preserve":

        prompt = f"""
Kamu adalah assistant multilingual.

Balas dengan mempertahankan pola code-switching pengguna
(ID-EN-AR) secara natural.

User:
{user_text}
"""

    elif mode == "normalize":

        prompt = f"""
Kamu adalah assistant multilingual.

Ubah seluruh respon menjadi Bahasa Indonesia formal
dan hindari code-switching.

User:
{user_text}
"""

    else:

        raise ValueError("Mode tidak valid")

    # =========================
    # TRY GEMINI
    # =========================

    try:

        print("\n[INFO] Menggunakan Gemini API...")

        response = model.generate_content(prompt)

        return response.text.strip()

    # =========================
    # FALLBACK
    # =========================

    except Exception as e:

        print("\n[WARNING] Gemini gagal, menggunakan fallback response.")
        print(e)

        return fallback_response(user_text)
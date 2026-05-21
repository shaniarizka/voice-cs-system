from google import genai
from dotenv import load_dotenv
import os
import time

# =========================
# LOAD ENV
# =========================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# =========================
# GEMINI CLIENT
# =========================

client = genai.Client(
    api_key=API_KEY
)

# =========================
# FALLBACK RESPONSE
# =========================

def fallback_response(user_text):

    text = user_text.lower()

    # flight# flight
    if (
        "flight" in text
        or "fly" in text
        or "jeddah" in text
        or "jadah" in text
        or "book" in text
        or "schedule" in text
    ):

        return (
            "Baik, aku bisa bantu arrange flight "
            "ke Jeddah minggu depan."
        )

    # visa
    elif (
        "visa" in text
        or "saudi" in text
    ):

        return (
            "Untuk visa Saudi, biasanya diperlukan "
            "paspor aktif dan dokumen umrah."
        )

    # transport
    elif (
        "transport" in text
        or "madinah" in text
        or "transportasi" in text
    ):

        return (
            "Baik, aku bisa bantu carikan transport "
            "dari Jeddah ke Madinah."
        )

    # hotel
    elif (
        "hotel" in text
        or "makkah" in text
        or "haram" in text
    ):

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
    elif mode == "translate":

        prompt = f"""
    Kamu adalah assistant multilingual.

    Terjemahkan seluruh input menjadi Bahasa Inggris
    yang natural dan mudah dipahami.

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

        response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "timeout": 20
        }
    )

        return {
            "text": response.text.strip(),
            "source": "gemini"
        }

    # =========================
    # FALLBACK
    # =========================

    except Exception as e:

        print("\n[WARNING] Gemini gagal.")
        print(e)

        # tunggu sebentar jika quota/rate limit
        time.sleep(5)

        print("[INFO] Menggunakan fallback response...")

        return {
            "text": fallback_response(user_text),
            "source": "fallback"
        }
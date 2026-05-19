import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()

# Ambil API Key
API_KEY = os.getenv("GEMINI_API_KEY")

# Konfigurasi Gemini
genai.configure(api_key=API_KEY)

# Model Gemini
model = genai.GenerativeModel("gemini-2.5-flash")


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

    response = model.generate_content(prompt)

    return response.text.strip()
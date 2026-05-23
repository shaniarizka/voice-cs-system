# Voice Code-Switching Speech-to-Speech System

Sistem multilingual Speech-to-Speech end-to-end berbasis Whisper, Gemini API, dan TTS untuk memproses ujaran code-switching Bahasa Indonesia, Inggris, dan Arab.

---

# Deskripsi Proyek

Project ini dibuat untuk memenuhi tugas UAS Praktikum NLP dengan fokus pada:

* Speech-to-Text (STT)
* Code-switching speech processing
* Large Language Model (LLM)
* Text-to-Speech (TTS)
* Evaluasi pipeline multilingual speech system

Pipeline utama sistem:

```text
Speech → STT → LLM → TTS → Speech
```

Sistem mampu:

* mentranskripsi audio multilingual
* menghasilkan respon preserve code-switching
* menghasilkan respon normalize Bahasa Indonesia
* menghasilkan output suara dari respon sistem
* melakukan evaluasi WER, CER, dan latency

---

# Fitur Sistem

## 1. Speech-to-Text (STT)

Menggunakan OpenAI Whisper lokal untuk transkripsi audio multilingual.

Fitur:

* multilingual transcription
* support code-switching ID–EN–AR
* evaluasi WER & CER

---

## 2. Large Language Model (LLM)

Menggunakan Gemini API (`google-genai`).

Mode response:

### Preserve Mode

Mempertahankan pola code-switching pengguna.

Contoh:

```text
User:
Aku mau book flight ke Jeddah minggu depan.

Response:
Baik, aku bisa bantu arrange flight ke Jeddah minggu depan.
```

### Normalize Mode

Mengubah seluruh respon menjadi Bahasa Indonesia formal.

### Translate Mode (Opsional)

Menerjemahkan input menjadi Bahasa Inggris.

---

## 3. Text-to-Speech (TTS)

Menggunakan `pyttsx3` untuk menghasilkan output suara.

Output audio otomatis disimpan ke folder:

```text
outputs/
```

Contoh:

```text
outputs/2128_audio1_response.wav
```

---

# Struktur Folder

```text
voice-cs-system/
│
├── app/
│   ├── stt.py
│   ├── llm.py
│   ├── tts.py
│   ├── main.py
│   └── utils.py
│
├── data/
│   └── corpus/
│       ├── audio/
│       └── transcripts/
│
├── logs/
│   ├── evaluation_preserve.csv
│   └── evaluation_normalize.csv
│
├── outputs/
│   └── *.wav
│
├── analisis_pipeline.py
├── requirements.txt
├── README.md
└── .env
```

---

# Dataset dan Corpus

Dataset berupa audio code-switching Bahasa Indonesia, Inggris, dan Arab.

Format penamaan audio:

```text
{id}_audioXX.wav
```

Contoh:

```text
2128_audio01.wav
2305_audio18.wav
```

Ground truth disimpan dalam:

```text
data/corpus/transcripts/ground_truth.json
```

---

# Instalasi

## 1. Clone Repository

```bash
git clone <repository-url>
cd voice-cs-system
```

---

## 2. Buat Virtual Environment

### Windows

```bash
python -m venv env
env\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv env
source env/bin/activate
```

---

## 3. Install Dependency

```bash
pip install -r requirements.txt
```

Install Gemini SDK terbaru:

```bash
pip install -U google-genai
```

---

# Konfigurasi API Gemini

Buat file `.env`:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

API key diperoleh dari:

```text
https://aistudio.google.com/
```

---

# Menjalankan Pipeline

## Preserve Mode

Pada `analisis_pipeline.py`:

```python
LLM_MODE = "preserve"
```

Jalankan:

```bash
python analisis_pipeline.py
```

Hasil:

* evaluation_preserve.csv
* output response audio

---

## Normalize Mode

Ubah:

```python
LLM_MODE = "normalize"
```

Jalankan kembali:

```bash
python analisis_pipeline.py
```

Hasil:

* evaluation_normalize.csv

---

# Output Sistem

## 1. CSV Evaluation

File evaluasi:

```text
logs/evaluation_preserve.csv
logs/evaluation_normalize.csv
```

Kolom evaluasi:

* filename
* transcript
* ground_truth
* WER
* CER
* latency
* response
* llm_source

---

## 2. Output Audio

File hasil TTS:

```text
outputs/*.wav
```

---

# Evaluasi Sistem

## Metrik

### Word Error Rate (WER)

Mengukur kesalahan kata hasil transkripsi.

### Character Error Rate (CER)

Mengukur kesalahan karakter hasil transkripsi.

### Latency

Mengukur waktu proses end-to-end.

---

# Hasil Eksperimen

## Preserve Mode

Contoh hasil:

```text
Average WER      : 0.665
Average CER      : 1.965
Average Latency  : 26.44 sec
```

---

# Analisis Eksperimen

## Temuan

1. Whisper masih mengalami kesalahan pada:

* transliterasi Arab
* pelafalan campuran ID–EN–AR
* code-switching cepat

2. Gemini berhasil menghasilkan respon multilingual yang natural.

3. TTS berhasil menghasilkan audio response secara otomatis.

4. Latency cukup tinggi karena:

* pemrosesan Whisper CPU
* request Gemini API
* proses TTS sequential

---

# Kendala Sistem

## STT

* Kesalahan transkripsi bahasa Arab
* Mixed-language recognition belum stabil

## LLM

* Rate limit Gemini API
* 503 high demand
* fallback response diperlukan

## TTS

* pyttsx3 belum optimal untuk multilingual Arabic pronunciation

---

# Pengembangan Selanjutnya

* Integrasi Coqui TTS multilingual
* Segmentasi bahasa otomatis
* Language tagging
* Gradio interface
* FastAPI deployment
* Whisper large-v3-turbo

---

# Teknologi yang Digunakan

| Komponen | Teknologi      |
| -------- | -------------- |
| STT      | OpenAI Whisper |
| LLM      | Gemini API     |
| TTS      | pyttsx3        |
| Evaluasi | jiwer          |
| Backend  | Python         |

---

# Cara Push ke GitHub

```bash
git add .
git commit -m "Final NLP project update"
git push origin main
```

---

# Author

Praktikum NLP — Code-Switching Speech-to-Speech System

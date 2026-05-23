# Voice Code-Switching Speech-to-Speech System

Sistem multilingual Speech-to-Speech end-to-end berbasis Whisper, Gemini API, dan TTS untuk memproses ujaran code-switching Bahasa Indonesia, Inggris, dan Arab.


# Deskripsi Proyek

Project ini dibuat untuk memenuhi tugas UAS Praktikum NLP dengan fokus pada:

* Speech-to-Text (STT)
* Code-switching speech processing
* Large Language Model (LLM)
* Text-to-Speech (TTS)
* Evaluasi pipeline multilingual speech system

Pipeline utama sistem:

Speech → STT → LLM → TTS → Speech


# Sistem mampu:

* mentranskripsi audio multilingual
* menghasilkan respon preserve code-switching
* menghasilkan respon normalize Bahasa Indonesia
* menghasilkan output suara dari respon sistem
* melakukan evaluasi WER, CER, dan latency


# Fitur Sistem

* Multilingual Speech-to-Text
* Code-switching response
* Preserve & Normalize mode
* Speech response generation
* Evaluasi WER, CER, dan latency
* Demo interface menggunakan Gradio

# Teknologi
* Python
* OpenAI Whisper
* Google Gemini API
* pyttsx3 TTS
* Gradio

# Struktur Folder
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

# Menjalankan Projek

##  Pipeline evaluation

python analisis_pipeline.py

## Gradio Demo

python gradio_app/app.py


# Output Sistem

* Transcript hasil STT
* Response dari LLM
* Audio response
* File evaluasi CSV
* Log hasil eksperimen


# Catatan

Sistem masih memiliki keterbatasan pada:

* transkripsi audio multilingual,
* pelafalan bahasa Arab,
* dan naturalness TTS multilingual.
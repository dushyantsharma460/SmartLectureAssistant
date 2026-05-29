# AI Lecture Assistant

AI-powered lecture search and summarization system built for the IIT Guwahati course:

## Applied Machine Learning for Signal Processing

This project converts lecture videos into searchable knowledge using:

- Speech-to-Text
- Embeddings
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Local LLMs using Ollama

---

# Features

- Convert lecture videos to audio
- Generate lecture transcripts using Whisper
- Merge subtitle chunks
- Create embeddings using `mxbai-embed-large`
- Semantic search using cosine similarity
- AI-generated lecture explanations
- AI-generated lecture summaries
- React + Tailwind frontend
- FastAPI backend
- Local LLM inference using Ollama

---

# Tech Stack

## Frontend

- React
- Tailwind CSS
- Axios
- React Markdown

## Backend

- FastAPI
- Python
- Ollama

## AI / ML

- Whisper
- mxbai-embed-large
- qwen2.5:7b-instruct
- Cosine Similarity
- RAG Pipeline

---

# Project Architecture

```text
Lecture Videos
        ↓
Audio Extraction (FFmpeg)
        ↓
Speech-to-Text (Whisper)
        ↓
Chunk Creation
        ↓
Chunk Merging
        ↓
Embedding Generation
        ↓
Vector Search
        ↓
LLM Response Generation
        ↓
React Frontend
```

---

# Project Structure

```text
project/
│
├── videos/
├── audios/
├── jsons/
├── merged_jsons/
├── summaries/
├── embeddings/
├── outputs/
│
├── scripts/
│   ├── video_to_audio.py
│   ├── transcribe.py
│   ├── merge_chunks.py
│   ├── create_embeddings.py
│   ├── summarize.py
│   └── search.py
│
├── app/
│
├── requirements.txt
└── README.md
```

---

# Workflow

## 1. Convert Videos to Audio

```bash
python scripts/video_to_audio.py
```

Extracts MP3 audio from lecture videos using FFmpeg.

---

## 2. Generate Transcripts

```bash
python scripts/transcribe.py
```

Uses OpenAI Whisper to generate lecture transcripts.

### Output

```text
jsons/*.json
```

---

## 3. Merge Chunks

```bash
python scripts/merge_chunks.py
```

Merges multiple subtitle chunks into larger semantic chunks.

### Output

```text
merged_jsons/*.json
```

---

## 4. Create Embeddings

```bash
python scripts/create_embeddings.py
```

Creates vector embeddings using:

- mxbai-embed-large

### Output

```text
embeddings/embeddings.joblib
```

---

## 5. Generate Lecture Summaries

```bash
python scripts/summarize.py
```

Creates AI-generated summaries for lectures.

### Output

```text
summaries/*.json
```

---

## 6. Search Lectures

```bash
python scripts/search.py
```

Allows semantic search over lecture transcripts using embeddings and cosine similarity.

---

# Models Used

## Whisper

Used for:

- Speech-to-text transcription

---

## mxbai-embed-large

Used for:

- Embedding generation
- Semantic similarity search

---

## qwen2.5:7b-instruct

Used for:

- AI-generated responses
- Lecture summarization

---

# Example Queries

## Lecture Search

- What is EEG?
- Explain FFT
- What is ZCR?
- How is pitch estimated?
- Difference between voiced and unvoiced sounds

---

## Lecture Summary

- ECG_EEG_and_Brain_Signals
- Pitch_Estimation_and_Stationary_Nonstationary_Signals
- ZCR_and_Autocorrelation_for_Voiced_Unvoiced_Analysis

---

# Installation

## Clone Repository

```bash
git clone 
```

---

## Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

# Requirements

## Python Packages

```text
fastapi
uvicorn
pandas
numpy
scikit-learn
joblib
requests
openai-whisper
torch
```

---

# Future Improvements

- Lecture linking
- Voice search
- PDF note generation
- Multi-course support

---

# Author

## Dushyant Sharma

BS in Data Science and AI

IIT Guwahati
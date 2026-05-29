from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

EMBEDDING_PATH = os.path.join(
    BASE_DIR,
    "../../embeddings/embeddings.joblib"
)

SUMMARY_PATH = os.path.join(
    BASE_DIR,
    "../../summaries"
)

df = joblib.load(
    EMBEDDING_PATH
)


def create_embeddings(text_list):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "mxbai-embed-large",
            "input": text_list
        }
    )

    data = r.json()

    return data["embeddings"]


def inference(prompt):

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b-instruct",
            "prompt": prompt,
            "stream": False
        }
    )

    data = r.json()

    print(data)

    return data.get(
        "response",
        "No response generated"
    )


def format_time(seconds):

    seconds = int(seconds)

    minutes = seconds // 60

    remaining_seconds = seconds % 60

    return f"{minutes:02}:{remaining_seconds:02}"


@app.get("/")
def home():

    return {
        "message": "Backend Running"
    }


@app.get("/search")
def search(query: str):

    try:

        question_embedding = create_embeddings(
            [query]
        )[0]

        similarities = cosine_similarity(
            np.vstack(df['embedding']),
            [question_embedding]
        ).flatten()

        threshold = 0.25

        top_result = 5

        max_prob = similarities.argsort()[::-1][0:top_result]

        filtered_results = [
            index for index in max_prob
            if similarities[index] > threshold
        ]

        if len(filtered_results) == 0:

            return {
                "lecture": "N/A",
                "start": "N/A",
                "end": "N/A",
                "confidence": 0,
                "answer": "Topic not found in lectures"
            }

        new_df = df.loc[filtered_results]

        prompt = f"""
You are an AI assistant for the IIT Guwahati course:
Applied Machine Learning for Signal Processing.

Lecture Chunks:
{new_df[['title','number','start','end','text']].to_json()}

User Question:
{query}

Instructions:

1. Answer ONLY from lecture chunks.

2. Give ONLY explanation.

3. Do NOT include:
- lecture name
- timestamps
- headings
- markdown titles
- chunk ids
- references
- metadata

4. Keep response concise and student friendly.

5. Use bullet points when needed.
"""

        response = inference(prompt)

        lecture = new_df.iloc[0]["title"]

        start = format_time(
            new_df.iloc[0]["start"]
        )

        end = format_time(
            new_df.iloc[0]["end"]
        )

        confidence = round(
            similarities[max_prob[0]] * 100,
            2
        )

        return {
            "lecture": lecture,
            "start": start,
            "end": end,
            "confidence": confidence,
            "answer": response
        }

    except Exception as e:

        print(e)

        return {
            "lecture": "Error",
            "start": "N/A",
            "end": "N/A",
            "confidence": 0,
            "answer": str(e)
        }


@app.get("/summary")
def get_summary(lecture: str):

    try:

        files = os.listdir(SUMMARY_PATH)

        matched_file = None

        for file in files:

            clean_name = file.replace(".json", "")

            if lecture.lower() in clean_name.lower():

                matched_file = file

                break

        if matched_file is None:

            return {
                "title": "N/A",
                "summary": "Summary not found"
            }

        summary_file = os.path.join(
            SUMMARY_PATH,
            matched_file
        )

        with open(summary_file, "r", encoding="utf-8") as f:

            data = json.load(f)

        return {
            "title": data["title"],
            "summary": data["summary"]
        }

    except Exception as e:

        print(e)

        return {
            "title": "Error",
            "summary": str(e)
        }
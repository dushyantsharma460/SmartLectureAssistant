import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import joblib
import requests

def create_embeddings(text_list):

    print("Thinking...")

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "mxbai-embed-large",
            "input": text_list
        }
    )

    return r.json()['embeddings']


def inference(prompt):

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b-instruct",
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json()


df = joblib.load(
    "embeddings/embeddings.joblib"
)

incoming_query = input("Ask a Question: ")

question_embedding = create_embeddings(
    [incoming_query]
)[0]

similarities = cosine_similarity(
    np.vstack(df['embedding']),
    [question_embedding]
).flatten()

threshold = 0.40

top_result = 5

max_prob = similarities.argsort()[::-1][0:top_result]

filtered_results = [
    index for index in max_prob
    if similarities[index] > threshold
]

if len(filtered_results) == 0:
    print("Topic not found in lectures")
    exit()

new_df = df.loc[filtered_results]

prompt = f"""
You are an AI assistant for the IIT Guwahati course:
"Applied Machine Learning for Signal Processing"
from B.S. in Data Science and AI.

Below are lecture subtitle chunks containing:
- video title
- video number
- start timestamp
- end timestamp
- spoken text

Lecture Chunks:
{new_df[["title","number","start","end","text"]].to_json()}

------------------------------------------------

User Question:
{incoming_query}

Instructions:
1. Answer ONLY from the provided lecture chunks.
2. Tell the user:
   - which video contains the topic
   - exact timestamps
   - what is explained there
3. If multiple videos discuss the topic, mention all relevant videos.
4. Keep the answer clear and student-friendly.
5. If the question is unrelated to the course, say:
   "I can only answer questions related to this course."
6. If the topic is not found in the lecture chunks, say:
   "I could not find this topic in the provided lectures."
"""

with open("outputs/prompt.txt", "w") as f:
    f.write(prompt)

response = inference(prompt)["response"]

print(response)

with open("outputs/response.txt", "w") as f:
    f.write(response)
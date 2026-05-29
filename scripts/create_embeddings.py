import requests
import os
import json
import pandas as pd
import joblib

def create_embeddings(text_list):

    r = requests.post(
        "http://localhost:11434/api/embed",
        json={
            "model": "mxbai-embed-large",
            "input": text_list
        }
    )

    embedding = r.json()['embeddings']

    return embedding


jsons = sorted(os.listdir("merged_jsons"))

my_list = []

chunk_id = 1

for json_file in jsons:

    with open(f"merged_jsons/{json_file}") as f:

        content = json.load(f)

        print(f"Creating Embeddings for {json_file}")

        embeddings = create_embeddings(
            [data["text"] for data in content]
        )

    for i, chunk in enumerate(content):

        chunk["chunk_id"] = chunk_id

        chunk_id += 1

        chunk["embedding"] = embeddings[i]

        my_list.append(chunk)


df = pd.DataFrame(my_list)

os.makedirs("embeddings", exist_ok=True)

joblib.dump(
    df,
    "embeddings/embeddings.joblib"
)

print("Embeddings Saved")
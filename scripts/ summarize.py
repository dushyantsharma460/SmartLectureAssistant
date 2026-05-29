import os
import json
import requests

os.makedirs("summaries", exist_ok=True)

def generate_summary(text):

    prompt = f"""
You are an AI assistant.

Summarize the following lecture transcript in simple student-friendly language.

Instructions:
1. Keep summary clear and concise.
2. Use bullet points.
3. Mention important topics.
4. Avoid unnecessary details.

Lecture Transcript:
{text}
"""

    r = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "qwen2.5:7b-instruct",
            "prompt": prompt,
            "stream": False
        }
    )

    return r.json()["response"]


json_files = os.listdir("jsons")

for file in json_files:

    file_path = os.path.join("jsons", file)

    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)

    lecture_text = content["text"]

    print(f"Generating summary for {file}...")

    summary = generate_summary(lecture_text)

    summary_data = {
        "title": file.replace(".json", ""),
        "summary": summary
    }

    output_path = os.path.join(
        "summaries",
        file
    )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            summary_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"{file} summary saved")
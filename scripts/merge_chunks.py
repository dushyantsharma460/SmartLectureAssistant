import os
import json

n = 5

for filename in os.listdir("jsons"):

    file_path = os.path.join("jsons", filename)

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data["chunks"]

    merged_chunks = []

    for i in range(0, len(chunks), n):

        batch = chunks[i:i+n]

        merged_text = " ".join(
            item["text"] for item in batch
        )

        merged_chunks.append({
            "number": batch[0]["number"],
            "title": batch[0]["title"],
            "start": batch[0]["start"],
            "end": batch[-1]["end"],
            "text": merged_text
        })

    os.makedirs("merged_jsons", exist_ok=True)

    output_path = os.path.join("merged_jsons", filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            merged_chunks,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(f"{filename} done")
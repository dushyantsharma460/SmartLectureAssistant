import whisper
import json
import os

model = whisper.load_model("small.en")

audio_list = os.listdir("audios")

for audio in audio_list:

    number = audio.split("_")[0]
    title = audio.split("_", 1)[1].replace(".mp3", "")

    json_name = f"0{number}_{title}.json"

    file_path = f"jsons/{json_name}"

    if os.path.exists(file_path):
        print(f"{json_name} already exists")
        continue

    result = model.transcribe(
        audio=f"audios/{audio}",
        language="en",
        fp16=False,
    )

    chunks = []

    for data in result["segments"]:

        chunks.append({
            "number": number,
            "title": title,
            "start": data["start"],
            "end": data["end"],
            "text": data["text"]
        })

    chunks_with_text = {
        "chunks": chunks,
        "text": result["text"]
    }

    with open(file_path, "w") as file:
        json.dump(chunks_with_text, file, indent=4)

    print(f"{json_name} saved")
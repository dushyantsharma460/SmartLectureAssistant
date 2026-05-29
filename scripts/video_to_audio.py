import os
import subprocess

files = os.listdir("videos")

for file in files:

    tutorial_number = file.split("Tutorial")[1].split("[")[0]
    topic_name = file.split("[")[1].split("]")[0]

    print(tutorial_number, topic_name)

    subprocess.run([
        "ffmpeg",
        "-i",
        f"videos/{file}",
        f"audios/{tutorial_number}_{topic_name}.mp3"
    ])
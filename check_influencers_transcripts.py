import os
import json

for influencer in os.listdir("./profiles"):
    with open(os.path.join("profiles", influencer), encoding="utf-8") as fp:
        data = json.load(fp)
    if not os.path.isfile(os.path.join("transcripts", f"{data[0]['id']}.vtt")):
        print(influencer.split(".")[0])

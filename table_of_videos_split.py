import pandas as pd
import os
import tqdm
import json
import csv
from collections import defaultdict

for influencer in tqdm.tqdm(os.listdir("./profiles")):
    with open(os.path.join("profiles", influencer), encoding="utf-8") as fp:
        raw_data = json.load(fp)

    data: defaultdict[str, list] = defaultdict(list)

    for video in raw_data:
        if video["authorMeta"]["region"] == "US":
            data["id"].append(video["id"])
            data["author"].append(video["authorMeta"]["name"])
            data["nation"].append(video["authorMeta"]["region"])
            data["date"].append(video["createTime"])

            data["views"].append(video["playCount"])
            data["likes"].append(video["diggCount"])
            data["comments"].append(video["commentCount"])
            data["shares"].append(video["shareCount"])

            data["url"].append(video["webVideoUrl"])
            data["text"].append(video["text"])

            if os.path.isfile(os.path.join("clean_transcripts", video["id"] + ".txt")):
                with open(
                    os.path.join("clean_transcripts", video["id"] + ".txt"),
                    encoding="utf-8",
                ) as fp:
                    data["transcript"].append(fp.read())
            else:
                data["transcript"].append(pd.NA)

            data["hashtags"].append(
                list(set(tag["name"] for tag in video["hashtags"] if tag["name"] != ""))
            )

    df = pd.DataFrame(data)

    if df.shape[0] > 0:
        df.to_csv(
            os.path.join(
                "video_data", f"{influencer.removesuffix('.json')}_videos.csv"
            ),
            index=False,
            quoting=csv.QUOTE_NONNUMERIC,
        )

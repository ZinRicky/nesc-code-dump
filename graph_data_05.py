import numpy as np
import pandas as pd
import os
import re
import json
from collections import defaultdict
from tqdm import tqdm
import csv

# Esportazione di tutte le possibili proiezioni di grafo mancanti

# Già fatte altrove:
# - Grafo con tutto
# - Grafo con solo persone

# Da fare:
# - Grafo con solo contenuti e hashtag
# - Grafo con solo contenuti
# - Grafo delle influencer

comments = pd.read_csv(
    os.path.join("polished_data", "comments_from_videos.csv"),
    dtype={
        "id": "Int64",
        "video_id": "Int64",
        "author": object,
        "date": "Int64",
        "likes": "Int64",
        "replies": "Int64",
        "reply_of": "Int64",
        "text": object,
    },
)

videos = pd.read_csv(os.path.join("polished_data", "videos_from_influencers.csv"))
videos["hashtags"] = videos["hashtags"].apply(lambda s: json.loads(s.replace("'", '"')))

hashtags = pd.read_csv(
    os.path.join("polished_data", "hashtags_from_influencers.csv"),
    names=["ht", "count"],
)

data: defaultdict[tuple, int] = defaultdict(int)

for comment in tqdm(comments.itertuples(), total=comments.shape[0]):
    ht_regex = r"#(\w+)"
    if isinstance(comment.text, str):
        comment_hashtags = re.findall(ht_regex, comment.text)
        ht_list = [x for x in comment_hashtags if x in hashtags.ht.array]
        for i, ht1 in enumerate(sorted(ht_list)):
            for ht2 in sorted(ht_list)[i + 1 :]:
                data[(ht1, ht2)] += 1

for video in tqdm(videos.itertuples(), total=videos.shape[0]):
    video_hashtags = [x for x in video.hashtags if x in hashtags.ht.array]
    video_hashtags.sort()
    for i, ht1 in enumerate(video_hashtags):
        for ht2 in video_hashtags[i + 1 :]:
            data[(ht1, ht2)] += 1

with open(
    os.path.join("polished_data", "hashtag_edges_list_undirected.csv"),
    "w",
    encoding="utf-8",
    newline="",
) as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(["Source", "Target", "Weight"])
    for x in data:
        file_writer.writerow([x[0], x[1], data[x]])

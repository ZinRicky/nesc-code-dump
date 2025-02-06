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
    # Comments and replies
    if not pd.isna(comment.reply_of):
        try:
            data[(comment.id, comment.reply_of)] += 1
        except:
            pass
    else:
        data[(comment.id, comment.video_id)] += 1

    # Data for hashtags
    ht_regex = r"#(\w+)"
    if isinstance(comment.text, str):
        ht_list = re.findall(ht_regex, comment.text)
        for ht in ht_list:
            if ht in hashtags.ht:
                data[(comment.id, f"hashtag_{ht}")] += 1

# for comment_author in tqdm(set(comments.author.array)):
#     comments_by_author = comments.loc[comments.author == comment_author]
#     for comment_by_author in comments_by_author.itertuples():
#         for other_comment in comments_by_author.loc[
#             comment_by_author.Index + 1 :
#         ].itertuples():
#             data[(comment_by_author.id, other_comment.id)] += 1
#             data[(other_comment.id, comment_by_author.id)] += 1

for video in tqdm(videos.itertuples(), total=videos.shape[0]):
    for ht in hashtags.ht:
        if ht in video.hashtags:
            data[(video.id, f"hashtag_{ht}")] += 1

for video_author in tqdm(set(videos.author.array)):
    videos_by_creator = videos.loc[videos.author == video_author]
    for video_by_creator in videos_by_creator.itertuples():
        for other_video in videos_by_creator.loc[
            video_by_creator.Index + 1 :
        ].itertuples():
            data[(video_by_creator.id, other_video.id)] += 1
            data[(other_video.id, video_by_creator.id)] += 1

with open(
    os.path.join("polished_data", "non_people_light_edges_list.csv"),
    "w",
    encoding="utf-8",
    newline="",
) as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(["Source", "Target", "Weight"])
    for x in data:
        file_writer.writerow([x[0], x[1], data[x]])

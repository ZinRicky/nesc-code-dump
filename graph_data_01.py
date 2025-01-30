import os
import csv
import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm

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
data: defaultdict[tuple, int] = defaultdict(int)

for comment in tqdm(comments.itertuples(), total=comments.shape[0]):
    if not pd.isna(comment.reply_of):
        try:
            data[
                (
                    comment.author,
                    comments[comments["id"] == comment.reply_of].author.values[0],
                )
            ] += 1
        except:
            pass
    else:
        data[
            (comment.author, videos[videos["id"] == comment.video_id].author.values[0])
        ] += 1

with open(
    os.path.join("polished_data", "comment_graph.csv"),
    "w",
    encoding="utf-8",
    newline="",
) as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(["Source", "Target", "Weight"])
    for x in data:
        file_writer.writerow([x[0], x[1], data[x]])

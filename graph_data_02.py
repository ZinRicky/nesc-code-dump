import numpy as np
import pandas as pd
import os
import re
from collections import defaultdict
from tqdm import tqdm
import csv

comments = pd.read_csv(os.path.join('polished_data', 'comments_from_videos.csv'), dtype={
                       'id': 'Int64', 'video_id': 'Int64', 'author': object, 'date': 'Int64',
                       'likes': 'Int64', 'replies': 'Int64', 'reply_of': 'Int64', 'text': object})

videos = pd.read_csv(os.path.join('polished_data', 'videos_from_influencers.csv'))

hashtags = pd.read_csv(os.path.join('polished_data', 'hashtags_from_influencers.csv'), names=['ht', 'count'])

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
    
    # Authors of the comments
    data[(comment.author, comment.id)] += 1
    data[(comment.id, comment.author)] += 1
    
    # Data for hashtags
    ht_regex = r"#(\w+)"
    if isinstance(comment.text, str):
        ht_list = re.findall(ht_regex, comment.text)
        for ht in ht_list:
            data[(comment.id, f'hashtag_{ht}')] += 1

for video in tqdm(videos.itertuples(), total=videos.shape[0]):
    for ht in hashtags.ht:
        if videos.loc[video.Index, f'hashtag_{ht}']:
            data[(video.id, f'hashtag_{ht}')] += 1
    
    data[(video.id, video.author)] += 1
    data[(video.author, video.id)] += 1
    


with open(os.path.join('polished_data', 'complete_graph.csv'), 'w', encoding='utf-8', newline='') as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(["Source", "Target", "Weight"])
    for x in data:
        file_writer.writerow([x[0], x[1], data[x]])
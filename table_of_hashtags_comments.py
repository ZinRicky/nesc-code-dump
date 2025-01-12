import os
import json
from tqdm import tqdm
import pandas as pd
import csv
import re
from collections import defaultdict

comments = pd.read_csv(os.path.join('polished_data', 'comments_from_videos.csv'), dtype={
                       'id': 'Int64', 'video_id': 'Int64', 'author': object, 'date': 'Int64',
                       'likes': 'Int64', 'replies': 'Int64', 'reply_of': 'Int64', 'text': object})
hashtags: defaultdict[str, int] = defaultdict(int)

for comment in tqdm(comments.itertuples(), total=comments.shape[0]):
    ht_regex = r"#(\w+)"
    if isinstance(comment.text, str):
        ht_list = re.findall(ht_regex, comment.text)
        for ht in ht_list:
            hashtags[ht] += 1

with open(os.path.join('polished_data', 'hashtags_from_comments.csv'), 'w', encoding='utf-8', newline='') as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for hashtag in hashtags:
        if hashtag:
            file_writer.writerow([hashtag, hashtags[hashtag]])

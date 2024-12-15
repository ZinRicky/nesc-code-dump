import os
import json
import tqdm
import csv
from collections import defaultdict

hashtags: defaultdict[str, int] = defaultdict(int)

for influencer in tqdm.tqdm(os.listdir('./profiles')):
    with open(os.path.join('profiles', influencer), encoding='utf-8') as fp:
        raw_data = json.load(fp)
    for video in raw_data:
        if 'hashtags' in video:
            for hashtag in video['hashtags']:
                hashtags[hashtag['name']] += 1

with open(os.path.join('polished_data', 'hashtags_from_influencers.csv'), 'w', encoding='utf-8', newline='') as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    for hashtag in hashtags:
        if hashtag:
            file_writer.writerow([hashtag, hashtags[hashtag]])

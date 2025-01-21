import pandas as pd
import os
import json
import tqdm
import csv
from collections import defaultdict

hashtags: defaultdict[str, int] = defaultdict(int)

videos = pd.read_csv(os.path.join(
    'polished_data', 'videos_from_influencers.csv'))

for video_hts in tqdm.tqdm(videos['hashtags'].apply(lambda s: json.loads(s.replace("'", '"'))), total=videos.shape[0]):
    for ht in video_hts:
        hashtags[ht] += 1

with open(os.path.join('polished_data', 'hashtags_from_influencers.csv'), 'w', encoding='utf-8', newline='') as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(['Hashtag', 'Count'])
    for hashtag in hashtags:
        if hashtag and hashtags[hashtag] >= 10:
            file_writer.writerow([hashtag, hashtags[hashtag]])

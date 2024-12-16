import pandas as pd
import os
import tqdm
import json
import csv
from collections import defaultdict

df: None | pd.DataFrame = None
hashtags: list[str] = []

with open(os.path.join('polished_data', 'hashtags_from_influencers.csv'), encoding='utf-8', newline='') as fp:
    hashtag_file = csv.reader(fp)
    for hashtag in hashtag_file:
        hashtags.append(hashtag[0])

for influencer in tqdm.tqdm(os.listdir('./profiles')):
    with open(os.path.join('profiles', influencer), encoding='utf-8') as fp:
        raw_data = json.load(fp)
    data: defaultdict[str, list] = defaultdict(list)
    for video in raw_data:
        data['id'].append(video['id'])
        data['author'].append(video['authorMeta']['name'])
        data['nation'].append(video['authorMeta']['region'])
        data['date'].append(video['createTime'])

        data['views'].append(video['playCount'])
        data['likes'].append(video['diggCount'])

        data['url'].append(video['webVideoUrl'])
        data['text'].append(video['text'])

        if os.path.isfile(os.path.join('clean_transcripts', video['id'] + '.txt')):
            with open(os.path.join('clean_transcripts', video['id'] + '.txt'), encoding='utf-8') as fp:
                data['transcript'].append(fp.read())
        else:
            data['transcript'].append(pd.NA)

        video_hashtags = {tag['name'] for tag in video['hashtags']}
        for ht in hashtags:
            data[f'hashtag_{ht}'].append(ht in video_hashtags)

    if df is None:
        df = pd.DataFrame(data)
    else:
        df = pd.concat([df, pd.DataFrame(data)])

if df is not None:
    df.to_csv(os.path.join('polished_data', 'videos_from_influencers.csv'),
              index=False, quoting=csv.QUOTE_NONNUMERIC)

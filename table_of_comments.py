import pandas as pd
import os
import json
import csv
from collections import defaultdict
from tqdm import tqdm

df: None | pd.DataFrame = None
videos = pd.read_csv(os.path.join('polished_data', 'videos_from_influencers.csv'))
relevant_videos = videos.loc[videos['nation'] == 'US'].id

for video in tqdm(relevant_videos, total=relevant_videos.shape[0]):
    if f'{video}.json' in os.listdir('comments'):
        with open(os.path.join('comments', f'{video}.json'), encoding='utf-8') as fp:
            raw_data = json.load(fp)
        data: defaultdict[str, list] = defaultdict(list)
        for comment in raw_data:
            if 'cid' in comment and 'uniqueId' in comment and 'createTime' in comment:
                data['id'].append(comment['cid'])
                data['video_id'].append(video)
                data['author'].append(comment['uniqueId'])
                data['date'].append(comment['createTime'])
                data['likes'].append(comment['diggCount'])
                data['replies'].append(int(comment['replyCommentTotal']) if comment['replyCommentTotal'] else 0)
                data['reply_of'].append(comment['repliesToId'])
                data['text'].append(comment['text'])
                
        if df is None:
            df = pd.DataFrame(data)
        else:
            df = pd.concat([df, pd.DataFrame(data)])

if df is not None:
    df.to_csv(os.path.join('polished_data', 'comments_from_videos.csv'),
              index=False, quoting=csv.QUOTE_NONNUMERIC)
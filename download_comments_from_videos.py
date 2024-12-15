import os
import json
import tqdm
import pandas as pd
from ensembledata.api import EDClient

df: pd.DataFrame = pd.read_csv(os.path.join(
    'polished_data', 'videos_from_influencers.csv'))
client = EDClient(token="P4NfbDhofMhHLsDi")

for video in tqdm.tqdm(df['id']):
    if not os.path.isfile(os.path.join('comments', f'{video}.json')):
        raw_data: list[dict] = []
        counter: int = 0
        result = client.tiktok.post_comments(aweme_id=str(video))
        if result.data is not None:
            raw_data.extend(result.data['comments'])
            while 'nextCursor' in result.data:
                counter = result.data.get('nextCursor')
                result = client.tiktok.post_comments(
                    aweme_id=str(video), cursor=counter)
                if result.data is not None:
                    raw_data.extend(result.data['comments'])
        if raw_data:
            with open(os.path.join('comments', f'{video}.json'), 'w', encoding='utf-8') as fp:
                json.dump(raw_data, fp)

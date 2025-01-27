import pandas as pd
import os
# from tqdm import tqdm

df: pd.DataFrame = pd.read_csv(os.path.join('polished_data', f'videos_from_influencers.csv'))
infl = set()

for video in df.sort_values(by=['comments', 'id']).itertuples():
    if not os.path.isfile(os.path.join('comments', f'{video.id}.json')):
        infl.add(video.author)

print(infl)
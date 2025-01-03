import os
import json
from tqdm import tqdm
import pandas as pd
from apify_client import ApifyClient

if not os.path.isdir('./comments'):
    os.mkdir('./comments')

i = 4  # TO BE CHANGED IF NEEDED
df: pd.DataFrame = pd.read_csv(os.path.join('polished_data', f'scrape{i}.csv'))
client = ApifyClient("apify_api_wfoGylt0b3QlsPIixwpQmaWgOhvFlk0Ad957")

for video in tqdm(df.sort_values('comments').itertuples(), total=df.shape[0]):
    if not os.path.isfile(os.path.join('comments', f'{video.id}.json')):
        run_input = {
            'postURLs': [video.url],
            'commentsPerPost': 5000,
            'maxRepliesPerComment': 1000
        }
        run = client.actor(
            "clockworks/tiktok-comments-scraper").call(run_input=run_input)
        with open(os.path.join('comments', f'{video.id}.json'), 'wb') as out_file:
            out_file.write(client.dataset(
                run["defaultDatasetId"]).get_items_as_bytes(item_format='json'))

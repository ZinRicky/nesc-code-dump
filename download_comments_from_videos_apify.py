import os
import json
import tqdm
import pandas as pd
from apify_client import ApifyClient

if not os.path.isdir('./comments'):
    os.mkdir('./comments')

i = 1 # TO BE CHANGED IF NEEDED
df: pd.DataFrame = pd.read_csv(f'scrape{i}.csv')

client = ApifyClient("apify_api_eGtf6QOosLv0J87H2PX9sZaEXjpz6f4tyDqJ")

for video, url in tqdm.tqdm(zip(df['id'], df['url'])):
    if not os.path.isfile(os.path.join('comments', f'{video}.json')):
        run_input = {
            'postURLs': [url],
            'commentsPerPost': 5000,
        }
        run = client.actor(
            "clockworks/tiktok-comments-scraper").call(run_input=run_input)
        with open(os.path.join('comments', f'{video}.json'), 'wb') as out_file:
            out_file.write(client.dataset(
                run["defaultDatasetId"]).get_items_as_bytes(item_format='json'))

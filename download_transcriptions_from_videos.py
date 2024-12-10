import os
import subprocess
import json
import time
import random
import tqdm

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0'

for influencer in os.listdir('profiles'):
    with open(os.path.join('profiles', influencer), encoding='utf-8') as fp:
        data = json.load(fp)
    for video in tqdm.tqdm(data):
        if not os.path.exists(os.path.join('transcripts', f'{video['id']}.vtt')) and 'subtitleLinks' in video['videoMeta']:
            link = video['videoMeta']['subtitleLinks'][0]['downloadLink']
            temporary_file = os.path.join('transcripts', f'{video['id']}.vtt')
            subprocess.run(['curl', '-o', temporary_file, '-A', user_agent, '-s', link])
            time.sleep(random.random())

import pandas as pd
import json

videos = pd.read_csv('polished_data/videos_from_influencers.csv',
                     dtype={'id': 'Int64', 'author': object, 'nation': object,
                     'date': 'Int64', 'views': 'Int64', 'likes': 'Int64', 'comments': 'Int64',
                     'shares': 'Int64', 'url': object, 'text': object, 'transcript': object, 'hashtags': object})

videos.hashtags.apply(lambda s: json.loads(s.replace("'", '"')))

print(videos.head(30))

# print(videos.columns)

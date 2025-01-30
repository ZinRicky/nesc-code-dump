import os
import json
from tqdm import tqdm
import pandas as pd
from apify_client import ApifyClient

if not os.path.isdir("./comments"):
    os.mkdir("./comments")

# i: int | None = None  # TO BE CHANGED IF NEEDED

# if i is None:
#     df: pd.DataFrame = pd.read_csv(
#         os.path.join("polished_data", f"videos_from_influencers.csv")
#     )
# else:
#     df = pd.read_csv(os.path.join("polished_data", f"scrape{i}.csv"))
client = ApifyClient("apify_api_JhCnQZfvI9rIeSa2falOvsitd8Rz2F3sgiHw")

for video in tqdm(
    [
        {
            "url": "https://www.tiktok.com/@lexitay_/video/7440289962857188639",
            "id": 7440289962857188639,
        }
    ]
):
    if not os.path.isfile(os.path.join("comments", f"{video['id']}.json")):
        run_input = {
            "postURLs": [video["url"]],
            "commentsPerPost": 5000,
            "maxRepliesPerComment": 1000,
        }
        run = client.actor("clockworks/tiktok-comments-scraper").call(
            run_input=run_input
        )
        if run is not None:
            with open(
                os.path.join("comments", f"{video['id']}.json"), "wb"
            ) as out_file:
                out_file.write(
                    client.dataset(run["defaultDatasetId"]).get_items_as_bytes(
                        item_format="json"
                    )
                )

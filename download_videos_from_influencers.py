from apify_client import ApifyClient
import os

client = ApifyClient("apify_api_cfEs0ENaG5BQvfUfTQX59eFl6EY2vr1BsgiL")

profiles = ["emergingmotherhood"]

for influencer in profiles:
    if f"{influencer}.json" not in os.listdir("./profiles"):
        run_input = {
            "profiles": [influencer],
            "oldestPostDate": "2024-01-01",
            "newestPostDate": "2025-01-01",
            "resultsPerPage": 700,
        }

        run = client.actor("clockworks/tiktok-profile-scraper").call(
            run_input=run_input
        )

        with open(os.path.join("profiles", f"{influencer}.json"), "wb") as out_file:
            out_file.write(
                client.dataset(run["defaultDatasetId"]).get_items_as_bytes(
                    item_format="json"
                )
            )

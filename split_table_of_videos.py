import pandas as pd
import os
import csv

full_data: pd.DataFrame = pd.read_csv(
    os.path.join("polished_data", "videos_from_influencers.csv")
)

for i in range(7):
    full_data.loc[i::7].to_csv(
        os.path.join(
            "polished_data",
            f"scrape{i+1}.csv",
        ),
        index=False,
        quoting=csv.QUOTE_NONNUMERIC,
    )

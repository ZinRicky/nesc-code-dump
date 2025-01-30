import os
import csv

with open(
    os.path.join("polished_data", "influencers.csv"), "w", encoding="utf-8", newline=""
) as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(["Name"])
    for influencer in os.listdir("profiles"):
        file_writer.writerow([influencer.removesuffix(".json")])

import scipy.sparse as spsp
import os
import pandas as pd
import csv
from tqdm import tqdm
from collections import defaultdict

# original_adjacency_matrix = spsp.load_npz(os.path.join(
#     'polished_data', 'comment_adjacency_matrix.npz'))
edges = pd.read_csv(os.path.join("polished_data", "comment_graph.csv"))
influencers = set(pd.read_csv(os.path.join("polished_data", "influencers.csv")).Name)

data: defaultdict[tuple[str, str], int] = defaultdict(int)

df = edges.loc[edges.Target.apply(lambda x: x in influencers)]

for source in tqdm(set(df.Source), total=df.shape[0]):
    dv = df.loc[edges.Source == source]
    if dv.shape[0] >= 2:
        dv_inf = dv.Target
        for inf1 in dv_inf:
            for inf2 in dv_inf:
                if inf1 != inf2:
                    data[(inf1, inf2)] += 1

final_data = []
influencers_L = list(influencers)

for i, x in tqdm(enumerate(influencers_L), total=len(influencers_L)):
    for y in influencers_L[i:]:
        if data[(x, y)]:
            final_data.append((x, y, data[(x, y)]))

with open(
    os.path.join("polished_data", "raw_influencer_graph.csv"),
    "w",
    encoding="utf-8",
    newline="",
) as fp:
    file_writer = csv.writer(fp, quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    file_writer.writerow(["Source", "Target", "Weight"])
    for x in tqdm(final_data):
        file_writer.writerow([x[0], x[1], x[2]])

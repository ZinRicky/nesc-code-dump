import numpy as np
import pandas as pd
from tqdm import tqdm
import os
import csv
from collections import defaultdict

df = pd.read_csv("polished_data/complete_graph.csv")
node_degrees: defaultdict[str, int] = defaultdict(int)

with open(os.path.join("polished_data", "full_nodes.txt"), encoding="utf-8") as fp:
    names = []
    for name in fp.readlines():
        names.append(name.replace("\n", ""))


with open(os.path.join("polished_data", "nodes.txt"), encoding="utf-8") as fp:
    people_names_list = []
    for name in fp.readlines():
        people_names_list.append(name.replace("\n", ""))
people_names = set(people_names_list)


def default_list():
    return [0, 0, 0]


degrees: defaultdict[str, list] = defaultdict(default_list)

for edge in tqdm(df.itertuples(), total=df.shape[0]):
    degrees[edge.Source][1] += 1
    degrees[edge.Target][0] += 1
    if (
        edge.Source in people_names
        or edge.Target in people_names
        or "hashtag_" in edge.Source
        or "hashtag_" in edge.Target
    ):
        degrees[edge.Source][2] += 0.5
        degrees[edge.Target][2] += 0.5
    else:
        degrees[edge.Source][2] += 1
        degrees[edge.Target][2] += 1

pd.DataFrame(
    {
        "Name": names,
        "Undirected degree": [int(degrees[name][2]) for name in names],
        "In-degree": [degrees[name][0] for name in names],
        "Out-degree": [degrees[name][1] for name in names],
    }
).sort_values(by="Undirected degree", ascending=False).to_csv(
    os.path.join("polished_data", "full_degrees.csv"),
    index=False,
    quoting=csv.QUOTE_MINIMAL,
)

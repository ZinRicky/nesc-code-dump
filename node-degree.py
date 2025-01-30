import pandas as pd
import os
from collections import defaultdict
from tqdm import tqdm
import csv

edges = pd.read_csv(
    os.path.join("polished_data", "comment_graph.csv"), encoding="utf-8"
)
# Degree = namedtuple('Degree', ['undirected', 'in', 'out'])

with open(os.path.join("polished_data", "nodes.txt"), encoding="utf-8") as fp:
    names = []
    for name in fp.readlines():
        names.append(name.replace("\n", ""))


def default_list():
    return [0, 0, 0]


degrees: defaultdict[str, list] = defaultdict(default_list)

for edge in tqdm(edges.itertuples(), total=edges.shape[0]):
    degrees[edge.Source][0] += 1
    degrees[edge.Source][2] += 1
    degrees[edge.Target][0] += 1
    degrees[edge.Target][1] += 1

pd.DataFrame(
    {
        "Name": names,
        "Undirected degree": [degrees[name][0] for name in names],
        "In-degree": [degrees[name][1] for name in names],
        "Out-degree": [degrees[name][2] for name in names],
    }
).to_csv(
    os.path.join("polished_data", "degrees.csv"),
    index=False,
    quoting=csv.QUOTE_NONNUMERIC,
)

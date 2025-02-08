import numpy as np
import pandas as pd
import igraph as ig
import csv

raw_edges = pd.read_csv("polished_data/influencer_edges_list_undirected.csv")
names = pd.read_csv("polished_data/influencers.csv")
node_name_position = {x.Name: x.Index for x in names.itertuples()}
inverse_node_name_position = {x.Index: x.Name for x in names.itertuples()}

edges = pd.DataFrame(
    {
        "Source": raw_edges.Source.apply(lambda s: node_name_position[s]).to_numpy(),
        "Target": raw_edges.Target.apply(lambda s: node_name_position[s]).to_numpy(),
        "weight": raw_edges.Weight,
    },
)

g = ig.Graph.DataFrame(edges, directed=False)
g.vs["original_index"] = list(range(len(g.vs)))

pr = g.pagerank(weights="weight")
cl = g.closeness(weights="weight")
bt = g.betweenness(weights="weight")

pd.DataFrame(
    {
        "id": [inverse_node_name_position[i] for i in g.vs["original_index"]],
        "PageRank": pr,
        "Closeness centrality": cl,
        "Betweenness centrality": bt,
    }
).sort_values(by=["Closeness centrality"], ascending=False).to_csv(
    "polished_data/influencers_measures.csv", index=False, quoting=csv.QUOTE_NONNUMERIC
)

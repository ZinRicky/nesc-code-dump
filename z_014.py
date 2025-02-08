import numpy as np
import pandas as pd
import igraph as ig
import matplotlib.pyplot as plt
import csv

raw_edges = pd.read_csv("polished_data/people_edges_list.csv")
node_names = pd.read_csv("polished_data/people_nodes.csv")["Name"].tolist()
node_name_position = {x: i for i, x in enumerate(node_names)}
inverse_node_name_position = {i: x for i, x in enumerate(node_names)}

edges = pd.DataFrame(
    {
        "Source": raw_edges.Source.apply(lambda s: node_name_position[s]).to_numpy(),
        "Target": raw_edges.Target.apply(lambda s: node_name_position[s]).to_numpy(),
        "weight": raw_edges.Weight,
    },
)

g = ig.Graph.DataFrame(edges)
g.vs["original_index"] = list(range(len(g.vs)))
g.delete_vertices([v.index for v in g.vs if g.degree(v, mode="in") <= 3])
g = g.subgraph(max(g.connected_components(mode="weak"), key=len))
# print(f"{edges.shape[0]==g.ecount()=}")

pd.DataFrame(
    {
        "id": [inverse_node_name_position[i] for i in g.vs["original_index"]],
        "Harmonic centrality": g.harmonic_centrality(weights="weight"),
        "Betweenness centrality": g.betweenness(weights="weight"),
    }
).sort_values(by=["Harmonic centrality"], ascending=False).to_csv(
    "polished_data/people_light_centralities.csv",
    index=False,
    quoting=csv.QUOTE_NONNUMERIC,
)

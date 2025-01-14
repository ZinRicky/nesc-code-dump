import os
import csv
import pandas as pd
import numpy as np
from collections import defaultdict
from tqdm import tqdm
from multiprocessing import Pool


def not_npc(x: str, table, influencers):
    return x, False if set(table.loc[table.Source == x, 'Target']) <= influencers and table.loc[table.Target == x].empty else True


edges = pd.read_csv(os.path.join('polished_data', 'comment_graph.csv'))
influencers = set(pd.read_csv(os.path.join(
    'polished_data', 'influencers.csv')).Name)

def f(x):
    return not_npc(x, edges, influencers)


def main():
    source_nodes: set = set()

    print("Indexing source nodes.")
    for x in tqdm(edges.Source):
        source_nodes.add(x)

    print("Removing NPCs.")

    with Pool() as p:
        relevant = p.imap_unordered(f, list(source_nodes))

        good_source_nodes: set = set()

        for x in tqdm(relevant, total=len(source_nodes)):
            if x[1]:
                good_source_nodes.add(x[0])

    edges.loc[edges.Source.apply(lambda x: x in good_source_nodes)].to_csv(
        os.path.join('polished_data', 'clean_comment_graph.csv'), index=False)


if __name__ == '__main__':
    main()

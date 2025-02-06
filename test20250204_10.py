import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

page_rank = pd.read_csv("polished_data/full_page_rank.csv")
influencers = pd.read_csv("polished_data/influencers.csv")

df = influencers.merge(page_rank, left_on="Name", right_on="id")

print(df.head())

fig1, ax = plt.subplots()
ax.loglog(df.Followers, df.PageRank, "o", color="#5e82b6")
ax.set_xlabel("# followers")
ax.set_ylabel("PageRank score")
plt.show()

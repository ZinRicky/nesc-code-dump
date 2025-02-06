import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("polished_data/full_page_rank.csv")

fig1, ax = plt.subplots()
ax.loglog(range(1, df.shape[0] + 1), df.PageRank, color="#5e82b6")
ax.set_xlabel("Rank position")
ax.set_ylabel("PageRank score")
plt.show()

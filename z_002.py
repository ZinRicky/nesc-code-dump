import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

page_rank = pd.read_csv("polished_data/full_hub_page_rank.csv")
influencers = pd.read_csv("polished_data/influencers.csv")

df = influencers.merge(page_rank, left_on="Name", right_on="id")

lin_reg = linregress(np.log(df.Followers), np.log(df.PageRank))

fig1, ax = plt.subplots()
(f2,) = ax.loglog(
    [df.Followers.min(), df.Followers.max()],
    np.exp(lin_reg.intercept)
    * np.array([df.Followers.min(), df.Followers.max()]) ** lin_reg.slope,
    label=f"Regression (r={lin_reg.rvalue:.3f})",
    color="#101010",
    ls="--",
)
(f1,) = ax.loglog(
    df.Followers, df.PageRank, "o", color="#5e82b6", label="Influencer data"
)
ax.set_xlabel("# followers")
ax.set_ylabel("PageRank score")
ax.set_title("Followers vs Hub PageRank — full graph")
ax.legend(handles=[f1, f2])
plt.show()

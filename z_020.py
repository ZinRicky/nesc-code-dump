import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

page_rank = pd.read_csv("polished_data/hashtags_page_rank.csv")
hashtags = pd.read_csv("polished_data/hashtags_from_influencers.csv")

df = hashtags.merge(page_rank, left_on="Hashtag", right_on="id")


lin_reg = linregress(np.log(df.Count), np.log(df.PageRank))

fig1, ax = plt.subplots()
(f2,) = ax.loglog(
    [df.Count.min(), df.Count.max()],
    np.exp(lin_reg.intercept)
    * np.array([df.Count.min(), df.Count.max()]) ** lin_reg.slope,
    label=f"Regression (r={lin_reg.rvalue:.3f})",
    color="#101010",
    ls="--",
)
(f1,) = ax.loglog(df.Count, df.PageRank, "o", color="#5e82b6", label="Data")
ax.set_xlabel("Uses")
ax.set_ylabel("PageRank score")
ax.set_title("Uses vs PageRank — hashtags graph")
ax.legend(handles=[f1, f2])
plt.show()

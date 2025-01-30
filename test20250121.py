import matplotlib.pyplot as plt
import pandas as pd
import os

hashtags = pd.read_csv(os.path.join("polished_data", "hashtags_from_influencers.csv"))

# print(hashtags.Count.head())
# quit()

plt.loglog(
    list(range(1, hashtags.shape[0] + 1)), hashtags.Count.sort_values(ascending=False)
)
plt.xlabel("Frequency rank")
plt.ylabel("Frequency")
plt.title("Frequency of hashtags, Zipf style")
plt.show()

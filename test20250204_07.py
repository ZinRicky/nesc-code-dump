import numpy as np
import pandas as pd
from tqdm import tqdm

df = pd.read_csv("polished_data/full_degrees.csv")

print(df["Out-degree"].mean())
print(np.quantile(df["Out-degree"], [0, 0.25, 0.5, 0.75, 1]))

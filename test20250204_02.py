import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import csv

degrees = pd.read_csv(os.path.join("polished_data", "degrees.csv"))

x, counts = np.unique(degrees["Undirected degree"].to_numpy(), return_counts=True)

frequencies = counts / degrees.shape[0]
kmin = 5
gamma = 1 + 1 / np.mean(
    np.log(
        degrees.loc[
            (degrees["Undirected degree"] >= kmin),
            "Undirected degree",
        ].to_numpy()
        / kmin
    )
)

# C = gamma - 1 * kmin ** (1 - gamma)
C = gamma - 1
# C = 1

print(f"{gamma=}")
print(f"{C=}")

fig1, ax = plt.subplots()
ax.loglog(x, frequencies, "o", color="#5e82b6")
ax.loglog(
    range(1, 201), [C * k ** (-gamma) for k in range(1, 201)], "--", color="#1e1e1e"
)
ax.text(15, 0.005, "$\\gamma \\approx {:.3f}$".format(gamma))
ax.legend(["Data", r"$C k^{-\gamma}$"])
ax.set_xlabel(r"$k_{\text{out}}$")
ax.set_ylabel(r"$p_{k_{\text{out}}}$")
ax.set_ylim(bottom=2e-6, top=1)
plt.show()

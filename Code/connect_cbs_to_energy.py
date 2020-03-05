# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:06:02 2020.

@author: laura
"""

import os
import pandas as pd
import numpy as np
from functions_cbs import ConnectDistances as CD


# def main():
#     """Execute file."""
# SETTINGS
os.chdir("..")
DATA_PATH = os.path.join(os.getcwd(), "Results/Distances")
pd.options.mode.chained_assignment = None

compare = CD(DATA_PATH)
compare.findPostcodePairs()
common_pairs = compare.findCommonPairs("smallest_50_distances_gas_median.csv",
                                       "smallest_50_distances_gas_mean.csv")
# files = os.listdir(DATA_PATH)
# data = {}
# for i in files:
#     data[i] = pd.read_csv(os.path.join(DATA_PATH, i))

# postcode_pairs = {}
# for i in data:
#     df = data[i]
#     df["Combined"] = tuple(zip(df["GroupA"], df["GroupB"], df["Group"]))
#     postcode_pairs[i] = df["Combined"]

# # for a specific combinations of tables, find all common pairs
# common_pairs = []
# demographics = postcode_pairs["age_smallest_50_distances.csv"]
# energy = postcode_pairs["smallest_50_distances_elec_mean.csv"]
# for i in demographics:
#     for j in energy:
#         if CD.compareObjects(i, j):
#             common_pairs.append(i)

# if __name__ == "__main__":
#     main()



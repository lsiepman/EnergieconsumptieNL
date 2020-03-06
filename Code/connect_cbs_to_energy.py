# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 16:06:02 2020.

@author: laura
"""

import os
import pandas as pd
from functions_cbs import ConnectDistances as CD

# pylint: disable=C0103

def main():
    """Execute file."""
    # SETTINGS
    os.chdir("..")
    DATA_PATH = os.path.join(os.getcwd(), "Results/Distances")
    pd.options.mode.chained_assignment = None

    compare = CD(DATA_PATH)
    compare.findPostcodePairs()

    energy_files = ["smallest_50_distances_elec_mean.csv",
                    "smallest_50_distances_elec_median.csv",
                    "smallest_50_distances_energy_mean.csv",
                    "smallest_50_distances_energy_median.csv",
                    "smallest_50_distances_gas_mean.csv",
                    "smallest_50_distances_gas_median.csv"]
    demographics_files = ["age_smallest_50_distances.csv",
                          "household_composition_smallest_50_distances.csv",
                          "immigration_smallest_50_distances.csv",
                          "position_household_smallest_50_distances.csv"]

    common_pairs = compare.collectCommonPairs(energy_files,
                                              demographics_files)

    count = 0
    for i in common_pairs:
        if len(common_pairs[i]) > 0:
            print(i)
            print(common_pairs[i])
            count += 1
    if count == 0:
        print("No common pairs found in the data")


if __name__ == "__main__":
    main()

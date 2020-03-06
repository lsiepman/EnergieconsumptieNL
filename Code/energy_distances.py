# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 10:25:42 2020.

@author: laura
"""

import os
import pandas as pd
from functions_general import GeneralFunctions as GF
from functions_cbs import CalculateEnergyCBS as CEC

# pylint: disable=C0103

def main():
    """Execute file."""
    # SETTINGS
    os.chdir("..")
    DATA_PATH = os.path.join(os.getcwd(), "Data")
    RESULTS_PATH = os.path.join(os.getcwd(), "Results/Distances")
    pd.set_option("max_columns", 25)
    pd.options.mode.chained_assignment = None

    # DATA
    energy = pd.read_csv(os.path.join(DATA_PATH, "data_energy_geo.csv"))

    # DATA PREP
    en_cols_to_drop = ["net_manager", "purchase_area", "street",
                       "zipcode_from", "zipcode_to", "city", "type_conn_perc",
                       "type_of_connection", "LON", "LAT"]

    energy.drop(en_cols_to_drop, axis=1, inplace=True)
    energy = GF.correctForConnection(energy)

    gas_mean, gas_median = CEC.groupEnergy(energy, "gas")
    elec_mean, elec_median = CEC.groupEnergy(energy, "electricity")
    del energy

    energy_mean = gas_mean.merge(elec_mean, left_index=True, right_index=True,
                                 suffixes=("_GAS", "_ELEC"))
    energy_median = gas_median.merge(elec_median, left_index=True,
                                     right_index=True,
                                     suffixes=("_GAS", "_ELEC"))

    gas_mean.reset_index(level="year", inplace=True)
    gas_median.reset_index(level="year", inplace=True)
    elec_median.reset_index(level="year", inplace=True)
    elec_mean.reset_index(level="year", inplace=True)
    energy_mean.reset_index(level="year", inplace=True)
    energy_median.reset_index(level="year", inplace=True)

    # CALC DISTANCES
    gas_mean_cec = CEC(gas_mean, "year", "energy",
                       ["annual_consume_corrected"])
    gas_mean_dist = gas_mean_cec.findNSmallestDistances(50)

    gas_median_cec = CEC(gas_median, "year", "energy",
                         ["annual_consume_corrected"])
    gas_median_dist = gas_median_cec.findNSmallestDistances(50)

    elec_mean_cec = CEC(elec_mean, "year", "energy",
                        ["annual_consume_corrected"])
    elec_mean_dist = elec_mean_cec.findNSmallestDistances(50)

    elec_median_cec = CEC(elec_median, "year", "energy",
                          ["annual_consume_corrected"])
    elec_median_dist = elec_median_cec.findNSmallestDistances(50)

    energy_mean_cec = CEC(energy_mean, "year", "energy",
                          ["annual_consume_corrected_GAS",
                           "annual_consume_corrected_ELEC"])
    energy_mean_dist = energy_mean_cec.findNSmallestDistances(50)

    energy_median_cec = CEC(energy_median, "year", "energy",
                            ["annual_consume_corrected_GAS",
                             "annual_consume_corrected_ELEC"])
    energy_median_dist = energy_median_cec.findNSmallestDistances(50)

    # EXPORT RESULTS
    gas_mean_file = os.path.join(RESULTS_PATH,
                                 "smallest_50_distances_gas_mean.csv")
    gas_mean_dist.to_csv(gas_mean_file, index=False)

    gas_median_file = os.path.join(RESULTS_PATH,
                                   "smallest_50_distances_gas_median.csv")
    gas_median_dist.to_csv(gas_median_file, index=False)

    elec_mean_file = os.path.join(RESULTS_PATH,
                                  "smallest_50_distances_elec_mean.csv")
    elec_mean_dist.to_csv(elec_mean_file, index=False)

    elec_median_file = os.path.join(RESULTS_PATH,
                                    "smallest_50_distances_elec_median.csv")
    elec_median_dist.to_csv(elec_median_file, index=False)

    energy_mean_file = os.path.join(RESULTS_PATH,
                                    "smallest_50_distances_energy_mean.csv")
    energy_mean_dist.to_csv(energy_mean_file, index=False)

    en_median_file = os.path.join(RESULTS_PATH,
                                  "smallest_50_distances_energy_median.csv")
    energy_median_dist.to_csv(en_median_file, index=False)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 09:11:35 2020
Example map interactive

@author: laura
"""
import os
import pandas as pd
from functions_interactive_map import MapInteractive

def main():
    """Execute file"""
    # SETTINGS
    os.chdir("..")
    pd.set_option('max_columns', 25)

    DATA_PATH = os.path.join(os.getcwd(), "Data")
    RESULT_PATH = os.path.join(os.getcwd(), "Results/National_Map_Interactive")

    # DATA
    data = pd.read_csv(os.path.join(DATA_PATH, "data_energy_geo.csv"))

    # CREATING MAPS
    gas = MapInteractive(data, "gas", 2008)
    gas.plotMap(os.path.join(RESULT_PATH, "Gas NL 2008"),
                "Gas (m3) usage in 2008")

    elec = MapInteractive(data, "electricity", 2008)
    elec.plotMap(os.path.join(RESULT_PATH, "Electricity NL 2008"),
                 "Electricity (kWh) usage in 2008")

if __name__ == "__main__":
    main()

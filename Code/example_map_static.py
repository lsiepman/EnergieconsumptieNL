# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 11:57:08 2020.

@author: laura
"""

import os
import pandas as pd
import cartopy.io.shapereader as shpreader
from functions_static_map import StaticMap

# pylint: disable=C0103

def main():
    """Execute file"""
    # SETTINGS
    os.chdir("..")
    pd.set_option('max_columns', 25)

    DATA_PATH = os.path.join(os.getcwd(), "Data")
    RESULT_PATH = os.path.join(os.getcwd(), "/Results/National_Map_Static/")

    # DATA
    shape_loc = os.path.join(DATA_PATH, "gadm36_NLD_shp/gadm36_NLD_1.shp")
    shapes = list(shpreader.Reader(shape_loc).geometries())
    data = pd.read_csv(os.path.join(DATA_PATH, "data_energy_geo.csv"))

    # PLOT
    gas_2008 = StaticMap(data, 2008, "gas")
    gas_2008.plotStaticMap("Gas usage in the Netherlands (2008)",
                           "Gas usage (m3)", shapes, RESULT_PATH)


if __name__ == "__main__":
    main()

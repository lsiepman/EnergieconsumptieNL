# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 12:46:34 2020.

@author: laura
"""

import os
import pandas as pd
from functions_cbs import CleanCBS

def main():
    """Execute file."""
    # SETTINGS
    os.chdir("../Data/CBS")
    pd.set_option('max_columns', 25)

    # DATA
    lst_files = os.listdir()
    lst_files = [i for i in lst_files if i.startswith("CBS") \
                 and "METADATA" not in i]

    func = CleanCBS(lst_files)
    func.readFiles()

    # DATA CLEANING
    func.stripCols()
    func.cleanFiles()
    func.combineFiles()
    func.selectYears(2008, 2018)

    # EXPORT
    func.saveCSV()

if __name__ == "__main__":
    main()

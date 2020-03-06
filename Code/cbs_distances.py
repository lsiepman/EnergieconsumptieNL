# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 15:30:45 2020.

@author: laura
"""

import os
import pandas as pd
from functions_cbs import CalculateEnergyCBS as CEC

# pylint: disable=C0103

def main():
    """Execute file."""
    # SETTINGS
    os.chdir("..")
    CBS_PATH = os.path.join(os.getcwd(), "Data/CBS")
    RESULTS_PATH = os.path.join(os.getcwd(), "Results/Distances")

    # DATA
    age = pd.read_csv(os.path.join(CBS_PATH, "Clean_CBS - Age (2008-2018).csv"),
                      dtype={"ID": int, "Perioden": int, "Bevolking_1": float})
    imm = pd.read_csv(os.path.join(CBS_PATH,
                                   "Clean_CBS - Immigration (2008-2018).csv"),
                      dtype={"ID": int, "Perioden": int, "Bevolking_1": float})
    pos = pd.read_csv(
        os.path.join(CBS_PATH, "Clean_CBS - Position_household (2008-2018).csv"),
        dtype={"ID": int, "Perioden": int, "Bevolking_1": float})
    hou = pd.read_csv(
        os.path.join(CBS_PATH,
                     "Clean_CBS - Household_composition (2008-2018).csv"))

    # DATA PREP
    # age
    age = age.loc[age["Leeftijd"] != "Total"]
    # make age a ordinal variable:
    age_list = ['0-5', '5-10', '10-15', '15-20', '20-25', '25-30',
                '30-35', '35-40', '40-45', '45-50', '50-55', '55-60', '60-65',
                '65-70', '70-75', '75-80', '80-85', '85-90', '90-95', '95<']
    age = CEC.createOrdinalColumn(age, "Leeftijd", "Age_score", age_list)
    age.set_index("Postcode", inplace=True)

    # use class
    age_cec = CEC(age, "Perioden", "cbs")
    age_cec.pivotCBS("Postcode", ["Geslacht", "Age_score"], "Bevolking_1")
    age_cec.calcDistances()
    age_dist = age_cec.findNSmallestDistances(50)

    # immigration
    imm_cec = CEC(imm, "Perioden", "cbs")
    imm_cec.pivotCBS("Postcode", ["Geslacht", "Migratieachtergrond"],
                     "Bevolking_1")
    imm_cec.calcDistances()
    imm_dist = age_cec.findNSmallestDistances(50)

    # position household
    pos_cec = CEC(pos, "Perioden", "cbs")
    pos_cec.pivotCBS("Postcode", ["Geslacht", "PositieInHetHuishouden"],
                     "Bevolking_1")
    pos_cec.calcDistances()
    pos_dist = pos_cec.findNSmallestDistances(50)

    # Household composition
    hou_cec = CEC(hou, "Perioden", "cbs")
    hou_cec.pivotCBS("Postcode", ["Huishoudenssamenstelling"],
                     "ParticuliereHuishoudens_1")
    hou_cec.calcDistances()
    hou_dist = hou_cec.findNSmallestDistances(50)

    # Save files
    age_dist.to_csv(os.path.join(RESULTS_PATH,
                                 "age_smallest_50_distances.csv"), index=False)
    imm_dist.to_csv(os.path.join(RESULTS_PATH,
                                 "immigration_smallest_50_distances.csv"),
                    index=False)
    pos_dist.to_csv(os.path.join(
        RESULTS_PATH, "position_household_smallest_50_distances.csv"),
                    index=False)
    hou_dist.to_csv(os.path.join(
        RESULTS_PATH, "household_composition_smallest_50_distances.csv"),
                    index=False)

if __name__ == "__main__":
    main()

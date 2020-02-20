# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:47:42 2020.

@author: laura
"""

import re
import numpy as np
import pandas as pd


class CleanCBS:
    """Collection of functions for to clean CBS data."""

    def __init__(self, file_lst):
        """
        Initialize class with the list of files.

        Parameters
        ----------
        file_lst : list of str
            list of filenames, either in current working directory,
            or with a longer path attached.

        Returns
        -------
        None.

        """
        self.file_lst = file_lst

        # replacement dictionaries for cleanFiles function
        self.age_dist = {
            "Geslacht": {"T001038": "Total", "3000": "Men",
                         "4000": "Women"},
            "Leeftijd": {"10000": "Total", "22000": "95<",
                         "70100": "0-5", "70200": "5-10",
                         "70300": "10-15", "70400": "15-20",
                         "70500": "20-25", "70600": "25-30",
                         "70700": "30-35", "70800": "35-40",
                         "70900": "40-45", "71000": "45-50",
                         "71100": "50-55", "71200": "55-60",
                         "71300": "60-65", "71400": "65-70",
                         "71500": "70-75", "71600": "75-80",
                         "71700": "80-85", "71800": "85-90",
                         "71900": "90-95"},
            "Postcode": {"NL01": "NL_total", "PC0999": "Unknown"}}

        self.imm_dist = {
            "Geslacht": {"T001038": "Total", "3000": "Men", "4000": "Women"},
            "Migratieachtergrond": {"1012600": "Dutch_background",
                                    "2012605": "Migration_background",
                                    "2012655": "Western_background",
                                    "2012657": "Non-Western_background",
                                    "T001040": "Total",
                                    "H008519": "Africa",
                                    "H008520": "America",
                                    "H008524": "Asia",
                                    "H007933": "Europe",
                                    "H008531": "Oceania",
                                    "H007935": "EU",
                                    "H008552": "Belgium",
                                    "H008592": "Germany",
                                    "H008632": "Indonesia",
                                    "H008673": "Morocco",
                                    "H007119": "Dutch_Caribbean",
                                    "H008718": "Poland",
                                    "H008751": "Suriname",
                                    "H008766": "Turkey",
                                    "A008187": "Remainder_non-Western",
                                    "A008188": "Remainder_Western"},
            "Postcode": {"NL01": "NL_total", "PC0999": "Unknown"}}

        self.pos_house = {
            "Geslacht": {"T001038": "Total", "3000": "Men", "4000": "Women"},
            "PositieInHetHuishouden": {
                "1015100": "Single", "1015110": "Single_parent",
                "1015120": "Couple_kids", "1015130": "Couple_no_kids",
                "1016440": "Child_at_home", "1016510": "Other",
                "1050001": "Person_private_household",
                "1050002": "Person_institutional_household",
                "T009002": "Total"},
            "Postcode": {"NL01": "NL_total", "PC0999": "Unknown"}}

        self.household = {
            "Huishoudenssamenstelling": {
                "1016030": "Multiple_w_children",
                "1016040": "Multiple_no_children",
                "1050010": "Total_private_household",
                "1050015": "Single_person"},
            "Postcode": {"NL01": "NL_total", "PC0999": "Unknown"},
            "GemiddeldeHuishoudensgrootte_2": {".": np.nan}}

        # Filename bases necessary to combine similar files to one file
        self.age_base = "CBS  bevolking geslacht leeftijd postcode .csv"
        self.imm_base = "CBS  geslacht migratieachtergrond postcode .csv"
        self.pos_base = "CBS  geslacht positie huishouden postcode .csv"
        self.hou_base = "CBS  huishoudenssamenstelling postcode .csv"

    def readFiles(self):
        """Read files into a dictionary of dataframes."""
        files = {}
        for i in range(len(self.file_lst)):
            files[i] = pd.read_csv(self.file_lst[i],
                                   sep=";", index_col="ID",
                                   dtype=str)
        self.files = files

    def stripCols(self):
        """Strip leading and trailing whitespaces.

        Function is applied for all columns in every dataframe
        in the dictionary of dataframes.
        """
        for frame in self.files.values():
            for col in frame.columns:
                frame[col] = frame[col].str.strip()

    def cleanFiles(self, repl=None):
        """Replace the codes used in the CBS data.

        Based on metadata.

        This function contains replacement dictionaries for
        the following datasets:
            - Bevolking; geslacht, leeftijd en viercijferige postcode
            - Bevolking; geslacht, migratieachtergrond, viercijferige postcode
            - Bevolking; geslacht, positie huishouden, viercijferige postcode
            - Huishoudens; huishoudenssamenstelling en viercijferige postcode

        For other datasets, a replacement dictionary should be supplied.

        Parameters
        ----------
        repl : dict
            Replacement dictionary. Default value = None.

        Returns
        -------
        Decoded dataset in the form of a dictionary of dataframes
        """
        files = self.files

        for idx, _ in enumerate(files):
            # filename base, filenames should be identical, except for
            # the years that the subset contains."""
            file_base = "".join(re.findall(r"[^0-9;,-]", self.file_lst[idx]))

            # columns to be cast to float
            colh = ["ParticuliereHuishoudens_1",
                    "GemiddeldeHuishoudensgrootte_2"]
            colp = "Bevolking_1"
            if repl is None:
                if file_base == self.age_base:
                    files[idx] = files[idx].replace(self.age_dist)
                    files[idx][colp] = files[idx][colp].astype(float)

                elif file_base == self.imm_base:
                    files[idx] = files[idx].replace(self.imm_dist)
                    files[idx][colp] = files[idx][colp].astype(float)

                elif file_base == self.pos_base:
                    files[idx] = files[idx].replace(self.pos_house)
                    files[idx][colp] = files[idx][colp].astype(float)

                elif file_base == self.hou_base:
                    files[idx] = files[idx].replace(self.household)
                    files[idx][colh] = files[idx][colh].astype(float)

                else:
                    print("no default replacement dict, supply repl")

                files[idx]["Postcode"] = \
                    files[idx]["Postcode"].str.replace("PC", "")
                files[idx]["Perioden"] = \
                    files[idx]["Perioden"].str.replace("JJ00", "").astype(int)

            else:
                files[idx] = files[idx].replace(repl)

        self.clean_files = files

    def combineFiles(self):
        """Combine separate dataframes.

        Based on the common section of the filenames.

        It strips any number from the filename,
        but requires the text part of the filenames to
        be identical in order to be combined.

        Returns
        -------
        Dictionary of combined dataframes
        """
        combine = {"Age": pd.DataFrame(), "Immigration": pd.DataFrame(),
                   "Position_household": pd.DataFrame(),
                   "Household_composition": pd.DataFrame()}

        for idx in range(len(self.clean_files)):
            # filename base
            file_base = "".join(re.findall(r"[^0-9;,-]", self.file_lst[idx]))

            if file_base == self.age_base:
                combine["Age"] = pd.concat([combine["Age"],
                                            self.clean_files[idx]])

            elif file_base == self.imm_base:
                combine["Immigration"] = pd.concat([combine["Immigration"],
                                                    self.clean_files[idx]])

            elif file_base == self.pos_base:
                combine["Position_household"] = \
                    pd.concat([combine["Position_household"],
                               self.clean_files[idx]])

            elif file_base == self.hou_base:
                combine["Household_composition"] = \
                    pd.concat([combine["Household_composition"],
                               self.clean_files[idx]])
            else:
                print("unknown dataset, do a manual concat")

        self.combine = combine
        return self.combine

    def selectYears(self, start_year, end_year):
        """Select the relevant year subsets from dataframes.

        Stores them inin a dictionary of dataframes.
        It requires the dataframes to have a column "Perioden".

        Parameters
        ----------
        start_year : int
            First relevant year
        end_year : int
            Last relevant year

        Returns
        -------
        Dictionary of dataframes with only the relevant years
        """
        combination_dict = self.combine
        self.start_year = start_year
        self.end_year = end_year

        for key, value in combination_dict.items():
            if len(value) > 0:
                cond1 = (value["Perioden"] >= start_year)
                cond2 = (value["Perioden"] <= end_year)
                combination_dict[key] = value.loc[cond1 & cond2]

        self.combine_years = combination_dict

    def returnFiles(self):
        """Return self.files at the current point of cleaning."""
        return self.files

    def saveCSV(self):
        """Save data in csv files.

        Each dataframe in a dictionary of dataframes is converted
        to its own csv file if the dataframe is not empty.
        """
        base_name = "Clean_CBS - {0} ({1}-{2}).csv"
        for key, value in self.combine_years.items():
            if len(value) > 0:
                value.to_csv(base_name.format(key,
                                              self.start_year,
                                              self.end_year))

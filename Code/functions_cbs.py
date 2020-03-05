# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:47:42 2020.

@author: laura
"""

import os
import re
from collections import Counter
import numpy as np
import pandas as pd
from scipy.spatial.distance import pdist, squareform
from functions_general import GeneralFunctions


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
        # initialize everything
        self.file_lst = file_lst
        self.files = None
        self.clean_files = None
        self.combine = None
        self.start_year = None
        self.end_year = None
        self.combine_years = None

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


class CalculateEnergyCBS:
    """Collection of functions to connect Energy data to CBS data."""

    def __init__(self, data, group_col, type_data, columns=None,
                 dist_measure="euclidean"):
        """Calculate the distances for different postcodes.

        Parameters
        ----------
        data : pandas dataframe
            Dataframe that contains multiple groups of data.
        group_col : str
            Name of column containing the groups.
        type_data: str
            Type of the data, "energy" or "cbs"
        columns : list of strings, optional
            Column names for columns to use in the distance calculation.
            The default is None.
        dist_measure : str, optional
            Type of distance measure to be used. The default is "euclidean".
            Other options are: ‘braycurtis’, ‘canberra’, ‘chebyshev’,
            ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, ‘euclidean’,
            ‘hamming’, ‘jaccard’, ‘kulsinski’, ‘mahalanobis’, ‘matching’,
            ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’,
            ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’

        Returns
        -------
        None.
        """
        self.splitGroup(data, group_col)

        if type_data == "energy":
            self.calcDistances(columns, dist_measure)

    @staticmethod
    def createOrdinalColumn(data, conv_col, new_col, values):
        """Convert a column with strings to ordinal.

        The strings are replaced with numbers.

        Parameters
        ----------
        data : pandas dataframe
            Data with a column that needs conversion.
        conv_col : str
            Column name of the column that needs conversion.
        new_col : str
            Column name of the column to store the ordinal values.
        values : list of str
            All values in the conv_col, in the order they are ordinal.

        Returns
        -------
        data : pandas dataframe
            Dataframe with the newly created column.

        """
        values_dict = dict(zip(values, np.arange(len(values))))
        data[new_col] = data[conv_col].map(values_dict)

        return data

    def splitGroup(self, data, group_col):
        """Split dataframe into dictionary of dataframes.

        Every dataframe contains one group of data

        Parameters
        ----------
        data : pandas dataframe
            Dataframe that contains multiple groups of data.
        group_col : str
            Name of column containing the groups

        Returns
        -------
        None.

        """
        data = data.dropna(subset=[group_col])
        groups = data[group_col].unique().tolist()

        data_dict = {}
        for i in groups:
            data_dict[i] = data.loc[data[group_col] == i]
            data_dict[i] = data_dict[i].drop(group_col, axis=1)
        self.data_dict = data_dict

    def returnDict(self, type_dict):
        """Return dictionary of dataframes.

        Can return either the distance dict or the data dict

        Parameters
        ----------
        type_dict : str
            Dictionary type to return. "data", or "distance"

        Returns
        -------
        Dictionary of dataframes.
        """
        if type_dict == "data":
            return self.data_dict
        if type_dict == "distance":
            return self.dist_dict
        else:
            print("Unknown dictionary type")

    @staticmethod
    def groupEnergy(data, en_type):
        """Group data on the Postcode4 level.

        This is performed on one energy type.

        Parameters
        ----------
        data : pandas dataframe
            A dataframe containing data for one energy type.
        en_type : str
            Energy type, as it occurs in the "type" column of data.

        Returns
        -------
        df_mean : pandas dataframe
            Dataframe with data grouped on Postcode4, calculates the mean.
        df_median : pandas dataframe
            Dataframe with data grouped on Postcode4, calculates the median.

        """
        df = data.loc[data["type"] == en_type]
        df = GeneralFunctions.removeOutliers(df, "annual_consume_corrected")

        # create a column for the groupby
        df["Postcode4"] = df["POSTCODE"].str.extract("([0-9]+)")

        df_mean = df.groupby(["Postcode4", "year"]).mean()
        df_median = df.groupby(["Postcode4", "year"]).median()

        return df_mean, df_median

    def calcDistances(self, columns=None, dist_measure="euclidean"):
        """Calculate distances between postcodes.

        Uses the scipy pdist function to calculate pairwise distances.

        Parameters
        ----------
        columns : list of str, optional
            List of columns to be used for the distance calculation.
            The default is None.
        dist_measure : str, optional
            Type of distance measure to be used. The default is "euclidean".
            Other options are: ‘braycurtis’, ‘canberra’, ‘chebyshev’,
            ‘cityblock’, ‘correlation’, ‘cosine’, ‘dice’, ‘euclidean’,
            ‘hamming’, ‘jaccard’, ‘kulsinski’, ‘mahalanobis’, ‘matching’,
            ‘minkowski’, ‘rogerstanimoto’, ‘russellrao’, ‘seuclidean’,
            ‘sokalmichener’, ‘sokalsneath’, ‘sqeuclidean’, ‘yule’

        Returns
        -------
        None.
        """
        dist_dict = {}
        for frame in self.data_dict.keys():
            if columns is None:
                print("No columns specified, using all columns.")
                columns = self.data_dict[frame].columns.tolist()

            df = self.data_dict[frame][columns]
            dist_dict[frame] = \
                pd.DataFrame(squareform(pdist(df, metric=dist_measure)),
                             index=df.index,
                             columns=df.index)

        self.dist_dict = dist_dict

    def findNSmallestDistances(self, n):
        """Create dataframe with the n smallest distances.

        Parameters
        ----------
        n : int
            Number of smallest distances for each dataframe in the dictionary
            of dataframes.

        Returns
        -------
        results : pandas dataframe
            Dataframe with the n smallest distances for each dataframe
            in the dictionary of dataframes.
        """
        temp_lst = []
        for frame in self.dist_dict.keys():
            df = self.dist_dict[frame]
            df = pd.DataFrame(df.unstack())

            df.index.names = ["GroupA", "GroupB"]
            df.columns = ["Distance"]
            df.reset_index(inplace=True)

            # remove mirror duplicates
            df = df.loc[pd.DataFrame(
                        np.sort(df[['GroupA', 'GroupB']], 1),
                        index=df.index).drop_duplicates(keep='first').index]
            df.replace(0, np.nan, inplace=True)
            chunk = df.nsmallest(n, "Distance")
            chunk["Group"] = frame
            temp_lst.append(chunk)

        results = pd.concat(temp_lst)

        return results

    def pivotCBS(self, index, columns, values):
        """Pivot the cbs data to a usable format.

        The pivot is necessary in order to calculate distances
        between postcodes.

        Parameters
        ----------
        index : str
            Index column for new dataframe.
        columns : list of str
            Columns that need to be pivoted.
        values : str
            Values to fill the new dataframe.

        Returns
        -------
        None.
        """
        for frame in self.data_dict.keys():
            df = self.data_dict[frame]
            df = df.pivot_table(index=[index],
                                columns=columns,
                                values=values)
            self.data_dict[frame] = df


class ConnectDistances:
    """Connecting the smallest distances of energy and cbs data."""

    def __init__(self, path):
        self.common_pairs = None
        self.readFiles(path)

    def readFiles(self, path):
        files = os.listdir(path)

        data = {}
        for i in files:
            data[i] = pd.read_csv(os.path.join(path, i))

        self.data = data

    def findPostcodePairs(self):
        postcode_pairs = {}
        for i in self.data:
            df = self.data[i]
            df["Combined"] = tuple(zip(df["GroupA"], df["GroupB"], df["Group"]))
            postcode_pairs[i] = df["Combined"]

        self.postcode_pairs = postcode_pairs
        print("Possible files to compare:")
        print("\n".join(postcode_pairs.keys()))

    @staticmethod
    def compareObjects(s, t):
        """See if list or tuple contains exactly the same elements."""
        return Counter(s) == Counter(t)

    def findCommonPairs(self, file_energy, file_demographics):

        demographics = self.postcode_pairs[file_demographics]
        energy = self.postcode_pairs[file_energy]
        common_pairs = []

        for i in demographics:
            for j in energy:
                print(i, j)
                if self.compareObjects(i, j):
                    common_pairs.append(i)

        self.common_pairs = common_pairs
        return common_pairs
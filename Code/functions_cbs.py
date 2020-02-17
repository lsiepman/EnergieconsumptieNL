# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:47:42 2020

@author: laura
"""

#%% IMPORTS
import pandas as pd
import numpy as np
import re


#%% FUNCTIONS
class CleanCBS:
    """Collection of functions to read, clean, combine and select the relevant data from the CBS datasets
    
    Parameters
    ------------
    file_list : list
        List of strings with filenames of files that need to be read from the current working directory
        """
    def __init__(self, file_lst):
        self.file_lst = file_lst
     
        
    def ReadFiles(self):
        """Reads files into a dictionary of dataframes"""
        files = {}
        for i in range(len(self.file_lst)):
            files[i] = pd.read_csv(self.file_lst[i], sep = ";", index_col = "ID", dtype = str)
        self.files = files
        
        return self.files
    
        
    def StripCols(self):
        """Strips leading and trailing whitespaces is all columns in every dataframe in the dictionary of dataframes"""
        for frame in self.files.values():
            for col in frame.columns:
                frame[col] = frame[col].str.strip()
        return self.files
        
                
    def CleanFiles(self, repl = None):
        """Replaces the codes used in the CBS data with the human understandable values from the metadata files. This function contains replacement dictionaries for the following datasets: 
            - Bevolking; geslacht, leeftijd en viercijferige postcode
            - Bevolking; geslacht, migratieachtergrond, viercijferige postcode
            - Bevolking; geslacht, positie huishouden, viercijferige postcode
            - Huishoudens; huishoudenssamenstelling en viercijferige postcode
            
        For other datasets, a replacement dictionary should be supplied.
        
        Parameters
        -----------
        repl : dict
            Replacement dictionary. Default value = None.
            
        Returns
        ----------
        Decoded dataset in the form of a dictionary of dataframes
        """ 
        age_dist = {
            "Geslacht" : {"T001038" : "Total", "3000" : "Men", "4000" : "Women"}, 
            "Leeftijd" : {"10000" : "Total", "22000" : "95<", "70100" : "0-5", 
                          "70200" : "5-10", "70300" : "10-15", "70400" : "15-20",
                          "70500" : "20-25", "70600" : "25-30","70700" : "30-35",
                          "70800" : "35-40", "70900" : "40-45", "71000" : "45-50", 
                          "71100" : "50-55", "71200" : "55-60", "71300" : "60-65", 
                          "71400" : "65-70", "71500" : "70-75", "71600" : "75-80", 
                          "71700" : "80-85", "71800" : "85-90", "71900" : "90-95"},
            "Postcode" : {"NL01" : "NL_total", "PC0999" : "Unknown"}}
        
        imm_dist = {
            "Geslacht" : {"T001038" : "Total", "3000" : "Men","4000" : "Women"}, 
            "Migratieachtergrond" : {"1012600" : "Dutch_background",
                                     "2012605" : "Migration_background", 
                                     "2012655" : "Western_background",
                                     "2012657" : "Non-Western_background",
                                     "T001040" : "Total", "H008519" : "Africa", 
                                     "H008520" : "America", "H008524" : "Asia", 
                                    "H007933" : "Europe","H008531" : "Oceania",
                                    "H007935" : "EU", "H008552" : "Belgium", 
                                    "H008592" : "Germany", "H008632" : "Indonesia", 
                                    "H008673" : "Morocco", 
                                    "H007119" : "Dutch_Caribbean", 
                                    "H008718" : "Poland", "H008751" : "Suriname",
                                    "H008766" : "Turkey", 
                                    "A008187" : "Remainder_non-Western", 
                                    "A008188": "Remainder_Western"},
            "Postcode" : {"NL01" : "NL_total", "PC0999" : "Unknown"}}
        
        pos_house = {
            "Geslacht" : {"T001038" : "Total", "3000" : "Men", "4000" : "Women"},
            "PositieInHetHuishouden" : {"1015100" : "Single", 
                                        "1015110" : "Single_parent",
                                        "1015120" : "Couple_kids", 
                                        "1015130" : "Couple_no_kids",
                                        "1016440" : "Child_at_home", 
                                        "1016510" : "Other", 
                                        "1050001" : "Person_private_household",
                                        "1050002" : "Person_institutional_household", 
                                        "T009002" : "Total"}, 
            "Postcode" : {"NL01" : "NL_total", "PC0999" : "Unknown"}}
        
        
        household = {
            "Huishoudenssamenstelling" : {"1016030" : "Multiple_w_children",
                                          "1016040" : "Multiple_no_children",
                                          "1050010"  : "Total_private_household",
                                          "1050015" : "Single_person"}, 
            "Postcode" : {"NL01" : "NL_total", "PC0999" : "Unknown"},
            "GemiddeldeHuishoudensgrootte_2" : {"." : np.nan}} 
        
        files = self.files
        
        for idx in range(len(files)):
            cat_file = "".join(re.findall(r"[^0-9;,-]", self.file_lst[idx]))
            
            if repl == None:
                if cat_file == "CBS  bevolking geslacht leeftijd postcode .csv":
                    files[idx] = files[idx].replace(age_dist)
                    files[idx]["Bevolking_1"] = files[idx]["Bevolking_1"].astype(float)
                    
                elif cat_file == "CBS  geslacht migratieachtergrond postcode .csv":
                    files[idx] = files[idx].replace(imm_dist)
                    files[idx]["Bevolking_1"] = files[idx]["Bevolking_1"].astype(float)
                    
                elif cat_file == "CBS  geslacht positie huishouden postcode .csv":
                    files[idx] = files[idx].replace(pos_house)
                    files[idx]["Bevolking_1"] = files[idx]["Bevolking_1"].astype(float)
                    
                elif cat_file == "CBS  huishoudenssamenstelling postcode .csv":
                    files[idx] = files[idx].replace(household)
                    files[idx][["ParticuliereHuishoudens_1", "GemiddeldeHuishoudensgrootte_2"]] = files[idx][["ParticuliereHuishoudens_1", "GemiddeldeHuishoudensgrootte_2"]].astype(float)
                    
                else:
                    print("no default replacement dict, supply repl")            
            
                files[idx]["Postcode"] = files[idx]["Postcode"].str.replace("PC", "")
                files[idx]["Perioden"] = files[idx]["Perioden"].str.replace("JJ00", "").astype(int)
                
            else:
                files[idx] = files[idx].replace(repl)
                    
        self.clean_files = files
        return self.clean_files
        
    
    def CombineFiles(self):
        """Combines separate dataframes based on the common section of the filenames. It strips any number from the filename, but requires the text part of the filenames to be identical in order to be combined
        
        Returns
        -------
        Dictionary of combined dataframes
        """
        combine = {"Age" : pd.DataFrame(), "Immigration" : pd.DataFrame(),
                   "Position_household" : pd.DataFrame(), 
                   "Household_composition" : pd.DataFrame()}
        
        for idx in range(len(self.clean_files)):
            cat_file = "".join(re.findall(r"[^0-9;,-]", self.file_lst[idx]))
            
            if cat_file == "CBS  bevolking geslacht leeftijd postcode .csv":
                   combine["Age"] = pd.concat([combine["Age"], self.clean_files[idx]])
                   
            elif cat_file == "CBS  geslacht migratieachtergrond postcode .csv":
                combine["Immigration"] = pd.concat([combine["Immigration"], self.clean_files[idx]])
                
            elif cat_file == "CBS  geslacht positie huishouden postcode .csv":
                combine["Position_household"] = pd.concat([combine["Position_household"], self.clean_files[idx]])
                
            elif cat_file == "CBS  huishoudenssamenstelling postcode .csv":
                combine["Household_composition"] = pd.concat([combine["Household_composition"], self.clean_files[idx]])
            else:
                print("unknown dataset, do a manual concat")
                
        self.combine = combine
        return self.combine
    
    
    def SelectYears(self, start_year, end_year):
        """Selects the relevant years from dataframes in a dictionary of dataframes. It requires the dataframes to have a column "Perioden".
        
        Parameters
        ----------
        start_year : int
            First relevant year
        end_year : int
            Last relevant year
            
        Returns
        ---------
        Dictionary of dataframes with only the relevant years
        """
        combination_dict = self.combine
        self.start_year = start_year
        self.end_year = end_year
        
        for key, value in combination_dict.items():
            if len(value) > 0:
                
                combination_dict[key] = value.loc[(value["Perioden"] >= start_year) & (value["Perioden"] <= end_year)]
                
        self.combine_years = combination_dict
        return self.combine_years
    
    
    def SaveCSV(self):
        """Saves the dataframes in a dictionary of dataframes to csv files when the dataframe is not empty."""
        for key, value in self.combine_years.items():
            if len(value) > 0:
                value.to_csv("Clean_CBS - {0} ({1}-{2}).csv".format(key, self.start_year, self.end_year))
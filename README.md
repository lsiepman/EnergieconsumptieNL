# Energy consumption in the Netherlands

Enexis, Liander, and Stedin, the three major network administators in the Netherlands, publish energy consumption data as open data on their websites. 


## Description of code
Short description of every code file and its results

*combining_data.py*
- Combines all seperate Enexis, Liander, and Stedin files. 
- Corrects difference between the year in the filename and the year the data was gathered
- Connects it to the geolocation data.
- Creates one large file with all data (in .gitignore)
- The output of this file is used in the other files

*example_map_interactive.py*
- Uses folium to create interactive html maps with energy consumption data
- This file shows how to use the function to create maps

*example_map_static.py*
- Uses cartopy and matplotlib to create a static map with energy consumption data
- This file shows how to use the function to create maps

*functions.py*
- All general functions are stored in this file for later use in different files.
- Functions can be used by importing the file

*graphs_energy_over_time.ipynb*
- Data exploration.
- Graphs over time for  the entire country and some cities

*maps_interactive_cities.py*
- Plots folium maps with energy consumption for the 10 largest cities in the Netherlands.
[Amsterdam, Rotterdam, The Hague, Utrecht, Eindhoven, Groningen, Tilburg, Almere, Breda, Nijmegen]

*maps_static_national.py*
- Creates a cartopy map with all gas or electricity usage for a year
- There are too much data points, so the process is very slow, especially for the more recent years of electricity usage


## DATA
- Energy data was taken from [Luca Basanisi
 on Kaggle](https://www.kaggle.com/lucabasa/dutch-energy)
 - Original data from:
   - [Enexis](https://www.enexis.nl/over-ons/wat-bieden-we/andere-diensten/open-data)
   - [Liander](https://www.liander.nl/partners/datadiensten/open-data/data)
   - [Stedin](https://www.stedin.net/zakelijk/open-data/verbruiksgegevens)
 - Some processing was made with the code available on [GitHub](https://github.com/lucabasa/kaggle_dutch_energy/blob/master/raw_data_cleaning.ipynb)
- Geolocation data was obtained through [OpenAddresses](https://openaddresses.io/)
- Shapefile data was obtained from [GADM](https://gadm.org/)

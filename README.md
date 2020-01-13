# Energy consumption in the Netherlands

Enexis, Liander, and Stedin, the three major network administators in the Netherlands, publish energy consumption data as open data on their websites. 


## Description of code
Short description of every .py file and its results

*combining_data.py*
- Combines all seperate Enexis, Liander, and Stedin files. 
- Corrects difference between the year in the filename and the year the data was gathered
- Connects it to the geolocation data.
- Creates one file with all data (in .gitignore)

*interactive_map_energy_consumption.py*
- Uses folium to create interactive html maps with energy consumption data

## DATA
- Energy data was taken from [Luca Basanisi
 on Kaggle](https://www.kaggle.com/lucabasa/dutch-energy)
 - Original data from:
   - [Enexis](https://www.enexis.nl/over-ons/wat-bieden-we/andere-diensten/open-data)
   - [Liander](https://www.liander.nl/partners/datadiensten/open-data/data)
   - [Stedin](https://www.stedin.net/zakelijk/open-data/verbruiksgegevens)
 - Some processing was made with the code available on [GitHub](https://github.com/lucabasa/kaggle_dutch_energy/blob/master/raw_data_cleaning.ipynb)
- Geolocation data was obtained through [OpenAddresses](https://openaddresses.io/)

# Notes on this project

## 1. When looking at maps showing the energy consumption in the Netherlands, can you see any regional patterns in the data?

*Method* 
Plotting usage dots, corrected for the number of active connections, after removal of outliers, on a map for each energy type for all years to visually examine the usage per zipcode.
Interactive maps were created using the python package Folium. Interactive HTML files were created. Maps showing the entire country are larger than 100 MB and are not placed on github. They can be recreated using the exampe_map_interactive.py code file.
Static maps were created with the python packages cartopy and matplotlib.

*Expectations*
1. More gas consumption outside of the [Randstad](https://en.wikipedia.org/wiki/Randstad), because the larger cities have relatively more appartment buildings and connected houses than the more rural parts of the country. It is assumed that detached houses, which have more wall surface area touching the outside air, will use more gas to keep the house warm than a appartment in an appartment building.
2. No clear differences between cities and rural areas in electricity consumption, since the usage is correct for the the number of active connections

*Results*
- When outliers were not removed, no clear regional differences could be found for either gas or electricity consumption. This probably was due to the fact that zipcodes which had very high energy consumption, skewed the colour scale used to visualise the usage
- Even after the outliers were removed, it was difficult to see trends due to the amount of data. (which also makes plotting any kind of map slow)

*Next steps*
- Examine which postcodes have an excessively high energy consumption (gas and/or electricity) and try to discover why
- Visualise cities [Amsterdam, Rotterdam, The Hague, Utrecht, Eindhoven, Groningen, Tilburg, Almere, Breda, Nijmegen]
- Visualise smaller regions on static maps for more detail (Basemap)



  
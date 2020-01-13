# Notes on this project

## 1. When looking at the energy consumption in the Netherlands, can you see any regional patterns in the data?

*Method* 
1. Plotting usage dots, corrected for the number of active connections, on a map for each energy type for all years to visually examine the usage per zipcode
2. Removing extremely high consumption and plotting the map again. 

*Expectations*
1. More gas consumption outside of the [Randstad](https://en.wikipedia.org/wiki/Randstad), because the larger cities have relatively more appartment buildings and connected houses than the more rural parts of the country. It is assumed that detached houses, which have more wall surface area touching the outside air, will use more gas to keep the house warm than a appartment in an appartment building.
2. No clear differences between cities and rural areas in electricity consumption, since the usage is correct for the the number of active connections

*Results*
- No clear regional differences could be found for either gas or electricity consumption
- Some postcodes had very high energy consumption, skewing the colour scale used to visualise the usage

*Next steps*
- Examine which postcodes have an excessively high energy consumption (gas and/or electricity) and try to discover why
- Visualise the national map again after removing the outliers to see whether the expected pattern will show
- Visualise smaller regions on static maps for more detail (Basemap)

  
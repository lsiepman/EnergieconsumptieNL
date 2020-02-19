# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 13:06:45 2020.

@author: laura
"""

from functions_general import GeneralFunctions
import folium
import branca.colormap as bcm
import re


class MapInteractive:
    """Collection of Interactive Map Functions.

    These functions are necessary for creating interactive Folium maps.
    """

    def __init__(self, data, energy_type, year):
        """Select the data for the interactive map.

        Remove rows with 0 active connections and corrects for
        the number of active connections per zipcode.

        Parameters
        ----------
        data : pandas dataframe
            energy consumption data
        energy_type : str
            "gas", or "electricity"
        year  : int
            year to plot

        Returns
        -------
        subset of original dataframe
        """
        self.energy_type = energy_type
        self.data_col = "annual_consume_corrected"

        condition1 = (data["type"] == energy_type)
        condition2 = (data["year"] == year)
        df = data.loc[condition1 & condition2]

        # remove data without geolocation
        df = df.dropna(subset=["LAT", "LON"]).reset_index(drop=True)

        # correct for number of active connections
        df = GeneralFunctions.correctForConnection(df)
        df = GeneralFunctions.removeOutliers(df, self.data_col)

        # remove inactive connections with energy consumption
        df = df.loc[df["perc_of_active_connections"] != 0]

        self.data = df

    def plotMap(self, filename, caption_legend):
        """Create a folium map (JS Leaflet).

        The map is saved in the current working directory, or specified with
        the file name.

        Parameters
        ----------
        filename : str
            final filename, without file extension
        caption_legend : str
            title of the legend

        Returns
        -------
        HTML file with interactive map

        """
        # color scale
        cmap = bcm.LinearColormap(['green', 'yellow', 'red'],
                                  vmin=self.data[self.data_col].min(),
                                  vmax=self.data[self.data_col].max())
        cmap.caption = caption_legend

        # create map
        interactive_map = folium.Map(location=[52.092876, 5.104480],
                                     zoom_start=6.5)
        interactive_map.add_child(cmap)

        # plot points
        for i in range(len(self.data)):
            colors = cmap(self.data[self.data_col].iloc[i])
            folium.CircleMarker(location=[self.data["LAT"].iloc[i],
                                          self.data["LON"].iloc[i]],
                                radius=2, weight=0, fill_opacity=1,
                                fill=True,
                                fill_color=colors).add_to(interactive_map)

        # save map
        interactive_map.save("{}.html".format(filename))


class MultipleInteractiveMaps(MapInteractive):
    """Create a series of interactive maps.

    Uses the MapInteractive class
    """

    def __init__(self, data, energy_type):
        """Select the data for the interactive map.

        Remove rows with 0 active connections and corrects for
        the number of active connections per zipcode.

        Parameters
        ----------
        data : pandas dataframe
            energy consumption data
        energy_type : str
            "gas", or "electricity"
        year  : int
            year to plot

        Returns
        -------
        subset of original dataframe
        """
        self.energy_type = energy_type
        self.data_col = "annual_consume_corrected"

        years = data["year"].unique().tolist()
        data = data.loc[data["type"] == energy_type]

        # remove data without geolocation
        data = data.dropna(subset=["LAT", "LON"]).reset_index(drop=True)

        # correct for number of active connections
        data = GeneralFunctions.correctForConnection(data)

        # remove inactive connections with energy consumption
        data = data.loc[data["perc_of_active_connections"] != 0]

        data_dict = {}
        for year in years:
            df = data.loc[data["year"] == year]
            df = GeneralFunctions.removeOutliers(df, self.data_col)
            data_dict[year] = df

        self.energy_dict = data_dict

    def plotMapYears(self, filename_base, unit_energy):
        """Plot a series of interactive maps.

        Uses the PlotInteractiveMap function to plot.

        Parameters
        ----------
        filename_base : str
            standard section of all filenames, without file extension
        unit_energy : str
            unit of the energy type, used in legend caption

        Returns
        -------
        saves the html folium maps in the current working directory,
        or at another locations determined by the filename_base.
        """
        for i in self.energy_dict:
            year = re.search(r"[0-9]{4}$", str(i)).group()
            caption = "{0} consumption in {1} ({2})".format(self.energy_type,
                                                            year,
                                                            unit_energy)
            self.data = self.energy_dict[i]
            self.plotMap("{0}_{1}".format(filename_base, i), caption)

            print("finished {}".format(i, filename_base))

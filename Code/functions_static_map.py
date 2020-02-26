# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 14:03:56 2020.

@author: laura
"""

import os
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib import cm as cmx
from functions_general import GeneralFunctions


class StaticMap:
    """Functions for plotting static maps."""
    def __init__(self, data, year, energy_type):
        """
        Select data for static map.

        Parameters
        ----------
        data : pandas dataframe
            Dataframe with energy consumption.
        year : int
            Year to plot.
        energy_type : str
            Which energy type to plot. "electricity" or "gas"

        Returns
        -------
        None.

        """

        self.energy_type = energy_type
        self.year = year
        self.data_col = "annual_consume_corrected"

        condition1 = (data["year"] == self.year)
        condition2 = (data["type"] == self.energy_type)
        data = data.loc[condition1 & condition2]

        data = data.dropna(subset=["LAT", "LON"]).reset_index(drop=True)
        data = GeneralFunctions.correctForConnection(data)
        data = GeneralFunctions.removeOutliers(data, self.data_col)

        self.data = data

    def plotStaticMap(self, title, label_colorbar, shapes, path,
                      extent=[3, 8, 50.5, 54]):
        """
        Plots a static map of energy usage in the Netherlands.

        The colour of the points indicates the usage.

        Parameters
        ----------
        title : str
            title of the plot
        label_colorbar : str
            title of the color bar
        shapes : polygons
            a (list of) polygons that are used to draw the map
        path : str
            save location of the plot
        extent : list of 4 int
            determines the zoom level and focus of the map.
            Has a default value that shows the entirety of the Netherlands.

        Returns
        --------
        Plot in the working directory or a subfolder based on title

        """
        min_data = min(self.data[self.data_col])
        max_data = max(self.data[self.data_col])

        fig = plt.figure(figsize=(8, 5))
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.add_geometries(shapes, ccrs.PlateCarree(),
                          edgecolor='black', facecolor='gray', alpha=0.2)
        ax.set_extent(extent, ccrs.PlateCarree())
        norm = colors.Normalize(vmin=min_data, vmax=max_data)
        cmap = plt.get_cmap('RdYlGn_r')
        m = cmx.ScalarMappable(cmap=cmap, norm=norm)

        for point in range(len(self.data[self.data_col])):
            plt.plot(self.data["LON"].iloc[point],
                     self.data["LAT"].iloc[point],
                     'o',
                     color=m.to_rgba(self.data[self.data_col].iloc[point]),
                     transform=ccrs.PlateCarree())
        plt.title(title)
        cb = plt.colorbar(m)
        cb.set_label(label_colorbar)

        save_loc = os.path.join(path, title)
        plt.savefig(save_loc, dpi=300)

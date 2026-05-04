# -*- coding: utf-8 -*-
"""
Plot paris bicycle network plan progress with a choropleth map.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib_map_utils.core.scale_bar import scale_bar

FOLDER_ARR = "./data/processed/"
FOLDER_BIKE = "./data/raw/"
FOLDERPLOT = "./plots/"
DPI = 400


# TODO add number of arrondissement inside the choropleth map
def main():
    gdf_arr = gpd.read_file(FOLDER_ARR + "paris_vote_arr_2020_bikenet.gpkg")
    fig, ax = plt.subplots(figsize=[11.69, 8.27], layout="tight")
    cax = ax.inset_axes([0.82, 0.42, 0.03, 0.45])
    kwargs = {
        "vmin": 0,
        "vmax": 1,
        "legend_kwds": {
            "cax": cax,
            "format": mtick.PercentFormatter(1),
            "ticks": [0.0, 0.25, 0.5, 0.75, 1.0],
        },
    }
    ax.text(
        x=0.835,
        y=0.91,
        transform=ax.transAxes,
        s="$\%$ acc",
        fontsize=20,
        ha="center",
        va="center",
    )
    gdf_arr.plot(
        ax=ax,
        column="length_accomplished_share",
        cmap="viridis",
        legend=True,
        edgecolor="white",
        linewidth=5,
        **kwargs,
    )
    scale_bar(
        ax,
        location="lower left",
        style="ticks",
        bar={"projection": gdf_arr.crs, "unit": "km", "major_mult": 1, "major_div": 3},
        labels={"style": "first_last"},
    )
    cax.tick_params(labelsize=13)
    ax.axis("off")
    fig.savefig(FOLDERPLOT + "map_bikeplan_choropleth.jpeg", dpi=DPI)


if __name__ == "__main__":
    main()

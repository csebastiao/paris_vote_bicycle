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
NUMBER_SIZE = 13


# TODO move scale bar up and right
# TODO make number look cooler
# TODO rename the % acc
# TODO Move 16, C, and 12 to better positions
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
    # Plot results
    gdf_arr.plot(
        ax=ax,
        column="length_accomplished_share",
        cmap="viridis",
        legend=True,
        edgecolor="white",
        linewidth=5,
        **kwargs,
    )
    # Label colormap
    ax.text(
        x=0.835,
        y=0.91,
        transform=ax.transAxes,
        s="$\%$ acc",
        fontsize=20,
        ha="center",
        va="center",
    )
    # Add scale bar
    scale_bar(
        ax,
        location="lower left",
        style="ticks",
        bar={"projection": gdf_arr.crs, "unit": "km", "major_mult": 1, "major_div": 3},
        labels={"style": "first_last", "fontsize": NUMBER_SIZE},
    )
    cax.tick_params(labelsize=NUMBER_SIZE)
    rep_point = gdf_arr.geometry.representative_point()
    arrs = gdf_arr["NUM_ARROND"].values
    # Add arrondissement number
    for i in range(len(gdf_arr)):
        if arrs[i] == 1:
            text = "C"
        else:
            text = arrs[i]
        ax.text(
            x=rep_point[i].xy[0][0],
            y=rep_point[i].xy[1][0],
            s=text,
            color="white",
            fontweight="bold",
            ha="center",
            va="center",
            fontsize=20,
        )
    ax.axis("off")
    fig.savefig(FOLDERPLOT + "map_bikeplan_choropleth.jpeg", dpi=DPI)


if __name__ == "__main__":
    main()

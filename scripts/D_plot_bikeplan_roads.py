# -*- coding: utf-8 -*-
"""
Plot paris bicycle network plan progress.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.ticker as mtick
from matplotlib_map_utils.core.scale_bar import scale_bar
import numpy as np

FOLDER_ARR = "./data/processed/"
FOLDER_BIKE = "./data/raw/"
FOLDERPLOT = "./plots/"
STATE_MAP = {
    "Pas d'aménagement": "Not built yet",
    "Provisoire ou coronapiste": "Not built yet",
    "Réalisé Pré-2021": "Built before 2021",
    "Réalisé dans le Plan Vélo": "Built",
    "Hors Plan Vélo (Embellir)": "Built",
    "Annoncé réalisé": "Built",
}
COLORMAP = "viridis_r"
END_CMAP = 0.66
STATE_COLOR = {
    "Built before 2021": "silver",
    "Not built yet": plt.get_cmap(COLORMAP)(0),
    "Built": plt.get_cmap(COLORMAP)(END_CMAP),
}
NUMBER_SIZE = 10
ARR_SIZE = 15
DPI = 400


def main():
    gdf_arr = gpd.read_file(FOLDER_ARR + "paris_vote_arr_2020_bikenet.gpkg")
    # Plot bicycle plan progress over arrondissement
    gdf_bikenet = gpd.read_file(FOLDER_BIKE + "bikenet_paris_2026_01_28.json")
    gdf_bikenet = gdf_bikenet.set_crs(epsg=4326)
    gdf_bikenet = gdf_bikenet.to_crs(gdf_arr.crs)
    gdf_bikenet["Etat"] = gdf_bikenet["Etat"].map(STATE_MAP)
    gdf_bikenet["color"] = gdf_bikenet["Etat"].map(STATE_COLOR)
    fig = plt.figure(figsize=[11.69, 8.27])
    ax_f = fig.add_axes((0, 0, 0.55, 1))
    for state, color in STATE_COLOR.items():
        gdf_bikenet[gdf_bikenet["Etat"] == state].plot(
            ax=ax_f, color=color, linewidth=2, label=state
        )
    ax_f.legend()
    gdf_arr.plot(ax=ax_f, color="black", edgecolor="white", linewidth=5)
    # Add scale bar
    scale_bar(
        ax_f,
        location="lower left",
        style="ticks",
        bar={"projection": gdf_arr.crs, "unit": "km", "major_mult": 1, "major_div": 3},
        labels={"style": "first_last", "fontsize": NUMBER_SIZE},
    )
    ax_f.axis("off")
    # Plot choropleth map
    ax_s = fig.add_axes((0.45, 0, 0.55, 1))
    cax = ax_s.inset_axes([0.82, 0.42, 0.03, 0.45])
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
        ax=ax_s,
        column="length_accomplished_share",
        cmap=truncate_colormap(plt.get_cmap(COLORMAP), maxval=END_CMAP),
        legend=True,
        edgecolor="white",
        linewidth=5,
        **kwargs,
    )
    # Label colormap
    ax_s.text(
        x=0.835,
        y=0.91,
        transform=ax_s.transAxes,
        s="N",
        fontsize=ARR_SIZE,
        ha="center",
        va="center",
    )
    cax.tick_params(labelsize=NUMBER_SIZE)
    rep_point = gdf_arr.geometry.representative_point()
    arrs = gdf_arr["NUM_ARROND"].values
    # Add arrondissement number
    for i in range(len(gdf_arr)):
        if arrs[i] == 1:
            text = "C"
            xx = rep_point[i].xy[0][0] - 300
            yy = rep_point[i].xy[1][0] + 300
        elif arrs[i] == 5:
            xx = rep_point[i].xy[0][0] - 200
            yy = rep_point[i].xy[1][0] - 100
            text = arrs[i]
        elif arrs[i] == 6:
            xx = rep_point[i].xy[0][0] + 200
            yy = rep_point[i].xy[1][0] - 100
            text = arrs[i]
        elif arrs[i] == 8:
            xx = rep_point[i].xy[0][0]
            yy = rep_point[i].xy[1][0] - 100
            text = arrs[i]
        elif arrs[i] == 12:
            xx = rep_point[i].xy[0][0]
            yy = rep_point[i].xy[1][0] - 100
            text = arrs[i]
        elif arrs[i] == 13:
            xx = rep_point[i].xy[0][0] - 2000
            yy = rep_point[i].xy[1][0] + 100
            text = arrs[i]
        elif arrs[i] == 15:
            xx = rep_point[i].xy[0][0] - 100
            yy = rep_point[i].xy[1][0] - 200
            text = arrs[i]
        elif arrs[i] == 16:
            xx = rep_point[i].xy[0][0] + 900
            yy = rep_point[i].xy[1][0] + 300
            text = arrs[i]
        else:
            xx = rep_point[i].xy[1][0]
            yy = rep_point[i].xy[1][0]
            text = arrs[i]
        ax_s.text(
            x=xx,
            y=yy,
            s=text,
            color="white",
            fontweight="bold",
            ha="center",
            va="center",
            fontsize=ARR_SIZE,
        )
    ax_s.axis("off")
    fig.savefig(FOLDERPLOT + "map_bikeplan.jpeg", dpi=DPI, bbox_inches="tight")


# Source - https://stackoverflow.com/a/18926541
def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        "trunc({n},{a:.2f},{b:.2f})".format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)),
    )
    return new_cmap


if __name__ == "__main__":
    main()

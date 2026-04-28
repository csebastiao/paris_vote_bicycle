# -*- coding: utf-8 -*-
"""
Plot paris official data.
"""

import geopandas as gpd
import matplotlib.pyplot as plt


FOLDER_DATA = "./data/processed/paris_official_data/"
FOLDERPLOT = "./plots/"
PLOT_COLS = {
    "median_income": "Greens",
    "share_commuter_cyclist": "Greens",
    "share_commuter_driver": "Reds",
    "Left_wing_share": "Reds",
    "Right_wing_share": "Blues",
    "ratio_LR": "bwr_r",
}
DPI = 300


def main():
    gdf = gpd.read_file(FOLDER_DATA + "paris_vote_arr_2020.gpkg")
    for column_name, cmap in PLOT_COLS.items():
        fig, ax = plt.subplots(layout="constrained")
        if column_name == "ratio_LR":
            kwargs = {"vmin": -0.6, "vmax": 0.6}
        else:
            kwargs = {}
        gdf.plot(
            ax=ax, column=column_name, cmap=cmap, legend=True, linewidth=2, **kwargs
        )
        ax.axis("off")
        fig.savefig(FOLDERPLOT + "Paris_" + column_name + ".png", dpi=DPI)


if __name__ == "__main__":
    main()

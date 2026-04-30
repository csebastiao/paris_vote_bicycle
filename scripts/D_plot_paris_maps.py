# -*- coding: utf-8 -*-
"""
Plot paris official data.
"""

import geopandas as gpd
import matplotlib.pyplot as plt


FOLDER_DATA = "./data/processed/"
FOLDERPLOT = "./plots/"
PLOT_COLS = {
    "median_income": "RdYlGn",
    "share_commuter_cyclist": "Greens",
    "share_commuter_driver": "Reds",
    "Left_wing_share": "Reds",
    "Right_wing_share": "Blues",
    "ratio_LR": "bwr_r",
    "length_accomplished_share": "RdYlGn",
    "length_before_2021": "RdYlGn",
    "length_before_2021_norm": "RdYlGn",
    "length_planned": "RdYlGn",
    "length_planned_norm": "RdYlGn",
}
DPI = 300


# TODO make json file for parameters
def main():
    gdf = gpd.read_file(FOLDER_DATA + "paris_vote_arr_2020_bikenet.gpkg")
    for column_name, cmap in PLOT_COLS.items():
        fig, ax = plt.subplots(figsize=[11.69, 8.27], layout="constrained")
        if column_name == "ratio_LR":
            kwargs = {"vmin": -0.6, "vmax": 0.6}
        else:
            kwargs = {}
        gdf.plot(ax=ax, column=column_name, cmap=cmap, legend=True, **kwargs)
        ax.axis("off")
        fig.savefig(FOLDERPLOT + "Paris_" + column_name + ".jpeg", dpi=DPI)


if __name__ == "__main__":
    main()

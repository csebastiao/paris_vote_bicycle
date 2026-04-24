# -*- coding: utf-8 -*-
"""
Plot paris official data.
"""

import geopandas as gpd
import matplotlib.pyplot as plt


FOLDER_DATA = "./data/processed/paris_official_data/"
FOLDERPLOT = "./plots/"
PARTY_DICT = {
    "LUC": "Purples",
    "LUD": "Blues",
    "LUG": "Oranges",
    "LFI": "Reds",
    "LEXD": "Greys",
}
DPI = 300


def main():
    gdf_pop = gpd.read_file(FOLDER_DATA + "paris_dem_iris_2021_condensed_filledna.gpkg")
    for column_name, cmap in {
        "pop_density": "inferno",
        "median_income": "Greens",
        "share_commuter_cyclist": "Greens",
        "share_commuter_driver": "Reds",
    }.items():
        fig, ax = plt.subplots(layout="constrained")
        gdf_pop.plot(
            ax=ax, column=column_name, cmap=cmap, legend=True, scheme="fisher_jenks"
        )
        ax.axis("off")
        fig.savefig(FOLDERPLOT + "Paris_" + column_name + "_IRIS.png", dpi=DPI)
    gdf_vote = gpd.read_file(FOLDER_DATA + "paris_vote_arr_2020.gpkg")
    fig, ax = plt.subplots(layout="constrained")
    gdf_vote.plot(
        ax=ax,
        column="ratio_LR",
        cmap="bwr_r",
        vmin=-0.9,
        vmax=0.9,
        edgecolor="black",
        linewidth=0.1,
        legend=True,
    )
    ax.axis("off")
    fig.savefig(FOLDERPLOT + "Paris_vote_2020_LR.png", dpi=DPI)
    gdf_metro = gpd.read_file(FOLDER_DATA + "idf_metro.gpkg")
    fig, ax = plt.subplots(layout="constrained")
    gpd.GeoDataFrame(geometry=[gdf_vote.union_all()], crs=gdf_vote.crs).boundary.plot(
        ax=ax, edgecolor="black", linewidth=1
    )
    gdf_metro.plot(ax=ax, color="red", markersize=5, linewidth=0.1)
    ax.axis("off")
    fig.savefig(FOLDERPLOT + "Paris_simplified_metro.png", dpi=DPI)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
Plot paris bicycle network plan progress with lines.
"""

import geopandas as gpd
import matplotlib.pyplot as plt

END_CMAP = 0.75
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
STATE_COLOR = {
    "Built before 2021": "darkgrey",
    "Not built yet": plt.get_cmap("viridis")(0),
    "Built": plt.get_cmap("viridis")(END_CMAP),
}
DPI = 250


# TODO add legend
# TODO find better colors coherent with viridis
def main():
    gdf_arr = gpd.read_file(FOLDER_ARR + "paris_vote_arr_2020_bikenet.gpkg")
    # Plot bicycle plan progress over arrondissement
    gdf_bikenet = gpd.read_file(FOLDER_BIKE + "bikenet_paris_2026_01_28.json")
    gdf_bikenet = gdf_bikenet.set_crs(epsg=4326)
    gdf_bikenet = gdf_bikenet.to_crs(gdf_arr.crs)
    gdf_bikenet["Etat"] = gdf_bikenet["Etat"].map(STATE_MAP)
    gdf_bikenet["color"] = gdf_bikenet["Etat"].map(STATE_COLOR)
    fig, ax = plt.subplots(figsize=[11.69, 8.27], layout="constrained")
    gdf_bikenet.plot(ax=ax, color=gdf_bikenet["color"], linewidth=2)
    gdf_arr.plot(ax=ax, color="whitesmoke", edgecolor="white", linewidth=5)
    ax.axis("off")
    fig.savefig(FOLDERPLOT + "map_bikeplan_roads.jpeg", dpi=DPI)


if __name__ == "__main__":
    main()

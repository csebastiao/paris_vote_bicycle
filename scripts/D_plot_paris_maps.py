# -*- coding: utf-8 -*-
"""
Plot paris official data.
"""

import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib_map_utils.core.scale_bar import scale_bar


FOLDER_ARR = "./data/processed/"
FOLDER_BIKE = "./data/raw/"
FOLDERPLOT = "./plots/"
PLOT_COLS = {
    "median_income": "RdYlGn",
    "share_commuter_cyclist": "Greens",
    "share_commuter_driver": "Reds",
    "Left_wing_share": "Reds",
    "Right_wing_share": "Blues",
    "ratio_LR": "bwr_r",
    "length_accomplished_share": "Greys",
    "length_before_2021": "RdYlGn",
    "length_before_2021_norm": "RdYlGn",
    "length_planned": "RdYlGn",
    "length_planned_norm": "RdYlGn",
    "length_built": "RdYlGn",
    "length_built_norm": "RdYlGn",
}
STATE_MAP = {
    "Pas d'aménagement": "Not built yet",
    "Provisoire ou coronapiste": "Not built yet",
    "Réalisé Pré-2021": "Built before 2021",
    "Réalisé dans le Plan Vélo": "Built",
    "Hors Plan Vélo (Embellir)": "Built",
    "Annoncé réalisé": "Built",
}
STATE_COLOR = {
    "Built before 2021": "gray",
    "Not built yet": "red",
    "Built": "green",
}
DPI = 250


# TODO make json file for parameters
# TODO add legend
# TODO add minimalist basemap for bikenet?
# TODO switch to km
# TODO add white boundaries to "explode" the borough fo
# TODO add very very light grey to Paris boundaries with white boundaries for bikeplan
# TODO add numbers of arrondissements in dark and light grey on maps
# TODO built before 2021 make thinner and choose pink or some else
def main():
    gdf_arr = gpd.read_file(FOLDER_ARR + "paris_vote_arr_2020_bikenet.gpkg")
    # Plot choropleth maps
    for column_name, cmap in PLOT_COLS.items():
        fig, ax = plt.subplots(figsize=[11.69, 8.27], layout="constrained")
        if column_name == "ratio_LR":
            kwargs = {"vmin": -0.6, "vmax": 0.6, "legend_kwds": {"shrink": 0.75}}
        else:
            kwargs = {"legend_kwds": {"shrink": 0.75}}
        gdf_arr.plot(ax=ax, column=column_name, cmap=cmap, legend=True, **kwargs)
        scale_bar(
            ax,
            location="lower left",
            style="boxes",
            bar={"projection": gdf_arr.crs, "unit": "km"},
            labels={"style": "first_last"},
        )
        ax.axis("off")
        ax.get_tightbbox()
        fig.savefig(FOLDERPLOT + "Paris_" + column_name + ".jpeg", dpi=DPI)
    # Plot bicycle plan progress over arrondissement
    gdf_bikenet = gpd.read_file(FOLDER_BIKE + "bikenet_paris_2026_01_28.json")
    gdf_bikenet = gdf_bikenet.set_crs(epsg=4326)
    gdf_bikenet = gdf_bikenet.to_crs(gdf_arr.crs)
    gdf_bikenet["Etat"] = gdf_bikenet["Etat"].map(STATE_MAP)
    gdf_bikenet["color"] = gdf_bikenet["Etat"].map(STATE_COLOR)
    fig, ax = plt.subplots(figsize=[11.69, 8.27], layout="constrained")
    gdf_bikenet.plot(ax=ax, color=gdf_bikenet["color"], linewidth=2)
    ax.axis("off")
    scale_bar(
        ax,
        location="lower left",
        style="boxes",
        bar={"projection": gdf_arr.crs, "unit": "km"},
        labels={"style": "first_last"},
    )
    ax.get_tightbbox()
    fig.savefig(FOLDERPLOT + "Paris_bikeplan.jpeg", dpi=DPI)


if __name__ == "__main__":
    main()

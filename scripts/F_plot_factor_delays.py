# -*- coding: utf-8 -*-
"""
Plot results.
"""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib_map_utils.core.scale_bar import scale_bar
import geopandas as gpd
import statsmodels.api as sm

FOLDEROOTS = "./data/processed/"
FOLDERPLOT = "./plots/"


# TODO add number of arrondissement inside the choropleth map
# TODO make scatter points look better
def main():
    with open("./scripts/F_plot_factor_delays.json", "r") as f:
        plot_params = json.load(f)
    for key in plot_params["rcparams"]:
        mpl.rcParams[key] = plot_params["rcparams"][key]
    gdf_arr = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    mean_acc = gdf_arr["length_accomplished_share"].mean()
    for idx, column in enumerate(plot_params["column"]):
        # Estimate linear regression
        model = sm.OLS(
            gdf_arr["length_accomplished_share"],
            sm.add_constant(gdf_arr[column].values),
        ).fit(cov_type="HC3")
        # Plot arrondissements
        fig, ax = plt.subplots(figsize=plot_params["figsize"])
        ax.spines[["right", "top"]].set_visible(False)
        ax.scatter(
            gdf_arr[column],
            gdf_arr["length_accomplished_share"],
            s=plot_params["s"][idx],
            color=plot_params["color"][idx],
            zorder=2,
        )
        for i in range(len(gdf_arr)):
            ax.annotate(
                gdf_arr["NUM_ARROND"].values[i],
                (
                    gdf_arr[column].values[i],
                    gdf_arr["length_accomplished_share"].values[i],
                ),
                fontweight="bold",
                color="white",
                ha="center",
                va="center",
            )
        # Add expected value lines
        ax.plot(
            [-1, 99999],
            [mean_acc, mean_acc],
            linestyle="dashed",
            color="#E1E1E1",
            zorder=0,
        )
        if column != "ratio_LR":
            mean_share = gdf_arr[column].mean()
        else:
            mean_share = 0
        ax.plot(
            [mean_share, mean_share],
            [0, 1],
            linestyle="dashed",
            color="#E1E1E1",
            zorder=0,
        )
        xx = np.linspace(
            gdf_arr[column].min() - 0.05, gdf_arr[column].max() + 0.05, num=100
        )
        ax.plot(
            xx,
            model.params["x1"] * xx + model.params["const"],
            color="#000000",
            linewidth=2,
            zorder=1,
        )
        ax.set_ylabel("Share of bicycle lanes accomplished")
        ax.set_xlabel(plot_params["xlabel"][idx])
        ax.set_xlim(plot_params["xlim"][idx])
        ax.set_ylim([0, 1])
        # Add as an inset the choropleth map of the factor
        cax = ax.inset_axes([plot_params["inset_x"][idx], 0.5, 0.5, 0.5])
        gcax = cax.inset_axes([0.82, 0.42, 0.03, 0.45])
        kwargs = {
            "vmin": 0,
            "vmax": 1,
            "legend_kwds": {
                "cax": gcax,
                "format": mtick.PercentFormatter(1),
                "ticks": [0.0, 0.25, 0.5, 0.75, 1.0],
            },
        }
        cax.text(
            x=0.835,
            y=0.91,
            transform=cax.transAxes,
            s=plot_params["colorbar_label"][idx],
            fontsize=10,
            va="center",
            ha="center",
        )
        gdf_arr.plot(
            ax=cax,
            column=column,
            cmap=plot_params["cmap"][idx],
            legend=True,
            edgecolor="white",
            linewidth=2,
            **kwargs,
        )
        scale_bar(
            cax,
            location="lower left",
            style="ticks",
            bar={
                "projection": gdf_arr.crs,
                "unit": "km",
                "major_mult": 1,
                "major_div": 3,
            },
            labels={"style": "first_last"},
        )
        gcax.tick_params(labelsize=7)
        cax.xaxis.set_major_locator(mtick.NullLocator())
        cax.yaxis.set_major_locator(mtick.NullLocator())
        fig.savefig(FOLDERPLOT + f"scatterplot_{column}.jpeg")


if __name__ == "__main__":
    main()

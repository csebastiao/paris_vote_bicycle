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
INSET_NUMBER_SIZE = 5
MAIN_NUMBER_SIZE = 8


def main():
    with open("./scripts/E_plot_factor_delays.json", "r") as f:
        plot_params = json.load(f)
    for key in plot_params["rcparams"]:
        mpl.rcParams[key] = plot_params["rcparams"][key]
    gdf_arr = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    mean_acc = gdf_arr["length_accomplished_share"].mean()
    fig, axs = plt.subplots(
        ncols=2,
        sharey="all",
        figsize=plot_params["figsize"],
    )
    for idx, column in enumerate(plot_params["column"]):
        # Estimate linear regression
        model = sm.OLS(
            gdf_arr["length_accomplished_share"],
            sm.add_constant(gdf_arr[column].values),
        ).fit(cov_type="HC3")
        # Plot arrondissements
        axs[idx].spines[["right", "top"]].set_visible(False)
        axs[idx].scatter(
            gdf_arr[column],
            gdf_arr["length_accomplished_share"],
            s=plot_params["s"][idx],
            color=plot_params["color"][idx],
            zorder=2,
        )
        # Add arrondissement number for each dot
        if column == "Right_wing_share":
            for i in range(len(gdf_arr)):
                if gdf_arr["NUM_ARROND"].values[i] == 1:
                    axs[idx].annotate(
                        "C",
                        (
                            gdf_arr[column].values[i],
                            gdf_arr["length_accomplished_share"].values[i],
                        ),
                        fontsize=MAIN_NUMBER_SIZE,
                        fontweight=900,
                        color="white",
                        ha="center",
                        va="center",
                    )
                elif gdf_arr["NUM_ARROND"].values[i] == 11:
                    axs[idx].annotate(
                        gdf_arr["NUM_ARROND"].values[i],
                        (
                            gdf_arr[column].values[i],
                            gdf_arr["length_accomplished_share"].values[i],
                        ),
                        textcoords="offset points",
                        xytext=(18, -15),
                        arrowprops=dict(arrowstyle="-"),
                        fontweight=900,
                        fontsize=MAIN_NUMBER_SIZE,
                        color="black",
                        ha="center",
                        va="center",
                    )
                elif gdf_arr["NUM_ARROND"].values[i] == 19:
                    axs[idx].annotate(
                        gdf_arr["NUM_ARROND"].values[i],
                        (
                            gdf_arr[column].values[i],
                            gdf_arr["length_accomplished_share"].values[i],
                        ),
                        textcoords="offset points",
                        xytext=(-18, 15),
                        arrowprops=dict(arrowstyle="-"),
                        fontweight=900,
                        fontsize=MAIN_NUMBER_SIZE,
                        color="black",
                        ha="center",
                        va="center",
                    )
                else:
                    axs[idx].annotate(
                        gdf_arr["NUM_ARROND"].values[i],
                        (
                            gdf_arr[column].values[i],
                            gdf_arr["length_accomplished_share"].values[i],
                        ),
                        fontweight=900,
                        fontsize=MAIN_NUMBER_SIZE,
                        color="white",
                        ha="center",
                        va="center",
                    )
        else:
            axs[idx].set_ylabel("Share of bicycle lanes accomplished")
            for i in range(len(gdf_arr)):
                if gdf_arr["NUM_ARROND"].values[i] == 1:
                    text = "C"
                else:
                    text = gdf_arr["NUM_ARROND"].values[i]
                axs[idx].annotate(
                    text,
                    (
                        gdf_arr[column].values[i],
                        gdf_arr["length_accomplished_share"].values[i],
                    ),
                    fontweight=900,
                    fontsize=MAIN_NUMBER_SIZE,
                    color="white",
                    ha="center",
                    va="center",
                )
        # Add expected value lines
        axs[idx].plot(
            [-1, 99999],
            [mean_acc, mean_acc],
            linestyle="dashed",
            color="#E1E1E1",
            zorder=0,
        )
        mean_share = gdf_arr[column].mean()
        axs[idx].plot(
            [mean_share, mean_share],
            [0, 1],
            linestyle="dashed",
            color="#E1E1E1",
            zorder=0,
        )
        xx = np.linspace(
            gdf_arr[column].min() - 0.05, gdf_arr[column].max() + 0.05, num=100
        )
        axs[idx].plot(
            xx,
            model.params["x1"] * xx + model.params["const"],
            color="#000000",
            linewidth=2,
            zorder=1,
        )

        axs[idx].set_xlabel(plot_params["xlabel"][idx])
        axs[idx].set_xlim(plot_params["xlim"][idx])
        axs[idx].set_ylim([0, 1])
        axs[idx].set_aspect("equal")
        # Add as an inset the choropleth map of the factor
        cax = axs[idx].inset_axes([plot_params["inset_x"][idx], 0.65, 0.8, 0.4])
        gcax = cax.inset_axes([0.82, 0.42, 0.03, 0.45])
        vmax = plot_params["xlim"][idx][-1]
        kwargs = {
            "vmin": 0,
            "vmax": vmax,
            "legend_kwds": {
                "cax": gcax,
                "format": mtick.PercentFormatter(1),
                "ticks": [0, vmax / 2, vmax],
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
        if idx == 0:
            scale_bar(
                cax,
                location="lower left",
                style="ticks",
                bar={
                    "projection": gdf_arr.crs,
                    "unit": "km",
                    "major_mult": 1,
                    "major_div": 3,
                    "tickwidth": 1,
                    "height": 0.03,
                },
                labels={
                    "style": "first_last",
                    "fontsize": INSET_NUMBER_SIZE,
                    "sep": 0.1,
                },
                units={"fontsize": INSET_NUMBER_SIZE, "fontweight": "normal"},
            )
        gcax.tick_params(labelsize=INSET_NUMBER_SIZE)
        # Add arrondissement number
        rep_point = gdf_arr.geometry.representative_point()
        arrs = gdf_arr["NUM_ARROND"].values
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
                xx = rep_point[i].xy[0][0] - 4000
                yy = rep_point[i].xy[1][0] + 500
                text = arrs[i]
            elif arrs[i] == 13:
                xx = rep_point[i].xy[0][0] - 200
                yy = rep_point[i].xy[1][0] - 100
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
                xx = rep_point[i].xy[0][0]
                yy = rep_point[i].xy[1][0]
                text = arrs[i]
            cax.text(
                x=xx,
                y=yy,
                s=text,
                color="white",
                fontweight="bold",
                ha="center",
                va="center",
                fontsize=MAIN_NUMBER_SIZE,
            )
        cax.axis("off")
    fig.subplots_adjust(wspace=0.15)
    fig.savefig(FOLDERPLOT + "scatterplot_delays.jpeg", bbox_inches="tight")


if __name__ == "__main__":
    main()

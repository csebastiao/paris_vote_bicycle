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
        2, 2, sharey="row", figsize=plot_params["figsize"], height_ratios=[0.3, 0.7]
    )
    for idx, column in enumerate(plot_params["column"]):
        # Estimate linear regression
        model = sm.OLS(
            gdf_arr["length_accomplished_share"],
            sm.add_constant(gdf_arr[column].values),
        ).fit(cov_type="HC3")
        # Plot arrondissements
        axs[1][idx].spines[["right", "top"]].set_visible(False)
        axs[1][idx].scatter(
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
                    axs[1][idx].annotate(
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
                    axs[1][idx].annotate(
                        gdf_arr["NUM_ARROND"].values[i],
                        (
                            gdf_arr[column].values[i],
                            gdf_arr["length_accomplished_share"].values[i],
                        ),
                        textcoords="offset points",
                        xytext=(21, -18),
                        arrowprops=dict(arrowstyle="-"),
                        fontweight=900,
                        fontsize=MAIN_NUMBER_SIZE,
                        color="black",
                        ha="center",
                        va="center",
                    )
                elif gdf_arr["NUM_ARROND"].values[i] == 19:
                    axs[1][idx].annotate(
                        gdf_arr["NUM_ARROND"].values[i],
                        (
                            gdf_arr[column].values[i],
                            gdf_arr["length_accomplished_share"].values[i],
                        ),
                        textcoords="offset points",
                        xytext=(-22, 17),
                        arrowprops=dict(arrowstyle="-"),
                        fontweight=900,
                        fontsize=MAIN_NUMBER_SIZE,
                        color="black",
                        ha="center",
                        va="center",
                    )
                else:
                    axs[1][idx].annotate(
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
            axs[1][idx].set_ylabel("Share of bicycle lanes accomplished")
            for i in range(len(gdf_arr)):
                if gdf_arr["NUM_ARROND"].values[i] == 1:
                    text = "C"
                else:
                    text = gdf_arr["NUM_ARROND"].values[i]
                axs[1][idx].annotate(
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
        axs[1][idx].plot(
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
        axs[1][idx].plot(
            [mean_share, mean_share],
            [0, 1],
            linestyle="dashed",
            color="#E1E1E1",
            zorder=0,
        )
        xx = np.linspace(
            gdf_arr[column].min() - 0.05, gdf_arr[column].max() + 0.05, num=100
        )
        axs[1][idx].plot(
            xx,
            model.params["x1"] * xx + model.params["const"],
            color="#000000",
            linewidth=2,
            zorder=1,
        )

        axs[1][idx].set_xlabel(plot_params["xlabel"][idx])
        axs[1][idx].set_xlim(plot_params["xlim"][idx])
        axs[1][idx].set_ylim([0, 1])
        axs[1][idx].set_aspect("equal")
        # Add as an inset the choropleth map of the factor
        gcax = axs[0][idx].inset_axes([0.82, 0.42, 0.03, 0.45])
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
        axs[0][idx].text(
            x=0.835,
            y=0.91,
            transform=axs[0][idx].transAxes,
            s=plot_params["colorbar_label"][idx],
            fontsize=10,
            va="center",
            ha="center",
        )
        gdf_arr.plot(
            ax=axs[0][idx],
            column=column,
            cmap=plot_params["cmap"][idx],
            legend=True,
            edgecolor="white",
            linewidth=2,
            **kwargs,
        )
        if idx == 0:
            scale_bar(
                axs[0][idx],
                location="upper left",
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
            axs[0][idx].text(
                x=xx,
                y=yy,
                s=text,
                color="white",
                fontweight="bold",
                ha="center",
                va="center",
                fontsize=MAIN_NUMBER_SIZE,
            )
        axs[0][idx].axis("off")
    fig.subplots_adjust(wspace=-0.45, hspace=0)
    fig.savefig(FOLDERPLOT + "scatterplot_delays.jpeg", bbox_inches="tight")


if __name__ == "__main__":
    main()

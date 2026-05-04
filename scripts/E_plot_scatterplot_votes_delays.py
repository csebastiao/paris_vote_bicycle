# -*- coding: utf-8 -*-
"""
Plot results.
"""

import json
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import geopandas as gpd
import statsmodels.api as sm

FOLDEROOTS = "./data/processed/"
FOLDERPLOT = "./plots/"


# TODO put number in center of dot in matplotlib and put only dot as markers
# TODO put inset for Left and Right the choropleth maps
def main():
    with open("./scripts/E_plot_scatterplot_votes_delays.json", "r") as f:
        plot_params = json.load(f)
    for key in plot_params["rcparams"]:
        mpl.rcParams[key] = plot_params["rcparams"][key]
    gdf_vote = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    mean_acc = gdf_vote["length_accomplished_share"].mean()
    for numbered in [True, False]:
        for idx, column in enumerate(plot_params["column"]):
            # Estimate linear regression
            model = sm.OLS(
                gdf_vote["length_accomplished_share"],
                sm.add_constant(gdf_vote[column].values),
            ).fit(cov_type="HC3")
            # Plot arrondissements
            fig, ax = plt.subplots(figsize=plot_params["figsize"])
            ax.scatter(
                gdf_vote[column],
                gdf_vote["length_accomplished_share"],
                **{
                    key: val[idx]
                    for key, val in plot_params.items()
                    if key
                    not in [
                        "figsize",
                        "rcparams",
                        "column",
                        "xlabel",
                        "xlim",
                    ]
                },
                label="Arrondissements",
                zorder=2,
            )
            if numbered:
                for i in range(len(gdf_vote)):
                    ax.annotate(
                        gdf_vote["NUM_ARROND"].values[i],
                        (
                            gdf_vote[column].values[i],
                            gdf_vote["length_accomplished_share"].values[i],
                        ),
                        xytext=(20, 20),
                        textcoords="offset pixels",
                    )
            # Add expected value lines
            ax.plot(
                [-1, 99999],
                [mean_acc, mean_acc],
                linestyle="dashed",
                color="#E1E1E1",
                zorder=0,
                label="Expected value",
            )
            if column != "ratio_LR":
                mean_share = gdf_vote[column].mean()
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
                gdf_vote[column].min() - 0.05, gdf_vote[column].max() + 0.05, num=100
            )
            ax.plot(
                xx,
                model.params["x1"] * xx + model.params["const"],
                color="#000000",
                label="Linear regression",
                linewidth=2,
                zorder=1,
            )
            # Add linear regression parameters
            ax.text(
                x=0.6,
                y=0.85,
                transform=ax.transAxes,
                s=f"$R^2$={round(model.rsquared, 3)}, slope={round(model.params['x1'], 3)}, p-value={round(model.pvalues['x1'], 5)}",
                fontsize=13,
            )
            ax.set_ylabel("Share of bicycle lanes accomplished")
            ax.set_xlabel(plot_params["xlabel"][idx])
            ax.set_xlim(plot_params["xlim"][idx])
            ax.set_ylim([0, 1])
            ax.legend()
            filename = f"scatterplot_delays_{column}"
            if numbered:
                filename += "_numbered"
            fig.savefig(FOLDERPLOT + filename + ".jpeg")


if __name__ == "__main__":
    main()

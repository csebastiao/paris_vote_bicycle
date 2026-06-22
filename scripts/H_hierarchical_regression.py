# -*- coding: utf-8 -*-
"""
Compute correlation and linear regression results table.
"""

import geopandas as gpd
import statsmodels.api as sm

FOLDEROOTS = "./data/processed/"
ALL_COLS = [
    "median_income",
    "mean_age",
    "share_commuter_cyclist",
    "share_commuter_driver",
    "Right_wing_share",
]


def main():
    gdf_arr = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    for column in ["median_income", "mean_age"]:
        gdf_arr[column] = (gdf_arr[column] - gdf_arr[column].min()) / (
            gdf_arr[column].max() - gdf_arr[column].min()
        )
    # Compute for all other variables together
    model_full = sm.OLS(
        gdf_arr["length_accomplished_share"],
        sm.add_constant(gdf_arr[ALL_COLS]),
    ).fit()
    print("Full model:", model_full.summary())
    res = []
    for col in ALL_COLS:
        cols_baseline = ALL_COLS.copy()
        cols_baseline.remove(col)
        model_baseline = sm.OLS(
            gdf_arr["length_accomplished_share"],
            sm.add_constant(gdf_arr[cols_baseline]),
        ).fit()
        print("Baseline for", col, model_baseline.summary())
        print(
            "Difference:",
            model_full.rsquared - model_baseline.rsquared,
            model_baseline.ssr - model_full.ssr,
        )
        res.append(
            [
                col,
                model_full.rsquared - model_baseline.rsquared,
                model_baseline.ssr - model_full.ssr,
            ]
        )
    print(res)


if __name__ == "__main__":
    main()

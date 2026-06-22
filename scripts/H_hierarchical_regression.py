# -*- coding: utf-8 -*-
"""
Compute correlation and linear regression results table.
"""

import geopandas as gpd
import statsmodels.api as sm

FOLDEROOTS = "./data/processed/"
BASELINE_COLS = [
    "median_income",
    "mean_age",
    "share_commuter_cyclist",
    "share_commuter_driver",
]


def main():
    gdf_arr = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    for column in ["median_income", "mean_age"]:
        gdf_arr[column] = (gdf_arr[column] - gdf_arr[column].min()) / (
            gdf_arr[column].max() - gdf_arr[column].min()
        )
    # Compute for all other variables together
    model_baseline = sm.OLS(
        gdf_arr["length_accomplished_share"], sm.add_constant(gdf_arr[BASELINE_COLS])
    ).fit()
    print("Baseline:", model_baseline.summary())
    for vote_col in ["Right_wing_share", "Left_wing_share"]:
        model_full = sm.OLS(
            gdf_arr["length_accomplished_share"],
            sm.add_constant(gdf_arr[BASELINE_COLS + [vote_col]]),
        ).fit()
        print("With ", vote_col, model_full.summary())
        print(
            "Difference:",
            model_full.rsquared - model_baseline.rsquared,
            model_baseline.ssr - model_full.ssr,
        )


if __name__ == "__main__":
    main()

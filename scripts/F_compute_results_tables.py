# -*- coding: utf-8 -*-
"""
Compute correlation and linear regression results table.
"""

import pandas as pd
import geopandas as gpd
import statsmodels.api as sm

FOLDEROOTS = "./data/processed/"
CORR_COLS = [
    "Left_wing_share",
    "Right_wing_share",
    "median_income",
    "share_commuter_cyclist",
    "share_commuter_driver",
    # Put last to exclude from linear regression table
    "length_before_2021_norm",
    "length_accomplished_share",
]


def main():
    gdf_vote = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    # Compute linear regression table
    lr_dict = {}
    for column in CORR_COLS[:-2]:
        if column == "median_income":
            gdf_vote[column] = (gdf_vote[column] - gdf_vote[column].min()) / (
                gdf_vote[column].max() - gdf_vote[column].min()
            )
        model = sm.OLS(
            gdf_vote["length_accomplished_share"],
            sm.add_constant(gdf_vote[column].values),
        ).fit(cov_type="HC3")
        lr_dict[column] = [
            model.rsquared,
            model.params["x1"],
            model.pvalues["x1"],
            model.params["const"],
            model.pvalues["const"],
        ]
    df_lr = pd.DataFrame.from_dict(
        lr_dict,
        orient="index",
        columns=["R2", "slope_val", "slope_pval", "const_val", "const_pval"],
    )
    df_lr.to_json(FOLDEROOTS + "linear_regression_results.json")
    # Compute correlation matrix
    df_corr = gdf_vote[CORR_COLS].corr()
    df_corr.to_json(FOLDEROOTS + "correlation_matrix.json")


if __name__ == "__main__":
    main()

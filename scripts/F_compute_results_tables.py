# -*- coding: utf-8 -*-
"""
Compute correlation and linear regression results table.
"""

import pandas as pd
import geopandas as gpd
import statsmodels.api as sm
from scipy.stats import pearsonr

FOLDEROOTS = "./data/processed/"
CORR_COLS = [
    "Left_wing_share",
    "Right_wing_share",
    "median_income",
    "share_commuter_cyclist",
    "share_commuter_driver",
    "length_before_2021_norm",
    "length_accomplished_share",  # Put last to exclude from linear regression table
]


def main():
    gdf_arr = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    # Compute linear regression table
    lr_dict = {}
    for column in CORR_COLS[:-1]:
        if column == "median_income":
            gdf_arr[column] = (gdf_arr[column] - gdf_arr[column].min()) / (
                gdf_arr[column].max() - gdf_arr[column].min()
            )
        model = sm.OLS(
            gdf_arr["length_accomplished_share"],
            sm.add_constant(gdf_arr[column].values),
        ).fit(cov_type="HC3")
        lr_dict[column] = [
            round(model.rsquared, 3),
            round(model.params["x1"], 3),
            round(model.pvalues["x1"], 5),
            round(model.params["const"], 3),
            round(model.pvalues["const"], 5),
        ]
    df_lr = pd.DataFrame.from_dict(
        lr_dict,
        orient="index",
        columns=["R2", "slope_val", "slope_pval", "const_val", "const_pval"],
    )
    df_lr.to_json(FOLDEROOTS + "linear_regression_results.json")
    # Compute correlation matrix
    corr = [
        [
            pearsonr(gdf_arr[CORR_COLS[i]], gdf_arr[CORR_COLS[j]])
            for j in range(len(CORR_COLS))
        ]
        for i in range(len(CORR_COLS))
    ]
    df_corr = pd.DataFrame(corr, index=CORR_COLS, columns=CORR_COLS)
    df_corr = df_corr.map(lambda x: (round(x[0], 3), round(x[1], 5)))
    df_corr.to_json(FOLDEROOTS + "correlation_matrix.json")


if __name__ == "__main__":
    main()

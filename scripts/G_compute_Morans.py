# -*- coding: utf-8 -*-
"""
Compute Moran's I for all metrics.
"""

from esda.moran import Moran
import geopandas as gpd
from libpysal import weights
import pandas as pd

FOLDEROOTS = "./data/processed/"
MORAN_COLS = [
    "Left_wing_share",
    "Right_wing_share",
    "median_income",
    "share_commuter_cyclist",
    "share_commuter_driver",
    "length_before_2021_norm",
    "length_accomplished_share",
]


def main():
    gdf_vote = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    w = weights.Queen.from_dataframe(gdf_vote, use_index=False)
    morans = [
        (Moran(gdf_vote[col], w).I, Moran(gdf_vote[col], w).p_sim) for col in MORAN_COLS
    ]
    df_corr = pd.DataFrame(morans, index=MORAN_COLS, columns=["I", "pval"])
    df_corr.to_json(FOLDEROOTS + "morans.json")


if __name__ == "__main__":
    main()

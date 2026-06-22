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
    "mean_age",
    "share_commuter_cyclist",
    "share_commuter_driver",
    "length_accomplished_share",
]


def main():
    gdf_arr = gpd.read_file(FOLDEROOTS + "paris_vote_arr_2020_bikenet.gpkg")
    w = weights.Rook.from_dataframe(gdf_arr, use_index=False)
    morans = [
        (
            round(Moran(gdf_arr[col], w).I, 3),
            round(Moran(gdf_arr[col], w).p_sim, 5),
        )
        for col in MORAN_COLS
    ]
    df_moran = pd.DataFrame(morans, index=MORAN_COLS, columns=["I", "pval"])
    df_moran.to_json(FOLDEROOTS + "morans.json")


if __name__ == "__main__":
    main()

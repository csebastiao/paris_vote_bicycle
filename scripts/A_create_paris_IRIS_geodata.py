# -*- coding: utf-8 -*-
"""
Create processed IRIS data from raw files in Paris.
"""

import os
import numpy as np
import pandas as pd
from libpysal import weights
import geopandas as gpd

FOLDER_IN = "./data/raw/official_data/"
FOLDER_OUT = "./data/processed/paris_official_data/"
MET_LIST = [
    "median_income",
    "share_commuter_cyclist",
    "share_commuter_driver",
]


def main():
    if not os.path.exists(FOLDER_OUT):
        os.makedirs(FOLDER_OUT)
    # Load all the statistical data
    df_iris_pop = pd.read_csv(
        FOLDER_IN + "IRIS_population_2021/base-ic-evol-struct-pop-2021.CSV",
        delimiter=";",
        low_memory=False,
    )
    df_iris_pop = df_iris_pop.rename({"IRIS": "CODE_IRIS"}, axis=1)
    df_iris_income = pd.read_csv(
        FOLDER_IN + "IRIS_income_2021/BASE_TD_FILO_IRIS_2021_DISP.csv",
        delimiter=";",
        low_memory=False,
    )
    df_iris_income = df_iris_income.rename({"IRIS": "CODE_IRIS"}, axis=1)
    df_iris_activity = pd.read_csv(
        FOLDER_IN + "IRIS_activity_2021/base-ic-activite-residents-2021.CSV",
        delimiter=";",
        low_memory=False,
    )
    df_iris_activity = df_iris_activity.rename({"IRIS": "CODE_IRIS"}, axis=1)
    # Load the spatial data
    gdf_iris = gpd.read_file(
        FOLDER_IN
        + "IRIS_geometry_2021/IRIS-GE/1_DONNEES_LIVRAISON_2021-06-00135/IRIS-GE_2-0_SHP_LAMB93_FXX-2021/IRIS_GE.SHP"
    )
    gdf_iris = gdf_iris.to_crs(epsg=4326)
    # Keep only the IRIS in Paris
    gdf_iris["dep"] = gdf_iris["CODE_IRIS"].apply(lambda x: str(x)[:2])
    gdf_paris_iris = gdf_iris[gdf_iris["dep"] == "75"]
    gdf_paris_iris = gdf_paris_iris[["CODE_IRIS", "geometry"]]
    # Join the statistical and spatial data
    gdf_paris_iris = gdf_paris_iris.merge(df_iris_pop, on="CODE_IRIS")
    gdf_paris_iris = gdf_paris_iris.to_crs(gdf_paris_iris.estimate_utm_crs())
    gdf_paris_iris["pop_density"] = gdf_paris_iris.apply(
        lambda df: df.P21_POP / (df.geometry.area / 10**6), axis=1
    )
    gdf_paris_iris = gdf_paris_iris.to_crs(epsg=4326)
    gdf_paris_iris = gdf_paris_iris.merge(df_iris_income, on="CODE_IRIS")
    gdf_paris_iris = gdf_paris_iris.merge(df_iris_activity, on="CODE_IRIS")
    gdf_paris_iris.to_file(FOLDER_OUT + "paris_dem_iris_2021.gpkg")
    # Keep only relevant columns
    gdf_condensed = gdf_paris_iris[
        [
            "CODE_IRIS",
            "P21_POP",
            "pop_density",
            "C21_ACTOCC15P",
            "C21_ACTOCC15P_VELO",
            "C21_ACTOCC15P_VOIT",
            "DISP_MED21",
            "geometry",
        ]
    ]
    # Clean string data with French decimal
    gdf_condensed["DISP_MED21"] = gdf_condensed["DISP_MED21"].apply(
        lambda x: np.nan if "n" in x else int(float(x.replace(",", ".")))
    )
    gdf_condensed["share_commuter_cyclist"] = (
        gdf_condensed.C21_ACTOCC15P_VELO / gdf_condensed.C21_ACTOCC15P
    )
    gdf_condensed["share_commuter_driver"] = (
        gdf_condensed.C21_ACTOCC15P_VOIT / gdf_condensed.C21_ACTOCC15P
    )
    gdf_condensed = gdf_condensed.rename(
        {
            "P21_POP": "pop",
            "DISP_MED21": "median_income",
        },
        axis=1,
    )
    gdf_condensed = gdf_condensed.drop(
        ["C21_ACTOCC15P_VELO", "C21_ACTOCC15P_VOIT", "C21_ACTOCC15P"], axis=1
    )
    gdf_condensed.to_file(FOLDER_OUT + "paris_dem_iris_2021_condensed.gpkg")
    # Replace na values for columns in MET_LIST by the average values of the k nearest neighbors with values
    gdf_condensed_na = gdf_condensed[gdf_condensed["median_income"].isna()]
    gdf_condensed_notna = gdf_condensed[gdf_condensed["median_income"].notna()]
    change_dict = {met: {} for met in MET_LIST}
    for idx, row in gdf_condensed_na.iterrows():
        gdf_iris_temp = gdf_condensed_notna.copy()
        gdf_iris_temp.loc[-1] = row
        W = weights.KNN.from_dataframe(gdf_iris_temp, use_index=True, k=8)
        W.transform = "r"
        for met in MET_LIST:
            change_dict[met][idx] = weights.lag_spatial(
                W, gdf_iris_temp[met].fillna(0).values
            )[-1]
    for met in MET_LIST:
        gdf_condensed[met] = gdf_condensed[met].fillna(change_dict[met])
    gdf_condensed["median_income"] = gdf_condensed["median_income"].map(round)
    gdf_condensed.to_file(FOLDER_OUT + "paris_dem_iris_2021_condensed_filledna.gpkg")


if __name__ == "__main__":
    main()

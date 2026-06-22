# -*- coding: utf-8 -*-
"""
Create processed IRIS data from raw files in Paris.
"""

import os
import numpy as np
import pandas as pd
import geopandas as gpd

FOLDER_IN = "./data/raw/official_data/"
FOLDER_OUT = "./data/processed/paris_official_data/"


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
    # Keep only relevant columns
    gdf_condensed = gdf_paris_iris[
        [
            "CODE_IRIS",
            "P21_POP",
            "pop_density",
            "P21_POP0002",
            "P21_POP0305",
            "P21_POP0610",
            "P21_POP1117",
            "P21_POP1824",
            "P21_POP2539",
            "P21_POP4054",
            "P21_POP5564_x",  # Because 2 similar columns found while merging all iris data
            "P21_POP6579",
            "P21_POP80P",
            "C21_ACTOCC15P",
            "C21_ACTOCC15P_VELO",
            "C21_ACTOCC15P_VOIT",
            "DISP_MED21",
            "geometry",
        ]
    ]
    gdf_condensed["mean_age"] = gdf_condensed.apply(
        get_mean_age,
        axis=1,
    )
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
        [
            "C21_ACTOCC15P_VELO",
            "C21_ACTOCC15P_VOIT",
            "C21_ACTOCC15P",
            "P21_POP0002",
            "P21_POP0305",
            "P21_POP0610",
            "P21_POP1117",
            "P21_POP1824",
            "P21_POP2539",
            "P21_POP4054",
            "P21_POP5564_x",
            "P21_POP6579",
            "P21_POP80P",
        ],
        axis=1,
    )
    gdf_condensed["NUM_ARROND"] = gdf_condensed["CODE_IRIS"].apply(
        lambda x: int(x[3:5])
    )
    gdf_condensed.to_file(FOLDER_OUT + "paris_dem_iris_2021.gpkg")
    gdf_arr = gdf_condensed.copy()
    # Merge arrondissement 1 to 4
    gdf_arr["NUM_ARROND"] = gdf_arr["NUM_ARROND"].apply(lambda x: x if x > 4 else 1)
    # Do weighted average by population
    col_to_wavg = [
        "median_income",
        "mean_age",
        "share_commuter_cyclist",
        "share_commuter_driver",
    ]
    for col in col_to_wavg:
        gdf_arr[col] = gdf_arr[col] * gdf_arr["pop"]
        gdf_arr["num_poly_" + col] = gdf_arr[col].apply(
            lambda x: 1 if pd.notna(x) else 0
        )
    gdf_arr = gdf_arr.dissolve(
        by="NUM_ARROND",
        aggfunc={"pop": "sum"}
        | {col: "mean" for col in col_to_wavg}
        | {"num_poly_" + col: "sum" for col in col_to_wavg},
    )
    for col in col_to_wavg:
        gdf_arr[col] = gdf_arr["num_poly_" + col] * gdf_arr[col] / gdf_arr["pop"]
    gdf_arr = gdf_arr.drop(["num_poly_" + col for col in col_to_wavg], axis=1)
    gdf_arr.to_file(FOLDER_OUT + "paris_dem_iris_2021_arr.gpkg")


def get_mean_age(df):
    if pd.isna(df["P21_POP0002"]):
        return np.nan
    return np.median(
        df["P21_POP0002"] * 1
        + df["P21_POP0305"] * 4
        + df["P21_POP0610"] * 8
        + df["P21_POP1117"] * 14
        + df["P21_POP1824"] * 21
        + df["P21_POP2539"] * 32
        + df["P21_POP4054"] * 47
        + df["P21_POP5564_x"] * 59
        + df["P21_POP6579"] * 72
        + df["P21_POP80P"] * 85
    ) / sum(
        [
            df["P21_POP0002"],
            df["P21_POP0305"],
            df["P21_POP0610"],
            df["P21_POP1117"],
            df["P21_POP1824"],
            df["P21_POP2539"],
            df["P21_POP4054"],
            df["P21_POP5564_x"],
            df["P21_POP6579"],
        ],
        df["P21_POP80P"],
    )


if __name__ == "__main__":
    main()

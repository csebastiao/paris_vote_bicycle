# -*- coding: utf-8 -*-
"""
Add bicycle plan progress to arrondissements.
"""

import pandas as pd
import shapely
import geopandas as gpd


FOLDER_RAW = "./data/processed/paris_simplified_results/"
FOLDER_OFFI = "./data/processed/paris_official_data/"
FOLDER_OUT = "./data/processed/"


def main():
    # TODO bikenet loading correctly
    gdf_bikenet = FOLDER_RAW
    gdf_vote_arr = gpd.read_file(FOLDER_OFFI + "paris_vote_arr_2020.gpkg")
    gdf_vote_arr = gdf_vote_arr.to_crs(gdf_bikenet.crs)
    gdf_vote_arr_res = add_length_to_poly(gdf_vote_arr, gdf_bikenet)
    gdf_vote_arr_res.to_file(FOLDER_OUT + "paris_vote_arr_2020_bikenet.gpkg")


def add_length_to_poly(gdf_poly, gdf_edges):
    gdf_poly_edges = gdf_poly.sjoin(gdf_edges, how="left", predicate="intersects")
    results_dict = {}
    for idx, row in gdf_poly_edges.iterrows():
        if isinstance(row["built"], str):
            length = shapely.intersection(
                row["geometry"],
                gdf_edges.loc[row["u"], row["v"], row["key"]]["geometry"],
            ).length
        else:
            length = 0
        planned = 0
        before = 0
        built = 0
        if row["built"] == "No":
            planned += length
        elif row["built"] == "2021-01-01":
            before += length
        else:
            planned += length
            built += length
        if idx not in results_dict.keys():
            results_dict[idx] = {
                "length_before_2021": before,
                "length_planned": planned,
                "length_built": built,
            }
        else:
            results_dict[idx]["length_before_2021"] += before
            results_dict[idx]["length_planned"] += planned
            results_dict[idx]["length_built"] += built
    df = pd.DataFrame.from_dict(results_dict, orient="index")
    gdf_poly_res = gdf_poly.merge(df, left_index=True, right_index=True)
    gdf_poly_res["length_accomplished_share"] = (
        gdf_poly_res["length_built"] / gdf_poly_res["length_planned"]
    )
    gdf_poly_res["length_final"] = (
        gdf_poly_res["length_before_2021"] + gdf_poly_res["length_planned"]
    )
    for col in [
        "length_before_2021",
        "length_planned",
        "length_built",
        "length_final",
    ]:
        gdf_poly_res[col + "_norm"] = (gdf_poly_res[col] / 10**3) / (
            gdf_poly_res["geometry"].area / 10**6
        )
    return gdf_poly_res


if __name__ == "__main__":
    main()

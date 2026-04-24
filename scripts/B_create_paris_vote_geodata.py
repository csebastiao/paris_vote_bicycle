# -*- coding: utf-8 -*-
"""
Create processed vote data by arrondissements from raw files in Paris.
"""

import os
import pandas as pd
import geopandas as gpd

FOLDER_IN = "./data/raw/official_data/"
FOLDER_OUT = "./data/processed/paris_official_data/"
COLS_TO_DROP = [
    "NB_BLANC",
    "NB_EMARG",
    "NB_INSCR",
    "NB_NUL",
    "NB_PROCU",
    "NB_VOTANT",
    "NUM_CIRC",
    "NUM_QUARTIER",
    "id_bv",
    "st_area_shape",
    "st_perimeter_shape",
]
ALIGNMENT_NUANCES_2020 = {
    "LEXG": 0,
    "LCOM": 1,
    "LFI": 2,
    "LSOC": 3,
    "LRDG": 4,
    "LDVG": 5,
    "LUG": 6,
    "LVEC": 7,
    "LECO": 8,
    "LDIV": 9,
    "LREG": 10,
    "LGJ": 11,
    "LREM": 12,
    "LMDM": 13,
    "LUDI": 14,
    "LUC": 15,
    "LDVC": 16,
    "LLR": 17,
    "LUD": 18,
    "LDVD": 19,
    "LDLF": 20,
    "LRN": 21,
    "LEXD": 22,
    "LNC": 99,
}
NUANCES_CANDIDATES = []


def main():
    if not os.path.exists(FOLDER_OUT):
        os.makedirs(FOLDER_OUT)
    # Save as a file alignment nuances
    df_alignment_nuances = pd.DataFrame.from_dict(
        ALIGNMENT_NUANCES_2020, orient="index", columns=["Value"]
    )
    df_alignment_nuances.to_json(FOLDER_OUT + "vote_alignment_nuances_2020.json")
    # Load every arrondissement results
    li = []
    for i in range(1, 21):
        li.append(
            pd.read_excel(
                FOLDER_IN
                + f"votingparis_values_2020/DDCT_BERP_municipales_2020_tour1_Ardt_{i:02}_20200315.xls"
            )
        )
    df_vote = pd.concat(li, axis=0)
    df_vote = df_vote.rename({"ID_BVOTE": "id_bv"}, axis=1)
    names_candidates = list(
        df_vote.drop(
            [
                "id_bv",
                "SCRUTIN",
                "ANNEE",
                "TOUR",
                "DATE",
                "NUM_CIRC",
                "NUM_QUARTIER",
                "NUM_ARROND",
                "NUM_BUREAU",
                "NB_PROCU",
                "NB_INSCR",
                "NB_EMARG",
                "NB_VOTANT",
                "NB_BLANC",
                "NB_NUL",
                "NB_EXPRIM",
            ],
            axis=1,
        )
    )
    # TODO nuances with 1st round
    candidates = {
        name: nuance for name, nuance in zip(names_candidates, NUANCES_CANDIDATES)
    }
    candidates += 0
    # TODO do with arrondissements directly instead of voting stations
    df_paris_vote_arr = 0
    gdf_paris_arr = gpd.read_file(FOLDER_IN + "arrondissements.geojson")
    gdf_vote = gdf_paris_arr.merge(df_paris_vote_arr, on="NUM_ARROND")
    gdf_vote = compute_left_right_vote_anomaly(gdf_vote)
    gdf_vote.to_file(FOLDER_OUT + "paris_vote_arr_2020.gpkg")


def compute_left_right_vote_anomaly(gdf_vote):
    rm = gdf_vote["Right_wing_share"].mean()
    lm = gdf_vote["Left_wing_share"].mean()
    vote_avg_ratio = rm - lm
    gdf_vote["ratio_LR"] = (
        (gdf_vote["Right_wing"] - gdf_vote["Left_wing"]) / gdf_vote["NB_EXPRIM"]
    ) - vote_avg_ratio
    return gdf_vote


if __name__ == "__main__":
    main()

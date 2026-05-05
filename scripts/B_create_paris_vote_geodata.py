# -*- coding: utf-8 -*-
"""
Create processed vote data by arrondissements from raw files in Paris.
"""

import os
from bs4 import BeautifulSoup
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
    "NUM_BUREAU",
    "DATE",
    "TOUR",
    "ANNEE",
    "SCRUTIN",
    "ID_BVOTE",
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


# TODO make version of arrondissements without the forests
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
        df_arr = pd.read_excel(
            FOLDER_IN
            + f"voting_paris_values_2020/DDCT_BERP_municipales_2020_tour1_Ardt_{i:02}_20200315.xls"
        )
        df_arr = df_arr.rename({col: col.strip() for col in df_arr.columns}, axis=1)
        # Map candidate to nuance
        candidates = {}
        if i < 5:
            area = 1
        else:
            area = i
        htmlfile = open(
            FOLDER_IN + f"voting_paris_candidates_2020/{area:02}.html",
            "r",
            encoding="utf-8",
        )
        data = htmlfile.read()
        soup = BeautifulSoup(data, "html.parser")
        all_res = soup.find_all("td")
        for i in range(0, len(all_res), 3):
            candidates[invert_first_last_names(all_res[i + 2].get_text())] = all_res[
                i + 1
            ].get_text()
        df_arr = df_arr.rename(candidates, axis=1)
        df_arr = df_arr.drop(COLS_TO_DROP, axis=1)
        df_arr = df_arr.T.groupby(level=0, dropna=False).sum().T
        li.append(df_arr)
    df_vote = pd.concat(li)
    df_vote = df_vote.fillna(0)
    left_parties = []
    right_parties = []
    for p in df_vote.columns:
        if p in ALIGNMENT_NUANCES_2020.keys():
            if ALIGNMENT_NUANCES_2020[p] < 12:
                left_parties.append(p)
            elif ALIGNMENT_NUANCES_2020[p] > 16 and ALIGNMENT_NUANCES_2020[p] < 90:
                right_parties.append(p)
    df_vote["Left_wing"] = df_vote.apply(
        lambda df: sum([df[party] for party in left_parties]), axis=1
    )
    df_vote["Right_wing"] = df_vote.apply(
        lambda df: sum([df[party] for party in right_parties]), axis=1
    )
    df_paris_vote_arr = df_vote.groupby("NUM_ARROND").sum()
    for col in ["Left_wing", "Right_wing"]:
        df_paris_vote_arr[col + "_share"] = (
            df_paris_vote_arr[col] / df_paris_vote_arr["NB_EXPRIM"]
        )
    gdf_paris_arr = gpd.read_file(FOLDER_OUT + "paris_dem_iris_2021_arr.gpkg")
    gdf_vote = gdf_paris_arr.merge(df_paris_vote_arr, on="NUM_ARROND")
    gdf_vote.to_file(FOLDER_OUT + "paris_vote_arr_2020.gpkg")


def invert_first_last_names(name):
    split_name = name.strip().split(" ")
    pronoun = split_name[0]
    first = " ".join([char for char in split_name[1:] if char != char.upper()])
    last = " ".join([char for char in split_name[1:] if char == char.upper()])
    return " ".join([pronoun, last, first])


if __name__ == "__main__":
    main()

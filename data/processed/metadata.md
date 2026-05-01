## paris_dem_iris_2021.gpkg
Made in A_create_paris_IRIS_geodata.py using:
- IRIS_geometry_2021: Coming from https://geoservices.ign.fr/irisge#telechargementter2021. Use France métropolitaine. Some IRIS are multipolygons, this is not a bug this is the case in the official data. To see the different type of IRIS polygons, see https://www.insee.fr/fr/information/2438155.
- IRIS_population_2021: Coming from https://www.insee.fr/fr/statistiques/8268806. Use France hors Mayotte.
- IRIS_activity_2021: Coming from https://www.insee.fr/fr/statistiques/8268843. Use France hors Mayotte.
- IRIS_income_2021: Coming from https://www.insee.fr/fr/statistiques/8229323. Use revenus disponibles.


## paris_dem_iris_2021_arr.gpkg
Made in A_create_paris_IRIS_geodata.py using paris_dem_iris_2021_condensed.gpkg, merging data at arrondissement level, except for arrondissement 1 to 4 that are merged together to follow voting areas.

## vote_alignmnent_nuances_2020.json
Made in B_create_paris_vote_geodata.py, copying manually https://www.archives-resultats-elections.interieur.gouv.fr/resultats/municipales-2020/nuances.php.

## paris_vote_arr_2020.gpkg
Made in B_create_paris_vote_geodata.py using:
- votingparis_values_2020: Coming from https://opendata.paris.fr/explore/dataset/elections-municipales-2020-1ertour. Using first round as closer to desired vote.
- Candidates nuances from https://www.archives-resultats-elections.interieur.gouv.fr/resultats/municipales-2020/075/C1075056.php.
- vote_alignment_nuances_2020.json: See above.

## paris_vote_arr_2020_bikenet.gpkg
Made in C_add_bikenet_to_vote.py using:
- paris_vote_arr_2020.gpkg: See above.
- bikenet_paris_2026_01_28.json: https://observatoire.parisenselle.fr/?date=2026-01-28.

### Voting system in Paris in 2020 explained

In 2020, in Paris people voted for a list at the *arrondissement* level (except for the first four *arrondissements* that are merged together). If more than 50% of the valid votes at the first round are for one list, there is no second round. The second round is between lists with at least 10% of valid votes. The list elected at the first round/leading the second round gets 50% of all seats, the remaining seats are proportionally divided among lists with at least 5% of valid votes. The elected councils then vote for the mayor of each *arrondissement*, and for the mayor of the *city*. Part of the councils elected for each *arrondissement* will become part of the council of the *city*. Source: https://www.franceinfo.fr/elections/municipales-2020-a-paris-le-mode-d-emploi-pour-comprendre-le-scrutin-dans-la-capitale_3813299.html.
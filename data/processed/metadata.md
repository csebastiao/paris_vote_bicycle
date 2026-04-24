## paris_dem_iris_2021.gpkg
Made in A_create_paris_IRIS_geodata.py using:
- IRIS_geometry_2021: Coming from https://geoservices.ign.fr/irisge#telechargementter2021. Use France métropolitaine. Not all IRIS are polygons some are multipolygons, this is not a bug this is the case in the official data. To see the different type of IRIS, see https://www.insee.fr/fr/information/2438155.
- IRIS_population_2021: Coming from https://www.insee.fr/fr/statistiques/8268806. Use France hors Mayotte.
- IRIS_activity_2021: Coming from https://www.insee.fr/fr/statistiques/8268843. Use France hors Mayotte.
- IRIS_income_2021: Coming from https://www.insee.fr/fr/statistiques/8229323. Use revenus disponibles.

## paris_dem_iris_2021_condensed.gpkg
Made in A_create_paris_IRIS_geodata.py using paris_dem_iris_2021.gpkg, adding composite attributes, dropping irrelevant columns and renaming other columns with clearer names.

## paris_dem_iris_2021_condensed_filledna.gpkg
Made in A_create_paris_IRIS_geodata.py using paris_dem_iris_2021_condensed.gpkg, adding estimated NA values for median income of areas.

## paris_vote_arr_2020.gpkg
In 2020, in Paris people voted for **one** list at the *arrondissements* level (except for the first four that are merged together). If more than 50% of the valid votes at the first round are for one list, there is no second round. The second round is between lists with at least 10% of valid votes. The list elected at the first round/leading the second round gets 50% of all seats, the remaining seats are proportionally divided among lists with at least 5% of valid votes. The elected councils then vote for the mayor of each *arrondissement*, and for the mayor of the *city*. Part of the councils elected for each *arrondissements* will become part of the council of the *city*. (source: https://www.franceinfo.fr/elections/municipales-2020-a-paris-le-mode-d-emploi-pour-comprendre-le-scrutin-dans-la-capitale_3813299.html)

Made using:
- votingparis_values_2020: Coming from https://opendata.paris.fr/explore/dataset/elections-municipales-2020-2emetour/information/ for all arrondissements except the 7th that was decided at the first round, can be found https://opendata.paris.fr/explore/dataset/elections-municipales-2020-1ertour

## vote_alignmnent_nuances_2020.json
Voting alignment can be found here: https://www.archives-resultats-elections.interieur.gouv.fr/resultats/municipales-2020/nuances.php. Used manually.


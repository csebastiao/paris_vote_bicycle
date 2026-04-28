# TODO getting blocked currently, saving html files individually

# import requests

# FOLDER_SAVE = "./data/raw/official_data/voting_paris_candidates_2020/

# def main():
# arr_num = [1] + list(range(5, 21))
# for arr in arr_num:
#     url = f"https://www.archives-resultats-elections.interieur.gouv.fr/resultats/municipales-2020/075/C1075056SR{arr:02}.php"
#     response = requests.get(url)
#     with open(FOLDER_SAVE + "{arr:02}_scraped.html", "wb") as f:
#         f.write(response.content)

# if __name__ == "__main__":
#     main()

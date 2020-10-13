from utils import *
from tqdm import tqdm
from random import randint
import pandas as pd
import math
import time
import os

breed_dct = {"6": "Ecaflip",
             "7": "Eniripsa",
             "8": "Iop",
             "9": "Cra",
             "1": "Feca",
             "11": "Sacrieur",
             "10": "Sadida",
             "2": "Osamodas",
             "3": "Enutrof",
             "4": "Sram",
             "5": "Xelor",
             "12": "Pandawa",
             "13": "Roublard",
             "14": "Zobal",
             "15": "Steamer",
             "16": "Eliotrope",
             "17": "Huppermage",
             "18": "Ouginak"}


def retrieve_n_pages(soup, char_per_page=24):
    s = soup.find("div", {"class": "ak-list-info"})
    if s:
        n_perso = s.find("strong").text
        if n_perso == "Aucun":
            return 0
        return math.ceil(int(n_perso) / char_per_page)
    return 1  # if there are less than 24 results, there will be no number of results displayed


def parse_page(soup):
    res_lst = []

    s1 = soup.findAll("tr", {"class": "ak-bg-odd"})
    s2 = soup.findAll("tr", {"class": "ak-bg-even"})

    for s in [s1, s2]:
        for row in s:
            values = row.findAll("a")
            name = values[0].text
            url = values[0].attrs["href"]
            values = {"name": name, "url": url}
            res_lst.append(values)

    return res_lst


def generate_url(page, breed_id=6, lvl=70, server=222, gender=0):
    return f"https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-persos?text=" \
           f"&character_breed_id%5B%5D={breed_id}" \
           f"&character_homeserv%5B%5D={server}" \
           f"&character_level_min={lvl}" \
           f"&character_level_max={lvl}" \
           f"&character_sex%5B%5D={gender}" \
           f"&page={page}#jt_list"


def generate_filename(breed_id=6, lvl=70, server=222, gender=0):
    return f"{server}_{breed_id}_{gender}_{lvl}.csv"


breed_dct = {"6": "Ecaflip",
             "7": "Eniripsa",
             "8": "Iop",
             "9": "Cra",
             "1": "Feca",
             "11": "Sacrieur",
             "10": "Sadida",
             "2": "Osamodas",
             "3": "Enutrof",
             "4": "Sram",
             "5": "Xelor",
             "12": "Pandawa",
             "13": "Roublard",
             "14": "Zobal",
             "15": "Steamer",
             "16": "Eliotrope",
             "17": "Huppermage",
             "18": "Ouginak"}

breeds = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
genders = [0, 1]
levels = range(60, 256)

if __name__ == "__main__":
    for server in [222]:
        for breed_id in breeds:
            for gender in genders:
                for lvl in tqdm(levels, desc="Level progression for "
                                             f"server {server} "
                                             f"breed {breed_id} "
                                             f"gender {gender}"):

                    filename = generate_filename(breed_id, lvl, server, gender)

                    if not os.path.isfile(os.path.join("url_lists", filename)):
                        try:
                            rows = []

                            # Check page 1 to get number of pages
                            time.sleep(0.2 + randint(1, 10) / 10)
                            url = generate_url(1, breed_id, lvl, server, gender)

                            soup = url_to_soup(url)
                            n_pages = retrieve_n_pages(soup)
                            parsed_soup = parse_page(soup)
                            rows += parsed_soup

                            for p in range(2, n_pages + 1):
                                time.sleep(0.2 + randint(1, 10) / 10)

                                url = generate_url(p, breed_id, lvl, server, gender)
                                soup = url_to_soup(url)
                                parsed_soup = parse_page(soup)
                                rows += parsed_soup

                            df = pd.DataFrame(rows)

                            df.to_csv(os.path.join("url_lists", filename), index=False)
                        except Exception as e:
                            print(e, url)

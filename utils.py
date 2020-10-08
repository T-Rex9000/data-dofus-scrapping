import requests
from bs4 import BeautifulSoup
import pandas as pd

def url_to_soup(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data)
    return soup


def fetch_all_breeds():
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

    # Merge all character csv files
    df = []

    for breed_id, breed in breed_dct.items():
        try:
            temp_df = pd.read_csv(f"character_lists/parsed_{breed}.csv")
            df.append(temp_df)
        except Exception as e:
            print(e)

    df = pd.concat(df)
    return df
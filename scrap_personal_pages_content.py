from parse_functions import *
import pandas as pd
from tqdm import tqdm
from random import randint
import json
import time
from os import listdir
from os.path import join, isfile

if __name__ == "__main__":
    url_lists_path = "./url_lists"
    out_path = "./data"

    url_lists = listdir(url_lists_path)

    for filename in url_lists:
        # Load url list
        tmp_df = pd.read_csv(join(url_lists_path, filename))

        tmp_url_lst = list(tmp_df["url"])

        # For every url
        for url in tqdm(tmp_url_lst, desc="List progress"):
            try:
                name_and_id = url.split("/")[-1]

                if isfile(join(out_path, f"{name_and_id}.json")):
                    continue

                time.sleep(randint(1, 6) / 10)

                # Scrap caracteristiques
                carac_dct = process_perso_caracteristiques(url="https://www.dofus.com" + url + "/caracteristiques")

                # If profile is not hidden
                if carac_dct:
                    # Scrap other info
                    others_dct = process_perso_main(url="https://www.dofus.com" + url)

                    # Merge info
                    carac_dct.update(others_dct)

                    # Save results
                    with open(join(out_path, f"{name_and_id}.json"), "w") as f:
                        json.dump(carac_dct, f)
                else:
                    with open(join(out_path, f"{name_and_id}.json"), "w") as f:
                        json.dump({}, f)
            except Exception as e:
                print(e, url)

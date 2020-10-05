from parse_functions import *
from datetime import datetime
from tqdm import tqdm
from random import randint
import json
import time
import os

if __name__ == "__main__":
    main_dct_path = "annuaire.json"
    data_path = "data"

    with open(main_dct_path, "r") as f:
        main_dct = json.load(f)

    for id, val in tqdm(main_dct.items()):
        time.sleep(0.2 + randint(1, 10) / 10)
        url = val["url"]

        carac_dct = process_perso_caracteristiques(url="https://www.dofus.com" + url + "/caracteristiques")

        if carac_dct:
            date = datetime.today().strftime('%Y-%m-%d')

            others_dct = process_perso_main(url="https://www.dofus.com" + url)

            carac_dct.update(others_dct)

            with open(os.path.join(data_path, f"{id}_{date}.json"), "w") as f:
                json.dump(carac_dct, f)


        else:
            continue

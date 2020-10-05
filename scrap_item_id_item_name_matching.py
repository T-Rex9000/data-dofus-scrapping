from utils import *
from tqdm import tqdm
import json
import time

if __name__ == "__main__":
    # Get DataFrame with all charcter csv files merged
    df = fetch_all_breeds()

    # Drop entirely empty equipments
    df.dropna(inplace=True, how="all")

    # Replace empty equipments with -1 (later mapped to unknown)
    df.fillna(-1, inplace=True)

    # Gather all item ids
    id_list = []

    for c in ['shield', 'amulet', 'ring1', 'cap', 'boots', 'weapon', 'hat', 'ring2', 'belt']:
        id_list += list(set(df[c]))

    # Start scrapping item names
    out_dct = {}

    for id in tqdm(id_list):
        time.sleep(1)
        url = f"https://www.dofus.com/fr/mmorpg/encyclopedie/equipements/{int(id)}"
        try:
            soup = url_to_soup(url)
            title = soup.find("h1").text.replace("\n", "")

            out_dct[int(id)] = title
            print(title)

        except Exception as e:
            print(e)

    # Save
    with open("scrapping/item_id_item_name.json", "w") as f:
        json.dump(out_dct, f)

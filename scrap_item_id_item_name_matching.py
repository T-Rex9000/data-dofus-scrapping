from utils import *
from tqdm import tqdm
import json
import time

if __name__ == "__main__":
    output_dct = {}
    list_of_items = []
    list_of_url_recipes = []
    item_types = ["equipements", "armes", "idoles"]
    list_nb_pages = [25, 8, 1]

    for item_type, nb_pages in zip(item_types, list_nb_pages):
        for page in range(1, nb_pages + 1):
            url = "https://www.dofus.com/fr/mmorpg/encyclopedie/{}?size=96&page={}".format(item_type, page)
            try:
                page = requests.get(url)
                soup = BeautifulSoup(page.content, 'html.parser')
                table_items = list(soup.find_all('tbody'))
                for i, link in enumerate(table_items[0].find_all('a')):
                    if i % 2 != 0:
                        id_item = link.get('href').split('/')[-1].split("-")[0]
                        nom_item = link.text
                        if id_item not in output_dct.keys():
                            output_dct[id_item] = nom_item
            except Exception as e:
                print(e)

    with open("scrapping/item_id_item_name.json", "w") as f:
        json.dump(output_dct, f)

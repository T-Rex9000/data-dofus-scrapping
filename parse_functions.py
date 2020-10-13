from utils import *
import json


def retrieve_items(soup):
    items = ["shield", "amulet", "ring1", "cap", "boots", "weapon", "hat", "ring2", "belt", "pet"]
    item_ids = {}

    for item in items:
        item_id = soup.find("div", {"class": f"ak-equipment-item ak-equipment-{item}"})

        try:
            item_id = int(
                json.loads(item_id.find('script', type='application/json').string)["linker-id"].split("_")[-1])
        except:
            item_id = None

        item_ids[item] = item_id

    dofus = soup.findAll("div", {"class": f"ak-equipment-item ak-equipment-dofus"})
    for i, dofu in enumerate(dofus[:6]):
        try:
            item_id = int(json.loads(dofu.find('script', type='application/json').string)["linker-id"].split("_")[-1])
        except:
            item_id = None

        item_ids[f"dofus-{i}"] = item_id

    return item_ids


def parse_table(pct, type, do_or_res=None):
    rows = pct.find_all("tr", {"class": "ak-bg-odd"}) + pct.find_all("tr", {"class": "ak-bg-even"})

    parsed_rows = {}

    if type == "characteristics":
        for row in rows:
            columns = row.find_all("td")
            c_name = columns[1].text

            parsed_rows[f"{c_name}_base"] = int(columns[2].text)
            parsed_rows[f"{c_name}_bonus"] = int(columns[3].text)
            parsed_rows[f"{c_name}_total"] = int(columns[4].text)

    elif type == "others":
        for row in rows:
            columns = row.find_all("td")
            c_name = columns[1].text
            parsed_rows[f"{do_or_res}_{c_name}_total"] = int(columns[2].text)

    return parsed_rows


def process_perso_caracteristiques(url):
    soup = url_to_soup(url)
    primary_tables = soup.findAll("div", {"class": "col-md-6 ak-primary-caracteristics"})[:2]
    secondary_tables = soup.findAll("div", {"class": "col-md-6 ak-secondary-caracteristics"})[:2]

    if len(primary_tables) == 0:  # restricted
        return

    primary_caracteristics = primary_tables[0]
    secondary_caracteristics = secondary_tables[0]
    primary_others = primary_tables[1]
    secondary_others = secondary_tables[1]

    primary_caracteristics = parse_table(primary_caracteristics, type="characteristics")
    secondary_caracteristics = parse_table(secondary_caracteristics, type="characteristics")
    primary_others = parse_table(primary_others, type="others", do_or_res="do")
    secondary_others = parse_table(secondary_others, type="others", do_or_res="res")

    item_ids = retrieve_items(soup)

    return {
        **item_ids,
        **primary_caracteristics,
        **secondary_caracteristics,
        **primary_others,
        **secondary_others
    }


def process_perso_main(url):
    soup = url_to_soup(url)

    res_dct = {}

    kolis = soup.findAll("div", {"class": "ak-total-kolizeum"})

    for koli in kolis:
        res_dct[f"{koli.text.split(':')[0]}"] = int(koli.find("span").text.replace(" ", "")) if koli.find(
            "span").text not in ["-1",
                                 "-"] else None

    xp = soup.find("div", {"class": "ak-total-xp"})

    if xp:
        xp = xp.find("span").text.replace(" ", "")
        res_dct["xp"] = int(xp) if xp != "-" else None
    else:
        res_dct["xp"] = None

    success = soup.find("div", {"class": "ak-total-success"})

    if success:
        success = success.find("span").text.replace(" ", "")
        res_dct["success"] = int(success) if success != "-" else None
    else:
        res_dct["success"] = None

    table = soup.find("table", {"class": "ak-container ak-table ak-responsivetable"})
    tds = table.findAll("td")

    if len(tds) == 16:
        res_dct["xp_general_rk"] = int(tds[1].text.replace(" ", "")) if tds[1].text != "-" else None
        res_dct["xp_breed_rk"] = int(tds[5].text.replace(" ", "")) if tds[5].text != "-" else None
        res_dct["xp_server_rk"] = int(tds[9].text.replace(" ", "")) if tds[9].text != "-" else None
        res_dct["xp_breed_server_rk"] = int(tds[13].text.replace(" ", "")) if tds[13].text != "-" else None

        res_dct["koli_general_rk"] = int(tds[2].text.replace(" ", "")) if tds[2].text != "-" else None
        res_dct["koli_breed_rk"] = int(tds[6].text.replace(" ", "")) if tds[6].text != "-" else None
        res_dct["koli_server_rk"] = int(tds[10].text.replace(" ", "")) if tds[10].text != "-" else None
        res_dct["koli_breed_server_rk"] = int(tds[14].text.replace(" ", "")) if tds[14].text != "-" else None

        res_dct["success_general_rk"] = int(tds[3].text.replace(" ", "")) if tds[3].text != "-" else None
        res_dct["success_breed_rk"] = int(tds[7].text.replace(" ", "")) if tds[7].text != "-" else None
        res_dct["success_server_rk"] = int(tds[11].text.replace(" ", "")) if tds[11].text != "-" else None
        res_dct["success_breed_server_rk"] = int(tds[15].text.replace(" ", "")) if tds[15].text != "-" else None
    else:
        res_dct["xp_general_rk"] = None
        res_dct["xp_breed_rk"] = None
        res_dct["xp_server_rk"] = None
        res_dct["xp_breed_server_rk"] = None

        res_dct["koli_general_rk"] = None
        res_dct["koli_breed_rk"] = None
        res_dct["koli_server_rk"] = None
        res_dct["koli_breed_server_rk"] = None

        res_dct["success_general_rk"] = None
        res_dct["success_breed_rk"] = None
        res_dct["success_server_rk"] = None
        res_dct["success_breed_server_rk"] = None

    res_dct["level"] = 200 + int(soup.find("span", {"class": "ak-directories-level"}).text[8:-1].replace("Omega ", ""))

    return res_dct


if __name__ == "__main__":
    print(process_perso_caracteristiques(
        "https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-persos/125857500222-vaucherminator/caracteristiques"))
    process_perso_main(
        "https://www.dofus.com/fr/mmorpg/communaute/annuaires/pages-persos/125857500222-vaucher`minator/")

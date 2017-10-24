import datetime
import json
import multiprocessing
import os
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlretrieve

import bs4
import requests
from selenium import webdriver


#THIS IS A STEP BY STEP PROGRAM :)
#TODO: for future use, consider:
#TODO: 1. getting data via selenium only (Don't use requests at all, since selenium has to be used for dynamicaly created content anyway. So html is available anyway...)
#TODO: 2. get all data - images and text - in one batch



def get_entries_on_pages():
    url_start = "https://boyawards.secure-platform.com/a/gallery?roundId=12&searchParams=%7B%22filterByApplicationCategoryPath%22%3A%5B%5D%2C%22filterByWinnerCategoriesIds%22%3A%5B%5D%2C%22pageIndex%22%3A"
    url_end = "%2C%22sortMode%22%3A%22ApplicationCategoryFriendlyPath%22%2C%22sortDirection%22%3A%22Ascending%22%2C%22displayMode%22%3A%22List%22%2C%22filterByFieldValues%22%3A%5B%5D%2C%22filterByTextValue%22%3Anull%7D"
    num_pages = range(0, 18 + 1)

    for num in num_pages:
        r = requests.get((url_start + str(num) + url_end))
        file = open(("./pages/" + str(num) + ".html"), mode="w", encoding="utf-8")
        file.write(("[" + r.text.split("applicationJudgements: [")[1].split("\n")[0]))
        file.close()

# get_entries_on_pages()


def get_all_entries_id_and_write_to_file():
    ids = []

    for filename in os.listdir("./pages/"):
        file = open("./pages/" + filename)
        line = file.readline()
        file.close()

        entries = line[2:-2].split("},{")

        for entry in entries:
            entry_dict = json.loads("{" + entry + "}")
            ids.append(entry_dict["id"])

    entries_file = open("entry_ids.txt", mode="w")
    for index in ids:
        entries_file.write(str(index) + "\n")
    entries_file.close()

# get_all_entries_id_and_write_to_file()


def get_entry_data(entry_id:str):
    boy_page_url = "https://boyawards.secure-platform.com/a/gallery/rounds/12/details/" + entry_id
    r = requests.get(boy_page_url)

    s = bs4.BeautifulSoup(r.text, "html.parser")
    gallery_info = s.find_all(class_="gallery_info")[0]
    p = gallery_info.find_all("p")

    product_name = s.find("p", class_="m_name").get_text()
    category = p[0].get_text()
    company_name = p[1].get_text().split("\n")[1]
    company_url = p[2].get_text().split("\n")[1]
    description_html = str(p[3]).split("\n")[1][:-4]
    video_url = gallery_info.find("a", {"id": "video-link"}).get("href")

    return {"boy_page_url": boy_page_url,
            "id": entry_id,
            "product_name": product_name,
            "category": category,
            "company_name": company_name,
            "company_url": company_url,
            "description_html": description_html,
            "video_url": video_url}


def for_each_entry_id_write_data_to_file():

    f = open("entry_ids.txt", "r")
    ids = [id.rstrip() for id in f.readlines()]
    f.close()

    start = datetime.datetime.now()

    for id in ids:
        with open(('./entries/' + id + ".json"), 'w', encoding="utf-8") as outfile:
            json.dump(get_entry_data(id), outfile, indent=0, sort_keys=True)

    print(datetime.datetime.now() - start)


# for_each_entry_id_write_data_to_file()


def save_entry_pictures(driver: webdriver, entry_id: str):
    boy_page_url = "https://boyawards.secure-platform.com/a/gallery/rounds/12/details/" + entry_id
    driver.get(boy_page_url)

    li_webelements = driver.find_element_by_class_name("slides").find_elements_by_tag_name("li")
    for i, li in enumerate(li_webelements):
        url = li.find_element_by_tag_name("a").get_attribute("href")
        ext = Path(urlparse(url).path).suffix
        path = "./images/" + entry_id + "/"
        Path(path).mkdir(parents=True, exist_ok=True)
        urlretrieve(url, (path + str(i+1) + ext))

    with open("log.txt", "a") as f:
        f.writelines(" ".join([entry_id, "got", str(len(li_webelements)), "images"])+"\n")


def for_each_entry_id_get_images():
    f = open("entry_ids.txt", "r")
    ids = [entry_id.rstrip() for entry_id in f.readlines()]
    f.close()

    start = datetime.datetime.now()

    driver = webdriver.Chrome(executable_path="./chromedriver.exe")

    for entry_id in ids:
        save_entry_pictures(driver, entry_id)

    with open("log.txt", "a") as f:
        now = str(datetime.datetime.now())
        how_long = (str(datetime.datetime.now() - start))
        f.writelines("  -->  ".join([now, how_long]) + "\n")


# for_each_entry_id_get_images()






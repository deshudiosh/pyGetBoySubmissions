import ast
import json

import os
import requests

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

get_all_entries_id_and_write_to_file()

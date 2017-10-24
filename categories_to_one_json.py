import json
import os
import timing
from collections import defaultdict


def sort_entries_by_category():

    # defaultdict auto creates keys, when they don't exist
    by_category = defaultdict(list)

    path = "./entries/"
    for entry_json in os.listdir(path):
        f = open((path+entry_json))
        file_read = f.read()
        entry_dict = json.loads(file_read)
        f.close()
        category = entry_dict["category"]
        by_category[category].append(entry_dict)

    # pprint(by_category)

    with open("./entries_by_category.json", "w", encoding="utf-8") as outfile:
        json.dump(by_category, outfile, indent=4, sort_keys=True)


timing.init()
sort_entries_by_category()

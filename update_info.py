import os
import json
from pathlib import Path


MAIN_DIRS = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


def gather_info(check_dir, json_data):

    for main in MAIN_DIRS:
        main_dir = check_dir / main
        titles = os.listdir(main_dir)
        for title in titles:
            verified = False
            if "[o]" in title:
                # title = title.replace("[o]", "").strip()
                verified = True

            vol_dir = main_dir / title

            vols = title.split(" ")[-1]
            title = title[: len(title) - len(vols)].strip()

            if json_data.get(title) is not None:
                continue
            else:
                title_dict = {
                    "kor": title.replace("[o]", "").strip(),
                    "eng": "",
                    "jpn": "",
                }

                author_dict = {
                    "kor": "",
                    "eng": "",
                    "jpn": "",
                }

                doc_info = {
                    "title": title_dict,
                    "vols": vols,
                    "verified": "O" if verified else "X",
                    "status": main,
                    "author": author_dict,
                }

                json_data[title] = doc_info


def main():
    check_dir = Path("d:/comix")
    json_path = Path("./comix_info.json")

    # Read comix list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    # Gather information
    gather_info(check_dir, json_data)

    # Sort
    key_list = list(json_data.keys())
    key_list.sort()

    new_json_data = dict()
    for k in key_list:
        new_json_data[k] = json_data[k]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(new_json_data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

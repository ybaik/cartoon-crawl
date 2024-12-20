import os
import re
import json
from pathlib import Path


MAIN_DIRS = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


def main():
    check_dir = Path("d:/comix")
    json_path = Path("./db/comix_info.json")
    json_data = (
        json_path.exists() and json.load(open(json_path, encoding="utf-8")) or dict()
    )

    for main in MAIN_DIRS:
        main_dir = check_dir / main

        for title in os.listdir(main_dir):
            verified = "[o]" in title
            title_info = title.replace("(완)", "").split()
            vols = title_info.pop() if re.match(r"\d+-\d+", title_info[-1]) else ""
            title = " ".join(title_info)
            if title in json_data:
                if json_data[title]["vols"] != vols:
                    print(title, json_data[title]["vols"], vols)
            else:
                print(1)


if __name__ == "__main__":
    main()

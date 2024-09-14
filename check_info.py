import os
import json
from pathlib import Path


MAIN_DIRS = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


def main():
    check_dir = Path("d:/comix")
    json_path = Path("./comix_info.json")

    # Read comix list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    # Check
    checked_keys = set()
    for main in MAIN_DIRS:
        main_dir = check_dir / main
        titles = os.listdir(main_dir)
        for title in titles:
            vols = title.split(" ")[-1]
            title = title[: len(title) - len(vols)].strip()

            if json_data.get(title) is not None:
                checked_keys.add(title)
            else:
                print(f"{title} is not in the comix_info.json")

    original_keys = set(json_data.keys())
    print(original_keys - checked_keys)


if __name__ == "__main__":
    main()

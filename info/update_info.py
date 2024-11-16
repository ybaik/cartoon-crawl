import os
import re
import json

from pathlib import Path


MAIN_DIRS = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


def gather_info(check_dir: Path, json_data: dict) -> None:
    for main in MAIN_DIRS:
        main_dir = check_dir / main

        for title in os.listdir(main_dir):
            verified = "[o]" in title
            title_info = title.replace("(완)", "").split()
            vols = title_info.pop() if re.match(r"\d+-\d+", title_info[-1]) else ""
            title = " ".join(title_info)
            if title in json_data:
                continue

            json_data[title] = {
                "title": {
                    "kor": title.replace("[o]", "").strip(),
                    "eng": "",
                    "jpn": "",
                },
                "vols": vols,
                "verified": "O" if verified else "X",
                "status": main,
                "author": {"kor": "", "eng": "", "jpn": ""},
            }


def main():
    check_dir = Path("d:/comix")
    json_path = Path("./db/comix_info.json")

    # Read comix list
    json_data = (
        json.load(open(json_path, encoding="utf-8")) if json_path.exists() else {}
    )

    # Gather information
    gather_info(check_dir, json_data)

    # Sort and write
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(dict(sorted(json_data.items())), f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

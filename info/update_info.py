import os
import re
import json

from pathlib import Path


MAIN_DIRS = ["미완", "미완_스캔", "연재중", "연재중_스캔", "완결", "완결_스캔"]


def gather_info(check_dir: Path, json_data: dict) -> None:

    for main in MAIN_DIRS:
        main_dir = check_dir / main
        titles = os.listdir(main_dir)
        for title in titles:
            verified = False
            if "[o]" in title:
                verified = True
            title = title.replace("(완)", "")
            vols = title.split()[-1]
            if re.match(r"\d+-\d+", vols):
                title = title.removesuffix(vols).strip()
            else:
                vols = ""

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

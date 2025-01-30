# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import List, Dict


def save_json(json_path: Path, json_data: Dict) -> None:
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def main():
    # Set path
    title = "b"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    site_url = "https://ww7.readfairytail.com"
    list_url = f"{site_url}/chapter"

    # Read url list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = {
            "site_name": "",
            "tag_list": list(),
            "vol_info": dict(),
        }

    for i in range(1, 36):
        json_data["vol_info"][f"페어리테일{i:0d}"] = {
            "vol_url": f"{site_url}/manga/edens-zero-chapter-{i}",
        }

    save_json(json_path, json_data)


if __name__ == "__main__":
    main()

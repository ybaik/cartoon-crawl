# -*- coding: utf-8 -*-
import json
from pathlib import Path
from crawling.crawling_toon import (
    crawling_vols,
    crawling_vols_selenium,
    crawling_img_list,
    crawling_img_list_selenium,
    download_images,
)


USE_SELENIUM = False


def main():
    # Set path
    title = "a"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url
    site_url = "https://www.11toon131.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%EC%A7%80%EC%98%A5%EB%9D%BD&is=7452&sord=&type=&page=1"

    tags = []
    tags.append("스파이")

    # Read url list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    # Extract voulumn-wise url information via
    if not USE_SELENIUM:
        crawling_vols(site_url, list_url, json_data, json_path)
    else:
        crawling_vols_selenium(site_url, list_url, json_data, json_path)

    # Extract image-wise url information via crawling
    if not USE_SELENIUM:
        crawling_img_list(json_data, json_path)
    else:
        crawling_img_list_selenium(json_data, json_path)
    # return

    download_images(json_data, base_dir, tags)


if __name__ == "__main__":
    main()

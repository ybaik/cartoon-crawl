# -*- coding: utf-8 -*-
import json
from pathlib import Path
from common.crawling_toon import (
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
    site_url = "https://www.11toon132.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%EB%B0%94%EB%9E%8C%EA%B3%84%EA%B3%A1%EC%9D%98%20%EB%82%98%EC%9A%B0%EC%8B%9C%EC%B9%B4&is=11125"

    tags = []
    tags.append("바람계곡의 나우시카")

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

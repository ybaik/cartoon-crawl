# -*- coding: utf-8 -*-
import json
from pathlib import Path
from common.crawling_manaboza import (
    crawling_vols,
    crawling_img_list,
)
from common.crawling_toon import download_images

from common.crawler import SeleniumCrawlerManaboza

USE_SELENIUM = True


def main():
    # Set path
    title = "a"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url
    site_url = "https://manaboza74.com/comic/ep_list/20771"
    list_url = site_url

    tags = []
    tags.append("-")

    # Read url list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    if not USE_SELENIUM:
        crawling_vols(site_url, list_url, json_data, json_path)
        crawling_img_list(json_data, json_path)
    else:
        crawler = SeleniumCrawlerManaboza(headless=False)
        crawler.crawling_vols(site_url, list_url, json_data, json_path)
        crawler.crawling_img_list(json_data, json_path)
        crawler.deinit()

    return
    download_images(json_data, base_dir, tags)


if __name__ == "__main__":
    main()

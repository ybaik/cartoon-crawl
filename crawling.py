# -*- coding: utf-8 -*-
import json
from pathlib import Path
from common.crawling_toon import (
    crawling_vols,
    crawling_img_list,
    download_images,
)
from common.crawler import SeleniumCrawlerToon

USE_SELENIUM = False


def main():
    # Set path
    title = "a"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url
    site_url = "https://www.11toon134.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%ED%8E%AB%EC%88%8D%20%EC%98%A4%EB%B8%8C%20%ED%98%B8%EB%9F%AC%EC%A6%88&is=21025"

    tags = []
    tags.append("펫숍 오브 호러즈")

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

        crawler = SeleniumCrawlerToon()
        crawler.crawling_vols(site_url, list_url, json_data, json_path)
        crawler.crawling_img_list(json_data, json_path)
        crawler.deinit()

    # return
    download_images(json_data, base_dir, tags)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
import json
from pathlib import Path
from common.crawler import SeleniumCrawlerToki


def main():
    # Set path
    title = "a"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url
    site_url = "https://manatoki461.net/comic"
    list_url = f"{site_url}/278794?stx=%EC%B9%B4%EB%93%9C%EC%BA%A1%ED%84%B0"

    tags = []
    tags.append("카드캡터 사쿠라")

    # Read url list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    # Initialize cralwer
    crawler = SeleniumCrawlerToki()

    # Extract voulumn-wise url information via
    crawler.crawling_vols(list_url, json_data, json_path)

    # Extract image-wise url information via crawling
    crawler.crawling_img_list(json_data, json_path)

    # return
    # crawler.download_images(json_data, base_dir, tags)


if __name__ == "__main__":
    main()

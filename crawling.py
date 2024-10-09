# -*- coding: utf-8 -*-
import json
from pathlib import Path
from common.crawler import create_crawler, download_images


USE_SELENIUM = False


def main():
    # Set path
    title = "a"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url - 11toon
    site_url = "https://www.11toon136.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%EA%B7%B8%EB%9E%9C%20%ED%8C%A8%EB%B0%80%EB%A6%AC%EC%95%84&is=35499"
    # # Set url - manaboza
    # site_url = "https://manaboza76.com/comic/ep_list"
    # list_url = f"{site_url}/35499"
    # # Set url - manatoki
    # site_url = "https://manatoki463.net/comic"
    # list_url = f"{site_url}/20721164?stx=%EA%B7%B8%EB%9E%9C+%ED%8C%A8%EB%B0%80%EB%A6%AC%EC%95%84"

    tags = []
    # tags.append("")

    # Read url list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    crawler = create_crawler(site_url, USE_SELENIUM)
    if crawler is None:
        print("Unknown site!")
        return
    crawler.crawling_vols(list_url, json_data, json_path)
    crawler.crawling_img_list(json_data, json_path)
    crawler.deinit()

    return
    download_images(json_data, base_dir, tags)


if __name__ == "__main__":
    main()

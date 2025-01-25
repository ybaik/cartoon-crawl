# -*- coding: utf-8 -*-
import json
from pathlib import Path
from common.crawler import create_crawler, download_images, filter_title


USE_SELENIUM = False


def main():
    # Set path
    title = "aa"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url - 11toon
    site_url = "https://www.11toon144.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%ED%8E%98%EC%96%B4%EB%A6%AC%ED%85%8C%EC%9D%BC&is=11&sord=&type=&page=2"
    # Set url - manaboza
    # site_url = "https://manaboza76.com/comic/ep_list"
    # list_url = f"{site_url}/35499"
    # # Set url - manatoki
    # site_url = "https://manatoki463.net/comic"
    # list_url = f"{site_url}/20721164?stx=%EA%B7%B8%EB%9E%9C+%ED%8C%A8%EB%B0%80%EB%A6%AC%EC%95%84"
    # Set url - newtoki
    # site_url = "https://newtoki.biz/manhwa"
    # list_url = f"{site_url}/7272"
    # site_url = "https://newtoki.biz/webtoon"
    # list_url = f"{site_url}/3593"

    # site_url = "https://www.mangaread.org/manga"
    # list_url = f"{site_url}/fairy-tail/chapter-475-dimaria-chronos-yesta"

    site_url = "https://ww7.readfairytail.com"
    list_url = f"{site_url}/manga/edens-zero"

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

    crawler = create_crawler(site_url, USE_SELENIUM)
    if crawler is None:
        print("Unknown site!")
        return
    crawler.crawling_vols(list_url, json_data, json_path)
    crawler.crawling_img_list(json_data, json_path)
    crawler.deinit()

    # Check filter
    json_data["tag_list"].append("Eden’s Zero")
    json_data["tag_list"].append("Chapter")
    for key in json_data["vol_info"].keys():
        tags = json_data["tag_list"]
        name = filter_title(key, tags)
        print(name)
        if name == key:
            print(key)
            pass

    # return
    download_images(json_data, base_dir, site_url)


if __name__ == "__main__":
    main()

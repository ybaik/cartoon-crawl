# -*- coding: utf-8 -*-
import json
from pathlib import Path
from common.crawler import create_crawler, download_images, filter_title


USE_SELENIUM = True


def main():
    # Set path
    title = "a"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url - 11toon
    site_url = "https://www.11toon139.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%EB%93%9C%EB%9E%98%EA%B3%A4%EB%B3%BC%20%ED%92%80%EC%BB%AC%EB%9F%AC%204%EB%B6%80%20%ED%94%84%EB%A6%AC%EC%A0%80%ED%8E%B8&is=21860"
    # # Set url - manaboza
    # site_url = "https://manaboza76.com/comic/ep_list"
    # list_url = f"{site_url}/35499"
    # # Set url - manatoki
    # site_url = "https://manatoki463.net/comic"
    # list_url = f"{site_url}/20721164?stx=%EA%B7%B8%EB%9E%9C+%ED%8C%A8%EB%B0%80%EB%A6%AC%EC%95%84"

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
    json_data["tag_list"].append("드래곤볼 풀컬러 4…부 프리저편")
    json_data["tag_list"].append("드래곤볼 풀컬러 4부 프리저편")
    for key in json_data["vol_info"].keys():
        tags = json_data["tag_list"]
        name = filter_title(key, tags)
        print(name)
        if name == key:
            print(key)
            pass

    return
    download_images(json_data, base_dir)


if __name__ == "__main__":
    main()

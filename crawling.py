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
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%EC%97%90%EB%8D%B4%EC%A6%88+%EC%A0%9C%EB%A1%9C&is=9545&sord=&type=&page=1"
    # Set url - manaboza
    # site_url = "https://manaboza76.com/comic/ep_list"
    # list_url = f"{site_url}/35499"
    # # Set url - manatoki
    # site_url = "https://manatoki463.net/comic"
    # list_url = f"{site_url}/20721164?stx=%EA%B7%B8%EB%9E%9C+%ED%8C%A8%EB%B0%80%EB%A6%AC%EC%95%84"
    # Set url - newtoki
    site_url = "https://newtoki.biz/manhwa"
    list_url = f"{site_url}/6068"
    # site_url = "https://newtoki.biz/webtoon"
    # list_url = f"{site_url}/6068"

    # site_url = "https://www.mangaread.org/manga"
    # list_url = f"{site_url}/tokyo-manji-revengers"

    site_url = "https://ww1.readtokyorevengers.net"
    list_url = f"{site_url}/manga/tokyo-revengers"

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

    # Filter files
    # for key in json_data["vol_info"].keys():
    #     if json_data["vol_info"][key].get("img_url") is None:
    #         continue

    #     files = []
    #     for img_url in json_data["vol_info"][key]["img_url"]:
    #         if (".gif" in img_url) or ("pp.userapi.com" in img_url):
    #             continue
    #         else:
    #             files.append(img_url)

    #     json_data["vol_info"][key]["img_url"] = files

    # with open(json_path, "w", encoding="utf-8") as f:
    #     json.dump(json_data, f, ensure_ascii=False, indent=4)

    # Check filter
    json_data["tag_list"].append("Tokyo Revengers Chapter")

    for key in json_data["vol_info"].keys():
        tags = json_data["tag_list"]
        name = filter_title(key, tags)
        print(name)
        if name == key:
            print(key)
            pass

    # Check list
    num_need_to_search = 0
    for key in json_data["vol_info"].keys():
        if json_data["vol_info"][key].get("img_url") is None:
            num_need_to_search += 1
            print(key)
    num_vol = len(json_data["vol_info"].keys())
    print(f"Number of volumes need to search: {num_need_to_search}/{num_vol}")

    # return
    download_images(json_data, base_dir, site_url)


if __name__ == "__main__":
    main()

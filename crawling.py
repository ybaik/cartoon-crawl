# -*- coding: utf-8 -*-

import os
import re
import json
import shutil
import urllib3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def main():

    name = "귀멸의 칼날"
    # base_path = f"D:/comix/기타작업/{name}"
    base_path = f"D:/comix/download0"
    # tag = "(ONE OUTS)"
    # tag1 = "(ONE O…UTS)"

    # extract episodes
    site_address = "http://156.239.152.53:9200/bbs"
    list_address = f"{site_address}/board.php?bo_table=toons&stx=%EA%B7%80%EB%A9%B8%EC%9D%98%20%EC%B9%BC%EB%82%A0&is=3737"
    source = requests.get(list_address).text

    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("button.episode")

    # episode-wise operation
    for i, key in enumerate(hotKeys, start=1):
        # if i not in [71, 68]:
        #     continue
        # extract episode title
        title = key.select_one(".episode-title").get_text()
        title = title.replace(name, "").strip()
        # title = title.replace(tag, "").strip()
        # title = title.replace(tag1, "").strip()

        print(f"{i}/{len(hotKeys)}: {title}")
        # continue
        save_base_path = f"{base_path}/{title}"
        # if os.path.isdir(save_base_path):
        #     continue
        os.makedirs(save_base_path, exist_ok=True)

        # extract episode target page
        target = key.get("onclick").replace("location.href='.", site_address)
        target_address = target[:-1]
        # print(target_address)

        # extract image list
        target = requests.get(target_address).text
        matched = re.search("var img_list = (.+?);", target, re.S)
        json_string = matched.group(1)
        img_list = json.loads(json_string)
        # print(frame_list)

        # download frame list
        http = urllib3.PoolManager()
        idx = 1
        for url in tqdm(img_list):
            ext = url.split(".")[-1]
            dst = f"{save_base_path}/{idx:03d}.{ext}"
            with http.request("GET", url, preload_content=False) as r, open(
                dst, "wb"
            ) as out_file:
                shutil.copyfileobj(r, out_file)
            idx += 1


if __name__ == "__main__":
    main()

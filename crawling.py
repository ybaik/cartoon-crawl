# -*- coding: utf-8 -*-

import os
import re
import json
import shutil
import urllib3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from fake_useragent import UserAgent
import ssl
import time


def main():

    ssl._create_default_https_context = ssl._create_unverified_context

    name = "카페 알파"
    base_path = f"D:/comix/기타작업/{name}"
    tags = [name]
    # tags.append("…코하마 지점")
    # tags.append("페이트 그랜드 오더…앤솔로지")

    # extract episodes
    site_address = "http://156.239.152.53:9200/bbs"
    list_address = f"{site_address}/board.php?bo_table=toons&stx=%EC%B9%B4%ED%8E%98%20%EC%95%8C%ED%8C%8C&is=2962"

    user_agent = UserAgent()
    headers = {"User-Agent": user_agent.random}
    source = requests.get(list_address, headers=headers).text

    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("button.episode")

    # episode-wise operation
    for i, key in enumerate(hotKeys, start=1):
        # if i != 3:
        #     continue

        # extract episode title
        title = key.select_one(".episode-title").get_text()
        for tag in tags:
            title = title.replace(tag, "").strip()

        print(f"{i}/{len(hotKeys)}: {title}")
        # continue
        save_base_path = f"{base_path}/{title}"
        if os.path.isdir(save_base_path):
            continue
        os.makedirs(save_base_path, exist_ok=True)

        # extract episode target page
        target = key.get("onclick").replace("location.href='.", site_address)
        target_address = target[:-1]
        # print(target_address)

        # extract image list
        target = requests.get(target_address).text
        matched = re.search("var img_list = (.+?);", target, re.S)
        if matched is None:
            print(1)
        json_string = matched.group(1)
        img_list = json.loads(json_string)
        # print(frame_list)

        # download frame list
        http = urllib3.PoolManager()
        idx = 1
        for url in tqdm(img_list):
            ext = url.split(".")[-1]
            dst = f"{save_base_path}/{idx:03d}.{ext}"

            if not os.path.exists(dst):
                with http.request(
                    "GET", url, preload_content=False, headers=headers
                ) as r, open(dst, "wb") as out_file:
                    shutil.copyfileobj(r, out_file)
            idx += 1
        time.sleep(1)


if __name__ == "__main__":
    main()

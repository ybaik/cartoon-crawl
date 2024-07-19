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

    name = "a"
    base_path = f"D:/comix/etc/{name}"
    tags = [name]
    tags.append("피안도 48일 후")

    # tags.append("원피스")
    # tags.append("(ONE PI…ECE)")
    # tags.append("(ONE PI…CE)")
    # tags.append("(ONE PIECE)")

    # extract episodes
    site_address = "https://www.11toon128.com/bbs"
    list_address = f"{site_address}/board.php?bo_table=toons&stx=%ED%94%BC%EC%95%88%EB%8F%84%2048%EC%9D%BC%20%ED%9B%84&is=20182"
    user_agent = UserAgent()
    headers = {"User-Agent": user_agent.random}
    source = requests.get(list_address, headers=headers).text

    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("button.episode")

    # episode-wise operation
    for i, key in enumerate(hotKeys, start=1):
        # if i > 1:
        #     continue
        if i > 20:
            continue
        # if i not in [4]:
        #     continue

        # extract episode title
        title = key.select_one(".episode-title").get_text()
        for tag in tags:
            title = title.replace(tag, "").strip()

        # print(i, title)
        # continue

        save_base_path = f"{base_path}/{title}"
        if not os.path.isdir(save_base_path):
            os.makedirs(save_base_path, exist_ok=True)
        else:
            # check number of files
            files = os.listdir(save_base_path)
            cnt = 0
            for file in files:
                name, ext = os.path.splitext(file)
                if ext == ".jpg":
                    cnt += 1
            if cnt >= 15:
                continue
        print(f"{i}/{len(hotKeys)}: {title}")

        # extract episode target page
        target = key.get("onclick").replace("location.href='.", site_address)
        target_address = target[:-1]
        # print(target_address)

        # extract image list
        target = requests.get(target_address).text

        # with open("d:/text.txt", "w", encoding="UTF-8") as f:
        #     f.write(target)

        # matched = re.search("var img_list_2 = (.+?);", target, re.S)
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

            if ext not in ["jpg", "JPG", "jpeg", "JPEG"]:
                ext = "jpg"

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

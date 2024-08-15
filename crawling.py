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
    # ssl._create_default_https_context = ssl._create_unverified_context

    name = "a"
    base_path = f"c:/comix/etc/{name}"
    tags = [name]
    tags.append("스파이")

    # Extract episodes
    site_url = "https://11toon.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%EC%8A%A4%ED%8C%8C%EC%9D%B4+%ED%8C%A8%EB%B0%80%EB%A6%AC%28SPY+X+FAMILY%29&is=12725&sord=&type=&page=2"
    user_agent = UserAgent()
    headers = {"User-Agent": user_agent.random}
    source = requests.get(list_url, headers=headers)

    # Page parsing
    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("button.episode")

    # episode-wise operation
    for i, key in enumerate(reversed(hotKeys), start=1):
        # for i, key in enumerate(hotKeys, start=1):
        # if i < 11:
        #     continue
        # if i > 20:
        #     continue
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
        target = key.get("onclick").replace("location.href='.", site_url)
        target_address = target[:-1]
        # print(target_address)

        # extract image list
        headers = {"User-Agent": user_agent.random}
        target = requests.get(target_address, headers=headers).text

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
                headers = {"User-Agent": user_agent.random}
                with http.request(
                    "GET", url, preload_content=False, headers=headers
                ) as r, open(dst, "wb") as out_file:
                    shutil.copyfileobj(r, out_file)
            idx += 1
        time.sleep(1)


if __name__ == "__main__":
    main()

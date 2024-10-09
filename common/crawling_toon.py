import re
import json
import time
import random
import shutil
import urllib3
import requests

from tqdm import tqdm
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def filter_title(title: str, tags: List) -> str:
    # Remove text in ()
    s = title.find("(")
    e = title.find(")")
    if s != e:
        tag = title[s : e + 1]
        title = title.replace(tag, "")

    # Apply additional filtering using given tags
    for tag in tags:
        title = title.replace(tag, "").strip()

    return title


def crawling_vols(
    site_url: str, list_url: str, json_data: Dict, json_path: Path
) -> bool:
    if len(json_data.keys()) != 0:
        return

    print("Volumn crawling has started...")
    print(list_url)

    user_agent = UserAgent()

    headers = {
        "User-Agent": user_agent.random,
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
        # "Accept-Language": "ko-KR,ko;q=0.9,en;q=0.8"
    }
    source = requests.get(list_url, headers=headers)

    # For debugging
    # with open("c:/comix/text.txt", "w", encoding="UTF-8") as f:
    #     f.write(source.text)

    # Page parsing
    soup = BeautifulSoup(source.text, "html.parser")
    hotKeys = soup.select("button.episode")
    for key in hotKeys:
        title = key.select_one(".episode-title").get_text()
        vol_url = key.get("onclick").replace("location.href='.", site_url)[:-1]
        if json_data.get(title) is None:
            json_data[title] = dict()
        json_data[title]["vol_url"] = vol_url

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def crawling_img_list(json_data: Dict, json_path: Path) -> None:

    # Check if there is file-wise url exists
    need_crawling_img_list = False
    for vol in json_data.values():
        if vol.get("img_url") is None:
            need_crawling_img_list = True
            break

    if not need_crawling_img_list:
        return

    print("Image list crawling has started...")

    user_agent = UserAgent()

    for k, v in json_data.items():
        if not v.get("img_url") is None:
            continue

        # Get page
        headers = {"User-Agent": user_agent.random}
        target = requests.get(v.get("vol_url"), headers=headers).text
        matched = re.search("var img_list = (.+?);", target, re.S)
        if matched is not None:
            json_string = matched.group(1)
            img_list = json.loads(json_string)
            json_data[k]["img_url"] = img_list

            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)


def download_images(json_data: Dict, save_base_dir: Path, tags: List) -> None:
    http = urllib3.PoolManager()
    user_agent = UserAgent()

    for k, v in json_data.items():
        print(k)
        name = filter_title(k, tags)

        # print(name)
        # continue

        save_dir = save_base_dir / name
        if not save_dir.exists():
            save_dir.mkdir()
        else:
            # check number of files
            files = [p for p in save_dir.glob("*.*")]
            if len(files) >= 15:
                continue
        # Download images
        idx = 1
        for img_url in tqdm(v["img_url"]):
            ext = img_url.split(".")[-1]
            if ext not in ["jpg", "JPG", "jpeg", "JPEG"]:
                ext = "jpg"
            dst_path = save_dir / f"{idx:03d}.{ext}"

            if not dst_path.exists():
                headers = {"User-Agent": user_agent.random}
                with http.request(
                    "GET", img_url, preload_content=False, headers=headers
                ) as r, open(dst_path, "wb") as out_file:
                    shutil.copyfileobj(r, out_file)
            idx += 1
        time.sleep(random.uniform(1, 2))

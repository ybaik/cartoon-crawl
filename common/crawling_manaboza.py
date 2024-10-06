import json
import requests

from pathlib import Path
from typing import Dict
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def crawling_vols(
    site_url: str, list_url: str, json_data: Dict, json_path: Path
) -> bool:
    if len(json_data.keys()) != 0:
        return

    print("Volumn crawling has started...")
    print(list_url)

    user_agent = UserAgent()
    headers = {"User-Agent": user_agent.random}
    source = requests.get(list_url, headers=headers)

    # Page parsing
    soup = BeautifulSoup(source.text, "html.parser")
    hotKeys = soup.select("a.flex-container")
    for key in hotKeys:
        title = key.select_one(".episode-title").get_text().strip()

        # extract episode target page
        target = key.get("data-episode-id")
        target_address = list_url.replace("ep_list", "ep_view")
        # target_address = target_address[:-2]
        vol_url = f"{target_address}/{target}"

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
        soup = BeautifulSoup(target, "html.parser")
        hotKeys = soup.select("img.document_img")

        img_list = []
        for key_sub in hotKeys:
            img_list.append(key_sub["data-src"])

        if len(img_list):
            json_data[k]["img_url"] = img_list
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, ensure_ascii=False, indent=4)

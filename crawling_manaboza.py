# -*- coding: utf-8 -*-
import os
import shutil
import urllib3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from fake_useragent import UserAgent
import ssl


def main():

    ssl._create_default_https_context = ssl._create_unverified_context

    base_path = "D:/comix/etc/바질리스크 오우카인법첩"
    # tag = "베르세르크_"
    # extract episodes
    site_address = "http://manaboza74.com/comic/ep_list/12777"
    list_address = f"{site_address}"

    user_agent = UserAgent()
    headers = {"User-Agent": user_agent.random}
    source = requests.get(list_address, headers=headers).text
    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("a.flex-container")

    # # episode-wise operation
    for i, key in enumerate(hotKeys, start=1):
        # if i != 3:
        #     continue

        # extract episode title
        title = key.select_one(".episode_stitle").get_text().strip()
        # title = title.replace(tag, "")
        # print(title)
        # if title not in [
        #     "33권",
        # ]:
        # continue

        print(f"{i}/{len(hotKeys)}: {title}")

        save_base_path = f"{base_path}/{title}"
        # if os.path.isdir(save_base_path):
        #     continue
        # os.makedirs(save_base_path, exist_ok=True)

        # extract episode target page
        target = key.get("data-episode-id")
        target_address = site_address.replace("ep_list", "ep_view")
        # target_address = target_address[:-2]
        target_address = f"{target_address}/{target}"

        print(target_address)

        # extract image list
        target_sub = requests.get(target_address).text
        soup_sub = BeautifulSoup(target_sub, "html.parser")
        hotKeys_sub = soup_sub.select("img.document_img")

        img_list = []
        for key_sub in hotKeys_sub:
            img_list.append(key_sub["data-src"])

        # download frame list
        http = urllib3.PoolManager()
        idx = 1
        for url in tqdm(img_list):
            # print(f"{j} /{len(img_list)}")
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


if __name__ == "__main__":
    main()

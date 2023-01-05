# -*- coding: utf-8 -*-
import os
import shutil
import urllib3
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def main():

    base_path = "D:\comix\기타작업\창천항로"
    # tag = "귀멸의\xa0칼날 "
    # extract episodes
    site_address = "https://www.manaboza16.com/comic/ep_list/3748"
    list_address = f"{site_address}"

    source = requests.get(list_address).text
    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("a.flex-container")

    # # episode-wise operation
    for i, key in enumerate(hotKeys, start=1):

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
        if os.path.isdir(save_base_path):
            continue
        os.makedirs(save_base_path, exist_ok=True)

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
            dst = f"{save_base_path}/{idx:03d}.{ext}"

            if not os.path.exists(dst):
                with http.request("GET", url, preload_content=False) as r, open(
                    dst, "wb"
                ) as out_file:
                    shutil.copyfileobj(r, out_file)
            idx += 1


if __name__ == "__main__":
    main()

import os
import re
import json
import shutil
import urllib3
import requests
from bs4 import BeautifulSoup


def main():

    base_path = "D:/comix/download1"
    # extract episodes
    site_address = "http://www.manaboza16.com/comic/ep_list/3606"
    list_address = f"{site_address}"

    source = requests.get(list_address).text
    soup = BeautifulSoup(source, "html.parser")
    hotKeys = soup.select("a.flex-container")

    # # episode-wise operation
    for i, key in enumerate(hotKeys, start=1):

        #     # extract episode title
        title = key.select_one(".episode_stitle").get_text().strip()
        if title not in ["06권"]:
            continue

        print(f"{i}/{len(hotKeys)}: {title}")

        save_base_path = f"{base_path}/{title}"
        if os.path.isdir(save_base_path):
            continue
        os.makedirs(save_base_path, exist_ok=True)

        # extract episode target page
        target = key.get("data-episode-id")
        target_address = site_address.replace("ep_list", "ep_view")
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
        for j, url in enumerate(img_list, start=1):
            print(f"{j} /{len(img_list)}")
            ext = url.split(".")[-1]
            dst = f"{save_base_path}/{j:03d}.{ext}"
            # urlretrieve(url, dst)
            with http.request("GET", url, preload_content=False) as r, open(
                dst, "wb"
            ) as out_file:
                shutil.copyfileobj(r, out_file)


if __name__ == "__main__":
    main()

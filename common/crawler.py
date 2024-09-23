# -*- coding: utf-8 -*-
import re
import json
import time
import binascii

from tqdm import tqdm
from pathlib import Path
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


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


class SeleniumCrawler:
    def __init__(
        self,
        headless: bool = False,
        driver_path: str = "c:/work/chromedriver-win64/chromedriver.exe",
        profile_path: str = "C:/Users/hyunx/AppData/Local/Google/Chrome/User Data",
    ) -> None:
        service = Service(executable_path=driver_path)
        options = Options()

        # Set basic options
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Set options selectively
        if headless:
            options.add_argument("--headless")
        else:
            options.add_argument(f"user-data-dir={profile_path}")
            options.add_argument("--remote-debugging-port=9222")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(service=service, options=options)

    def deinit(self):
        self.driver.quit()


class SeleniumCrawlerToon(SeleniumCrawler):
    def crawling_vols(
        self, site_url: str, list_url: str, json_data: Dict, json_path: Path
    ) -> None:
        if len(json_data.keys()) != 0:
            return

        print("Volumn crawling has started...")
        print(list_url)

        # Open page
        self.driver.get(url=list_url)
        poses = self.driver.find_elements(
            By.XPATH, '//*[@id="comic-episode-list"]/li/button'
        )
        for p in poses:
            title = p.find_element(By.CLASS_NAME, "episode-title").text
            vol_url = p.get_attribute("onclick").replace("location.href='.", site_url)[
                :-1
            ]
            if json_data.get(title) is None:
                json_data[title] = dict()
            json_data[title]["vol_url"] = vol_url

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def crawling_img_list(self, json_data: Dict, json_path: Path) -> None:

        # Check if there is file-wise url exists
        need_crawling_img_list = False
        for vol in json_data.values():
            if vol.get("img_url") is None:
                need_crawling_img_list = True
                break

        if not need_crawling_img_list:
            return

        print("Image list crawling has started...")
        for k, v in json_data.items():
            if not v.get("img_url") is None:
                continue

            # Open page
            self.driver.get(url=v.get("vol_url"))

            # Find image url list
            p_id = self.driver.find_elements(By.TAG_NAME, "script")
            for script in p_id:
                innerHTML = script.get_property("innerHTML")
                matched = re.search("var img_list = (.+?);", innerHTML, re.S)
                if matched is not None:
                    json_string = matched.group(1)
                    img_list = json.loads(json_string)
                    json_data[k]["img_url"] = img_list

                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=4)
                    break


class SeleniumCrawlerToki(SeleniumCrawler):
    def crawling_vols(self, list_url: str, json_data: Dict, json_path: Path) -> None:
        if len(json_data.keys()) != 0:
            return

        print("Volumn crawling has started...")
        print(list_url)

        # Open page
        self.driver.get(url=list_url)
        poses = self.driver.find_elements(By.XPATH, '//*[@id="serial-move"]/div/ul/li')
        for p in poses:
            tag = p.find_element(By.TAG_NAME, "a")
            # title
            title = tag.text

            if "권 " in title:
                title = title[: title.find("권") + 1]
            if "화 " in title:
                title = title[: title.find("화") + 1]
            vol_url = tag.get_attribute("href")
            if json_data.get(title) is None:
                json_data[title] = dict()
            json_data[title]["vol_url"] = vol_url

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def crawling_img_list(self, json_data: Dict, json_path: Path) -> None:

        # Check if there is file-wise url exists
        need_crawling_img_list = False
        for vol in json_data.values():
            if vol.get("img_url") is None:
                need_crawling_img_list = True
                break

        if not need_crawling_img_list:
            return

        print("Image list crawling has started...")

        for k, v in json_data.items():
            if not v.get("img_url") is None:
                continue

            # Open page
            self.driver.get(url=v.get("vol_url"))

            # Find image url list
            p_id = self.driver.find_elements(By.TAG_NAME, "script")
            for script in p_id:
                type = script.get_attribute("type")
                language = script.get_attribute("language")

                if type == "text/javascript" and language == "Javascript":
                    innerHTML = script.get_property("innerHTML")
                    pattern = r"html_data\+='([0-9A-Fa-f.]+)';"
                    matches = re.findall(pattern, innerHTML)
                    if not len(matches):
                        continue

                    clean_hex_string = ""
                    for match in matches:
                        clean_hex_string += match.replace(".", "")

                    bytes_data = binascii.unhexlify(clean_hex_string)
                    text = bytes_data.decode("utf-8")

                    pattern = r"https://.*?\.jpg"
                    jpg_urls = re.findall(pattern, text)

                    json_data[k]["img_url"] = jpg_urls

                    with open(json_path, "w", encoding="utf-8") as f:
                        json.dump(json_data, f, ensure_ascii=False, indent=4)
                    break

    def download_images(self, json_data: Dict, save_base_dir: Path, tags: List) -> None:

        for k, v in json_data.items():
            print(k)
            name = filter_title(k, tags)

            self.driver.get(url=v["vol_url"])

            p_id = self.driver.find_elements(By.TAG_NAME, "img")
            for script in p_id:
                print(1)

            cnt = 0
            for img_url in tqdm(v["img_url"]):

                if cnt < 10:
                    cnt += 1
                    continue

                self.driver.get(url=img_url)
                print(1)

            # continue

            # save_dir = save_base_dir / name
            # if not save_dir.exists():
            #     save_dir.mkdir()
            # else:
            #     # check number of files
            #     files = [p for p in save_dir.glob("*.*")]
            #     if len(files) >= 15:
            #         continue

            # # Download images
            # idx = 1
            # for img_url in tqdm(v["img_url"]):
            #     ext = img_url.split(".")[-1]
            #     if ext not in ["jpg", "JPG", "jpeg", "JPEG"]:
            #         ext = "jpg"
            #     dst_path = save_dir / f"{idx:03d}.{ext}"
            #     if not dst_path.exists():
            #         headers = {"User-Agent": user_agent.random}
            #         with http.request(
            #             "GET", img_url, preload_content=False, headers=headers
            #         ) as r, open(dst_path, "wb") as out_file:
            #             shutil.copyfileobj(r, out_file)
            #         print(1)

            #     break
            #     idx += 1
            # break
            # time.sleep(1)

# -*- coding: utf-8 -*-
import re
import json
import time
import random
import shutil
import urllib3
import binascii

from tqdm import tqdm
from pathlib import Path
from typing import List, Dict
from abc import abstractmethod

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


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
            # Check number of files
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


def create_crawler(site_url: str, use_selenium: bool):

    if not use_selenium:
        if "11toon" in site_url:
            return Crawler11toon(site_url=site_url)
        elif "manaboza" in site_url:
            return CrawlerManaboza(site_url=site_url)
    else:
        if "11toon" in site_url:
            return SeleniumCrawler11toon(site_url=site_url, headless=True)
        elif "manaboza" in site_url:
            return SeleniumCrawlerManaboza(site_url=site_url, headless=True)
        elif "manatoki" in site_url:
            return SeleniumCrawlerManatoki(site_url=site_url, headless=False)
    return None


class Crawler:
    def __init__(self, site_url: str):
        self.site_url = site_url
        self.response = None

    def open_page(self, url: str) -> None:
        user_agent = UserAgent()
        headers = {"User-Agent": user_agent.random}
        self.response = requests.get(url, headers=headers)
        time.sleep(random.uniform(1, 2))

    def deinit(self):
        pass

    @staticmethod
    def save_json(json_path: Path, json_data: Dict) -> None:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    def crawling_vols(self, list_url: str, json_data: Dict, json_path: Path) -> None:
        if len(json_data.keys()) != 0:
            return

        # Open page
        self.open_page(url=list_url)

        # Extract information using site-specific methods
        print("Volumn crawling has started...")
        self.site_wise_crawling_vols(list_url=list_url, json_data=json_data)
        print("Volumn crawling is complete...")

        # Save the extracted information
        self.save_json(json_path, json_data)

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
        for k, v in tqdm(json_data.items()):
            if not v.get("img_url") is None:
                continue

            # Open page
            self.open_page(url=v.get("vol_url"))

            # Find image url list
            img_list = self.site_wise_crawling_img_list()
            if len(img_list):
                json_data[k]["img_url"] = img_list
                self.save_json(json_path, json_data)
        print("Image list crawling is complete...")

    @abstractmethod
    def site_wise_crawling_vols(self, list_url: str, json_data: Dict) -> None:
        pass

    @abstractmethod
    def site_wise_crawling_img_list(self) -> List:
        pass


class Crawler11toon(Crawler):
    def site_wise_crawling_vols(self, list_url: str, json_data: Dict) -> None:
        soup = BeautifulSoup(self.response.text, "html.parser")
        items = soup.select(".episode.is-series")
        for item in items:
            title = item.select_one(".episode-title.ellipsis").get_text()
            # title = item.select_one(".episode-title").text

            vol_url = item.attrs["onclick"].replace("location.href='.", self.site_url)[
                :-1
            ]
            # vol_url = item.attrs["onclick"].replace("location.href='.", self.site_url)[:-1]

            if json_data.get(title) is None:
                json_data[title] = dict()
            json_data[title]["vol_url"] = vol_url

    def site_wise_crawling_img_list(self) -> List:
        matched = re.search("var img_list = (.+?);", self.response.text, re.S)
        if matched is not None:
            json_string = matched.group(1)
            img_list = json.loads(json_string)
            return img_list
        return []


class CrawlerManaboza(Crawler):
    def site_wise_crawling_vols(self, list_url: str, json_data: Dict) -> None:
        soup = BeautifulSoup(self.response.text, "html.parser")
        items = soup.select(".flex-container.episode-items")
        for item in items:
            title = item.select_one(".episode_stitle").text.strip()
            target = item.attrs["data-episode-id"]
            target_address = list_url.replace("ep_list", "ep_view")
            vol_url = f"{target_address}/{target}"

            if json_data.get(title) is None:
                json_data[title] = dict()
            json_data[title]["vol_url"] = vol_url

    def site_wise_crawling_img_list(self) -> List:
        img_list = []
        soup = BeautifulSoup(self.response.text, "html.parser")
        items = soup.select(".document_img")
        for item in items:
            img_list.append(item.attrs["data-src"])
        return img_list


class SeleniumCrawler(Crawler):
    def __init__(
        self,
        site_url: str,
        headless: bool = False,
        profile_path: str = "C:/Users/hyunx/AppData/Local/Google/Chrome/User Data",
    ) -> None:
        self.site_url = site_url
        self.driver = None
        self.options = Options()

        # Set basic options
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-blink-features=AutomationControlled")

        # For debugging
        self.options.add_experimental_option("detach", True)  # Prevent auto-shutdown

        # Set options selectively
        if headless:
            self.options.add_argument("--headless=new")
            self.options.add_argument("--ignore-ssl-errors")
        else:
            self.options.add_argument(f"user-data-dir={profile_path}")
            # self.options.add_argument("--remote-debugging-port=9222")
            # self.options.add_experimental_option(
            #     "excludeSwitches", ["enable-automation"]
            # )
            # self.options.add_experimental_option("useAutomationExtension", False)

    def deinit(self):
        if self.driver is not None:
            self.driver.quit()

    def open_page(self, url: str) -> None:
        if self.driver is None:
            self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(url=url)
        time.sleep(random.uniform(1, 2))


class SeleniumCrawler11toon(SeleniumCrawler):
    def site_wise_crawling_vols(self, list_url: str, json_data: Dict) -> None:
        poses = self.driver.find_elements(
            By.XPATH, '//*[@id="comic-episode-list"]/li/button'
        )
        for p in poses:
            title = p.find_element(By.CLASS_NAME, "episode-title").text
            vol_url = p.get_attribute("onclick").replace(
                "location.href='.", self.site_url
            )[:-1]
            if json_data.get(title) is None:
                json_data[title] = dict()
            json_data[title]["vol_url"] = vol_url

    def site_wise_crawling_img_list(self) -> List:
        p_id = self.driver.find_elements(By.TAG_NAME, "script")
        for script in p_id:
            innerHTML = script.get_property("innerHTML")
            matched = re.search("var img_list = (.+?);", innerHTML, re.S)
            if matched is not None:
                json_string = matched.group(1)
                img_list = json.loads(json_string)
                return img_list
        return []


class SeleniumCrawlerManaboza(SeleniumCrawler):
    def site_wise_crawling_vols(self, list_url: str, json_data: Dict):
        poses = self.driver.find_elements(By.CLASS_NAME, "flex-container")
        for p in poses:
            title = p.find_element(By.CLASS_NAME, "episode_stitle").text
            target = p.get_attribute("data-episode-id")
            target_address = list_url.replace("ep_list", "ep_view")
            vol_url = f"{target_address}/{target}"
            if json_data.get(title) is None:
                json_data[title] = dict()
            json_data[title]["vol_url"] = vol_url

    def site_wise_crawling_img_list(self) -> List:
        img_list = []
        ps = self.driver.find_elements(By.CLASS_NAME, "document_img")
        for p in ps:
            url = p.get_attribute("data-src")
            img_list.append(url)
        return img_list


class SeleniumCrawlerManatoki(SeleniumCrawler):
    def site_wise_crawling_vols(self, list_url: str, json_data: Dict) -> None:
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

    def site_wise_crawling_img_list(self) -> List:
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

                return jpg_urls

        return []

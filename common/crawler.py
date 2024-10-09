# -*- coding: utf-8 -*-
import re
import json
import time
import random
import binascii

from tqdm import tqdm
from pathlib import Path
from typing import List, Dict
from abc import abstractmethod

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


def create_crawler(site_url: str):

    if "11toon" in site_url:
        return SeleniumCrawler11toon(site_url=site_url, headless=True)
    elif "manaboza" in site_url:
        return SeleniumCrawlerManaboza(site_url=site_url, headless=True)
    elif "manatoki" in site_url:
        return SeleniumCrawlerManatoki(site_url=site_url, headless=False)
    return None


class SeleniumCrawler:
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

    def check_driver(self):
        if self.driver is None:
            self.driver = webdriver.Chrome(options=self.options)

    def deinit(self):
        if self.driver is not None:
            self.driver.quit()

    def crawling_vols(self, list_url: str, json_data: Dict, json_path: Path) -> None:
        if len(json_data.keys()) != 0:
            return

        # Open page
        print(list_url)
        self.check_driver()
        self.driver.get(url=list_url)
        time.sleep(random.uniform(1, 2))

        # Extract information using site-specific methods
        print("Volumn crawling has started...")
        self.site_wise_crawling_vols(list_url=list_url, json_data=json_data)
        print("Volumn crawling is complete...")

        # Save the extracted information
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    @abstractmethod
    def site_wise_crawling_vols(self, list_url: str, json_data: Dict) -> None:
        pass

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
        self.check_driver()
        for k, v in tqdm(json_data.items()):
            if not v.get("img_url") is None:
                continue

            # Open page
            self.driver.get(url=v.get("vol_url"))
            time.sleep(random.uniform(1, 2))

            # Find image url list
            self.site_wise_crawling_img_list(k, json_data, json_path)
        print("Image list crawling is complete...")

    @abstractmethod
    def site_wise_crawling_img_list(
        self, key: str, json_data: Dict, json_path: Path
    ) -> None:
        pass


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

    def site_wise_crawling_img_list(
        self, key: str, json_data: Dict, json_path: Path
    ) -> None:

        p_id = self.driver.find_elements(By.TAG_NAME, "script")
        for script in p_id:
            innerHTML = script.get_property("innerHTML")
            matched = re.search("var img_list = (.+?);", innerHTML, re.S)
            if matched is not None:
                json_string = matched.group(1)
                img_list = json.loads(json_string)
                json_data[key]["img_url"] = img_list

                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                break


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

    def site_wise_crawling_img_list(
        self, key: str, json_data: Dict, json_path: Path
    ) -> None:
        img_list = []
        ps = self.driver.find_elements(By.CLASS_NAME, "document_img")
        for p in ps:
            url = p.get_attribute("data-src")
            img_list.append(url)

        if len(img_list):
            json_data[key]["img_url"] = img_list

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)


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

    def site_wise_crawling_img_list(
        self, key: str, json_data: Dict, json_path: Path
    ) -> None:
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

                json_data[key]["img_url"] = jpg_urls

                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=4)
                break

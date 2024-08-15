import re
import json
import time
import shutil
import urllib3
from typing import List, Dict
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from fake_useragent import UserAgent


def filter_name(name: str, tags: List) -> str:

    # Remove text in ()
    s = name.find("(")
    e = name.find(")")
    if s != e:
        tag = name[s : e + 1]
        name = name.replace(tag, "")

    # Apply additional tags
    for tag in tags:
        name = name.replace(tag, "").strip()
    return name


def crawling_vols(site_url: str, list_url: str, json_data: Dict) -> None:
    driver_path = "c:/work/chromedriver-win64/chromedriver.exe"
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(service=service, options=options)

    # Open page
    driver.get(url=list_url)

    poses = driver.find_elements(By.XPATH, '//*[@id="comic-episode-list"]/li/button')
    for p in poses:
        title = p.find_element(By.CLASS_NAME, "episode-title").text
        vol_url = p.get_attribute("onclick").replace("location.href='.", site_url)[:-1]
        if json_data.get(title) is None:
            json_data[title] = dict()
        json_data[title]["vol_url"] = vol_url

    driver.quit()


def crawling_img_list(json_data: Dict) -> None:

    driver_path = "c:/work/chromedriver-win64/chromedriver.exe"
    service = Service(executable_path=driver_path)
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(service=service, options=options)

    for k, v in json_data.items():
        if not v.get("img_list") is None:
            continue

        # Open page
        driver.get(url=v.get("vol_url"))

        # Find image url list
        p_id = driver.find_elements(By.TAG_NAME, "script")
        for script in p_id:
            innerHTML = script.get_property("innerHTML")
            matched = re.search("var img_list = (.+?);", innerHTML, re.S)
            if matched is not None:
                json_string = matched.group(1)
                img_list = json.loads(json_string)
                json_data[k]["img_url"] = img_list
                break

    driver.quit()


def main():

    # Set path
    title = "a"
    base_dir = Path(f"c:/comix/etc/{title}")
    json_path = base_dir / "info.json"

    # Set url
    site_url = "https://11toon130.com/bbs"
    list_url = f"{site_url}/board.php?bo_table=toons&stx=%EC%8A%A4%ED%8C%8C%EC%9D%B4+%ED%8C%A8%EB%B0%80%EB%A6%AC%28SPY+X+FAMILY%29&is=12725&sord=&type=&page=2"

    tags = []
    tags.append("스파이")
    tags.append("패밀리")

    # Read url list
    if json_path.exists():
        with open(json_path, encoding="utf-8") as f:
            json_data = json.load(f)
    else:
        json_data = dict()

    # Check if volumne-wise url exists
    need_crawling_vols = False
    if len(json_data.keys()) == 0:
        need_crawling_vols = True

    # Extract voulumn-wise url information via crawling
    if need_crawling_vols:
        crawling_vols(site_url, list_url, json_data)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    # Check if there is file-wise url exists
    need_crawling_img_list = False
    for vol in json_data.values():
        if vol.get("img_url") is None:
            need_crawling_img_list = True
            break

    # Extract image-wise url information via crawling
    if need_crawling_img_list:
        crawling_img_list(json_data)
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

    # download frame list
    http = urllib3.PoolManager()
    user_agent = UserAgent()

    for k, v in json_data.items():
        name = filter_name(k, tags)
        save_dir = base_dir / name
        if not save_dir.exists():
            save_dir.mkdir()
        else:
            # check number of files
            files = [p for p in save_dir.glob("*.*")]
            if len(files) >= 15:
                continue
        # Download images
        idx = 1
        for img_url in v["img_url"]:
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
        time.sleep(1)


if __name__ == "__main__":
    main()

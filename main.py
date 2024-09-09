import os
import re
import requests
import cloudscraper
import argparse
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin

default_directory = "download"

class hentaipaw:
    ## maybe broked
    @staticmethod
    def extract_id(id):
        try:
            # URLかIDかを判別し、URLの場合はIDを抽出
            url_pattern = re.compile(r'https://ja\.hentaipaw\.com/articles/(\d+)')
            id_pattern = re.compile(r'(\d+)')

            match = url_pattern.search(id)
            if match:
                return match.group(1)

            # IDがURL形式でない場合も考慮
            match = id_pattern.search(id)
            if match:
                return match.group(1)
        except:
            print("[-] Failed to extract URL")
            return None

    @staticmethod
    def get_image_url(id):
        session = cloudscraper.create_scraper()  # cf bypass
        response = session.get(f"https://ja.hentaipaw.com/articles/{id}").content
        soup = BeautifulSoup(response, "html.parser")
        title = soup.find("title").text
        title = title.replace(" - エロモフ", "")
        elements = soup.find_all("div", class_="detail-gallery-item")
        # imgタグのsrc属性のURLを取得
        img_urls = []
        for element in elements:
            img_tag = element.find("img")
            if img_tag:
                img_url = urljoin(f"https://ja.hentaipaw.com/", img_tag["src"])  # This will handle relative URLs
                img_urls.append(img_url)

        return title, img_urls

    @staticmethod
    def download(id):
        id = hentaipaw.extract_id(id)
        if id is None:
            return
        
        title, img_urls = hentaipaw.get_image_url(id)
        base_dir = "hentaipaw"
        download_dir = os.path.join(default_directory, base_dir, id)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        print(f"[+] Downloading title: {title} page: {len(img_urls)}p")

        def download_image(url):
            tries = 3  # Number of retry attempts
            for attempt in range(tries):
                try:
                    response = requests.get(url)
                    response.raise_for_status()  # Raise an exception for bad status codes
                    filename = os.path.join(download_dir, os.path.basename(url))
                    with open(filename, 'wb') as file:
                        file.write(response.content)
                    return url, True
                except requests.RequestException:
                    print(f"[-] Error downloading {url}, attempt {attempt + 1} of {tries}")
                    if attempt == tries - 1:
                        return url, False

        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if not success:
                    print(f"[-] Failed to download {url}")

        print(f"[+] Download complete title: {title}")

class nyahentai:
    @staticmethod
    def extract_url(url):
        try:
            pattern = re.compile(r'https://nyahentai\.re/(\w+)/(\w+)/')
            match = pattern.search(url)

            if match:
                category = match.group(1)
                id = match.group(2)
                return category, id
            else:
                print("[-] Failed to extract URL")
                return None, None
        except:
            print("[-] Failed to extract URL")
            return None, None

    @staticmethod
    def get_image_url(url):
        session = requests.Session()
        response = session.get(url).content
        soup = BeautifulSoup(response, "html.parser")
        title = soup.find("title").text
        title = title.replace(" - エロ漫画 - NyaHentai", "")
        elements = soup.find_all("div", id="post-comic")
        # imgタグのsrc属性のURLを取得
        img_urls = []
        for element in elements:
            img_tags = element.find_all("img")
            for img_tag in img_tags:
                if img_tag.has_attr("src"):
                    img_urls.append(img_tag["src"])

        return title, img_urls

    @staticmethod
    def download(url):
        category, id = nyahentai.extract_url(url)
        if category is None or id is None:
            return

        compile_url = id + "-" + category
        title, img_urls = nyahentai.get_image_url(url)
        base_dir = "nyahentai"
        download_dir = os.path.join(default_directory, base_dir, compile_url)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        print(f"[+] Downloading title: {title} page: {len(img_urls)}p")

        def download_image(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                filename = os.path.join(download_dir, os.path.basename(url))
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return url, True
            except requests.RequestException:
                return url, False

        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if not success:
                    print(f"[-] Failed to download {url}")

        print(f"[+] Download complete title: {title}")

class momonga:
    @staticmethod
    def extract_url(url):
        try:
            pattern = re.compile(r'https://momon-ga\.com/(\w+)/(\w+)/')
            match = pattern.search(url)

            if match:
                category = match.group(1)
                id = match.group(2)
                return category, id
        except:
            print("[-] Failed to extract URL")
            return None, None

    @staticmethod
    def get_image_url(url):
        session = requests.Session()
        response = session.get(url).content
        soup = BeautifulSoup(response, "html.parser")
        title = soup.find("title").text
        title = title.replace(" - エロ漫画 momon:GA（モモンガッ!!）", "")
        elements = soup.find_all("div", id="post-hentai")
        # imgタグのsrc属性のURLを取得
        img_urls = []
        for element in elements:
            img_tags = element.find_all("img")
            for img_tag in img_tags:
                if img_tag.has_attr("src"):
                    img_urls.append(img_tag["src"])

        return title, img_urls

    @staticmethod
    def download(url):
        category, id = momonga.extract_url(url)
        if category is None or id is None:
            return

        compile_url = id + "-" + category
        title, img_urls = momonga.get_image_url(url)
        base_dir = "momonga"
        download_dir = os.path.join(default_directory, base_dir, compile_url)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        print(f"[+] Downloading title: {title} page: {len(img_urls)}p")

        def download_image(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                filename = os.path.join(download_dir, os.path.basename(url))
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return url, True
            except requests.RequestException:
                return url, False

        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if not success:
                    print(f"[-] Failed to download {url}")

        print(f"[+] Download complete title: {title}")

class dddsmart:
    ## maybe broked
    @staticmethod
    def extract_url(url):
        try:
            pattern = re.compile(r'https://ddd-smart\.net/top(\d+)-(\w+)')
            match = pattern.search(url)
            if match:
                category = match.group(1)
                id = match.group(2)
                return category, id
        except:
            print("[-] Failed to extract URL")
            return None, None

    @staticmethod
    def get_image_url(url):
        session = requests.Session()
        response = session.get(url).content
        soup = BeautifulSoup(response, "html.parser")
        title = soup.find("title").text
        title = title.replace(" - 同人すまーと", "")
        elements = soup.find_all("div", class_="comic-images")
        img_urls = []
        for element in elements:
            img_tags = element.find_all("img")
            for img_tag in img_tags:
                if img_tag.has_attr("src"):
                    img_urls.append(img_tag["src"])
        return title, img_urls

    @staticmethod
    def download(url):
        category, id = dddsmart.extract_url(url)
        if category is None or id is None:
            return

        compile_url = id + "-" + category
        title, img_urls = dddsmart.get_image_url(url)
        base_dir = "ddd-smart"
        download_dir = os.path.join(default_directory, base_dir, compile_url)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        print(f"[+] Downloading title: {title} page: {len(img_urls)}p")

        def download_image(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                filename = os.path.join(download_dir, os.path.basename(url))
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return url, True
            except requests.RequestException:
                return url, False

        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if not success:
                    print(f"[-] Failed to download {url}")

        print(f"[+] Download complete title: {title}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Doujinshi Downloader")
    parser.add_argument("url", help="URL of the doujinshi to download")
    args = parser.parse_args()

    # Call the appropriate function depending on the domain in the URL
    if "hentaipaw.com" in args.url:
        hentaipaw.download(args.url)
    elif "nyahentai.re" in args.url:
        nyahentai.download(args.url)
    elif "momon-ga.com" in args.url:
        momonga.download(args.url)
    elif "ddd-smart.net" in args.url:
        dddsmart.download(args.url)
    else:
        print(f"[-] Unsupported URL: {args.url}")
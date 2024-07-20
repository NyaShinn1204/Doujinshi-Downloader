import os
import re
import requests
import cloudscraper
from tqdm import tqdm
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

default_directory = "download"

class hentaipaw:
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
            print("[-] Failed extract URL")
            return

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
                img_urls.append(img_tag["src"])
            
        return title, img_urls
    
    def download(id):
        id = hentaipaw.extract_id(id)
        title, img_urls = hentaipaw.get_image_url(id)
                
        base_dir = "hentaipaw"
        download_dir = os.path.join(default_directory, base_dir, id)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        print(f"[+] Downloading title:{title} page:{len(img_urls)}p")
        
        def download_image(url):
            try:
                response = requests.get(url)
                response.raise_for_status()  # エラーがあれば例外を発生させる
                filename = os.path.join(download_dir, os.path.basename(url))
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return url, True
            except requests.RequestException as e:
                return url, False
        
        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if success != True:
                    print(f"[-] Failed to download {url}")
                    
        print(f"[+] Download complete title:{title}")

class nyahentai:
    def extract_url(url):
        try:
            pattern = re.compile(r'https://nyahentai\.re/(\w+)/(\w+)/')
            match = pattern.search(url)
            
            if match:
                category = match.group(1)
                id = match.group(2)
                return category, id
        except:
            print("[-] Failed extract URL")
            return

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
            img_tags = element.find_all("img")  # 修正: find_allに変更
            for img_tag in img_tags:
                if img_tag.has_attr("src"):
                    img_urls.append(img_tag["src"])
            
        return title, img_urls
    
    def download(url):
        category, id = nyahentai.extract_url(url)
        compile_url = id + "-" + category
        
        title, img_urls = nyahentai.get_image_url(url)
                
        base_dir = "nyahentai"
        download_dir = os.path.join(default_directory, base_dir, compile_url)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        print(f"[+] Downloading title:{title} page:{len(img_urls)}p")
        
        def download_image(url):
            try:
                response = requests.get(url)
                response.raise_for_status()  # エラーがあれば例外を発生させる
                filename = os.path.join(download_dir, os.path.basename(url))
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return url, True
            except requests.RequestException as e:
                return url, False
        
        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if success != True:
                    print(f"[-] Failed to download {url}")

        print(f"[+] Download complete title:{title}")
        
class momonga:
    def extract_url(url):
        try:
            pattern = re.compile(r'https://momon-ga\.com/(\w+)/(\w+)/')
            match = pattern.search(url)
            
            if match:
                category = match.group(1)
                id = match.group(2)
                return category, id
        except:
            print("[-] Failed extract URL")
            return

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
    
    def download(url):
        category, id = momonga.extract_url(url)
        compile_url = id + "-" + category
        
        title, img_urls = momonga.get_image_url(url)
                
        base_dir = "momonga"
        download_dir = os.path.join(default_directory, base_dir, compile_url)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        print(f"[+] Downloading title:{title} page:{len(img_urls)}p")
        
        def download_image(url):
            try:
                response = requests.get(url)
                response.raise_for_status()  # エラーがあれば例外を発生させる
                filename = os.path.join(download_dir, os.path.basename(url))
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return url, True
            except requests.RequestException as e:
                return url, False
        
        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if success != True:
                    print(f"[-] Failed to download {url}")

        print(f"[+] Download complete title:{title}")
        
class nhentai:
    def extract_id(id):
        try:
            # URLかIDかを判別し、URLの場合はIDを抽出
            url_pattern = re.compile(r'https://nhentai\.net/g/(\d+)')
            id_pattern = re.compile(r'(\d+)')
        
            match = url_pattern.search(id)
            if match:
                return match.group(1)
            
            # IDがURL形式でない場合も考慮
            match = id_pattern.search(id)
            if match:
                return match.group(1)
        except:
            print("[-] Failed extract URL")
            return

    def get_image_url(id):
        session = requests.Session()  # cf bypass
        response = session.get(f"https://nhentai.net/g/{id}").content
        soup = BeautifulSoup(response, "html.parser")
        title = soup.find("title").text
        title = title.replace("» nhentai: hentai doujinshi and manga", "")
        elements = soup.find_all("div", class_="thumb-container")
        # imgタグのsrc属性のURLを取得
        img_urls = []
        for element in elements:
            img_tag = element.find("img")
            if img_tag:
                img_urls.append(img_tag["data-src"])
            
        return title, img_urls
    
    def get_hd_image_url(id):
        session = requests.Session()  # cf bypass
        response = session.get(f"https://nhentai.net/g/{id}").content
        soup = BeautifulSoup(response, "html.parser")
        title = soup.find("title").text
        title = title.replace("» nhentai: hentai doujinshi and manga", "")
        elements = soup.find_all("div", class_="thumb-container")
        # imgタグのsrc属性のURLを取得
        img_urls_temp = []
        for element in elements:
            img_tag = element.find("img")
            if img_tag:
                img_urls_temp.append(img_tag["data-src"])
        
        cover_url = soup.find(itemprop="image").get("content")
        hd_id = re.search(r"/galleries/(\d+)/", cover_url).group(1)
        img_urls = []
        n = 0
        for i in elements:
            n += 1
            img_urls.append(f"https://i.nhentai.net/galleries/{hd_id}/{n}.jpg")
                    
        return title, img_urls
    
    def download(id, hd_quality=False):
        id = nhentai.extract_id(id)
        if hd_quality:
            title, img_urls = nhentai.get_hd_image_url(id)
        else:
            title, img_urls = nhentai.get_image_url(id)
                
        base_dir = "nhentai"
        download_dir = os.path.join(default_directory, base_dir, id)

        if not os.path.exists(download_dir):
            os.makedirs(download_dir)
        
        print(f"[+] Downloading title:{title} page:{len(img_urls)}p")
        
        def download_image(url):
            try:
                response = requests.get(url)
                response.raise_for_status()  # エラーがあれば例外を発生させる
                filename = os.path.join(download_dir, os.path.basename(url))
                with open(filename, 'wb') as file:
                    file.write(response.content)
                return url, True
            except requests.RequestException as e:
                return url, False
        
        # マルチスレッドで画像をダウンロード
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(download_image, url) for url in img_urls]
            for future in tqdm(as_completed(futures), total=len(futures), desc="Downloading", unit="file"):
                url, success = future.result()
                if success != True:
                    print(f"[-] Failed to download {url}")
                    
        print(f"[+] Download complete title:{title}")
        
## Example:
# hentaipaw.download("https://ja.hentaipaw.com/articles/2381472")
# nyahentai.download("https://nyahentai.re/magazine/re2991059/")
# momonga.download("https://momon-ga.com/fanzine/mo2991320/")
# nhentai.download("519944", hd_quality=True)
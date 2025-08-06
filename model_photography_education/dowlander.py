import os
import threading
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(current_dir, "download_photo")
MAX_PER_KEYWORD = 5000

MAX_PER_KEYWORD = 5000

KEYWORDS = [
    "humman face", "book", "laptop", "bed", "table", "phone", "people", "keyborad", "gaming mouse", "mousepad" , "cupboard"
]


def create_folder(name):
    path = os.path.join(DATASET_DIR, name)
    os.makedirs(path, exist_ok=True)
    return path

def download_with_google(keyword, max_num):
    folder = create_folder(keyword.replace(" ", "_"))
    crawler = GoogleImageCrawler(storage={"root_dir": folder})
    crawler.crawl(keyword=keyword, max_num=max_num)

def download_with_bing(keyword, max_num):
    folder = create_folder(keyword.replace(" ", "_"))
    crawler = BingImageCrawler(storage={"root_dir": folder})
    crawler.crawl(keyword=keyword, max_num=max_num)

def start_download(keyword):
    print(f"🔽 {keyword} için indirme başlatıldı...")
    try:
        download_with_google(keyword, MAX_PER_KEYWORD // 2)
        download_with_bing(keyword, MAX_PER_KEYWORD // 2)
        print(f"✅ {keyword} tamamlandı.")
    except Exception as e:
        print(f"❌ {keyword} indirilemedi: {e}")

def main():
    threads = []

    for keyword in KEYWORDS:
        t = threading.Thread(target=start_download, args=(keyword,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("🎉 Tüm indirmeler tamamlandı.")

if __name__ == "__main__":
    main()

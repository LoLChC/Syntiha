from icrawler.builtin import GoogleImageCrawler
import os

main_folder = "download_photo"

q = input("How to edicotion: ")

piece = input("How many dowland")

full_path = os.path.join(main_folder, q)

os.makedirs(full_path, exist_ok=True)

google_crawler = GoogleImageCrawler(storage={"root_dir": "dowland_photo/"+q})

google_crawler.crawl(keyword=q, max_num=piece, filters={
    "type": "photo",
    "size": "large"
}) 
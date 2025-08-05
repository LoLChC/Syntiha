from icrawler.builtin import GoogleImageCrawler
import os

# Bu Python dosyasının bulunduğu dizini al
script_dizini = os.path.dirname(os.path.abspath(__file__))

# Ana klasör adı
main_folder = "download_photo"

# Ana klasörün tam yolu
ana_klasor_yolu = os.path.join(script_dizini, main_folder)

# Kullanıcıdan sorgu ve indirme adedi alınır
q = input("What to search: ")
piece = int(input("How many to download: "))

# Alt klasörün tam yolu
full_path = os.path.join(ana_klasor_yolu, q)

# Klasörü oluştur
os.makedirs(full_path, exist_ok=True)

# Google crawler’ı başlat
google_crawler = GoogleImageCrawler(storage={"root_dir": full_path})

# Görselleri indir
google_crawler.crawl(keyword=q, max_num=piece, filters={
    "type": "photo",
    "size": "large"
})

print(f"Tam klasör yolu: {full_path}")

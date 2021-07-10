
import re
import urllib.request as urlreq
from bs4 import BeautifulSoup
import requests
#●画像ファイルをダウンロードするための準備
# ①-①.ライブラリをインポート
import time
import re
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from icrawler.builtin import BingImageCrawler
from PIL import Image
import os, glob
import numpy as np
from PIL import ImageFile


# ①-②.出力フォルダを作成
output_folder = Path('ira')
output_folder.mkdir(exist_ok=True)
# ①-③.スクレイピングしたいURLを設定
url = 'https://www.irasutoya.com/search?q=%E7%8C%AB'
# ①-④.画像ページのURLを格納するリストを用意
linklist = []

#●検索結果ページから画像のリンクを取り出す
# ②-①.検索結果ページのhtmlを取得
html = requests.get(url).text
# ②-②.検索結果ページのオブジェクトを作成
soup = BeautifulSoup(html, 'lxml')
# ②-③.画像リンクのタグをすべて取得
a_list =soup.select('div.boxmeta.clearfix > h2 > a')

# ②-④.画像リンクを1つずつ取り出す
for a in a_list:
# ②-⑤.画像ページのURLを抽出
    link_url = a.attrs['href']
# ②-⑥.画像ページのURLをリストに追加
    linklist.append(link_url)
    time.sleep(1.0)
alpha=['a','b','c','d','e','f','g']
# ●各画像ページから画像ファイルのURLを特定
# ③-①.画像ページのURLを1つずつ取り出す
for n,page_url in enumerate(linklist):
# ③-②.画像ページのhtmlを取得
    page_html = requests.get(page_url).text
# ③-③.画像ページのオブジェクトを作成
    page_soup = BeautifulSoup(page_html, "lxml")
# ③-④.画像ファイルのタグをすべて取得
    img_list = page_soup.select('div.entry > div > a > img')
# ③-⑤.imgタグを1つずつ取り出す
    for i,img in enumerate(img_list):
# ③-⑥.画像ファイルのURLを抽出
        img_url = (img.attrs['src'])
# ③-⑦.画像ファイルの名前を抽出
        filename = re.search(".*\/(.*png|.*jpg)$",img_url)
# ③-⑧.保存先のファイルパスを生成
        save_path = output_folder.joinpath(alpha[n]+str(i)+".jpg")
        time.sleep(1.0)
# ●画像ファイルのURLからデータをダウンロード
        try:
# ④-①.画像ファイルのURLからデータを取得
            image = requests.get(img_url)
# ④-②.保存先のファイルパスにデータを保存
            open(save_path, 'wb').write(image.content)
# ④-③.保存したファイル名を表示
            print(save_path)
            time.sleep(1.0)
        except ValueError:
# ④-④.失敗した場合はエラー表示
            print("ValueError!")



# 猫の画像を100枚取得
crawler = BingImageCrawler(storage={"root_dir": "cat"})
crawler.crawl(keyword="猫", max_num=100)


# IOError: image file is truncated (0 bytes not processed)回避のため
ImageFile.LOAD_TRUNCATED_IMAGES = True

classes = ["ira", "cat"]
num_classes = len(classes)
image_size = 64

im=[]
X_train = []
X_test  = []
y_train = []
y_test  = []

for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(classlabel+"/*.jpg")
    for i, file in enumerate(files):
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size, image_size))
        data = np.asarray(image)
        im.append(data.reshape(3,64,64))


    np.save("./"+classlabel+".npy", im)

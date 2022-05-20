import requests
import pandas as pd
import numpy as np

#楽天商品検索APIリクエストURL
url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"

#入力パラメーターを指定
param = {
    "applicationId" : "",       #アプリIDを入力
    "keyword" : "おもしろ雑貨" ,
    "format" : "json",
    "imageFlag" : 1
}

# APIを実行して結果を取得する
result = requests.get(url, param)

# jsonにデコードする
json_result = result.json()

#出力パラメータ―を指定
item_key = ['itemName', 'itemPrice','mediumImageUrls', 'itemCaption', 'itemUrl', 'shopName', 'shopUrl', 'reviewAverage', 'giftFlag', 'asurakuFlag']

item_list = []
for i in range(0, len(json_result['Items'])):
    tmp_item = {}
    item = json_result['Items'][i]['Item']
    for key, value in item.items():
        if key in item_key:
            tmp_item[key] = value
    item_list.append(tmp_item.copy())

# データフレームを作成
items_df = pd.DataFrame(item_list)

# 列の順番を入れ替える
items_df = items_df.reindex(columns=['itemName', 'itemPrice','mediumImageUrls', 'itemCaption', 'itemUrl', 'shopName', 'shopUrl', 'reviewAverage', 'giftFlag', 'asurakuFlag'])

# 列名と行番号を変更する:列名は日本語に、行番号は1からの連番にする
items_df.columns = ['商品名', '商品価格', '商品画像URL','商品説明文', '商品URL', '店舗名', '店舗URL', 'レビュー', 'ギフトラッピング', '翌日配送']
items_df.index = np.arange(1, 31)

#item_dfから出力したいものを指定
print(items_df[['商品名', '商品価格', '商品画像URL', 'レビュー', 'ギフトラッピング', '翌日配送']])
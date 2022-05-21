import requests
import pandas as pd
import numpy as np

"""
long : minprice
long : maxprice
string : genreid
bool   : asurakuflag
string : asurakuarea  （県名を～県で）エラー吐くので一旦停止中
string : genreid
"""
#566382
def api(minprice,maxprice,asurakuflag,genreid):    # 引数(budget, asuraku, category)
    #楽天商品検索APIリクエストURL
    url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"
    #入力パラメーターを指定
    param = {
        "applicationId" : "",       #アプリIDを入力
        "keyword"     : "おもしろ雑貨",
        "format"      : "json",
        "imageFlag"   : 1,
        "minPrice"    : minprice,
        "maxPrice"    : maxprice,
        "asurakuFlag" : asurakuflag,
        #"asurakuArea" : asurakuarea,
        "genreId"     : genreid
    }
    
    
    # APIを実行して結果を取得する
    result = requests.get(url, param)

    # jsonにデコードする
    json_result = result.json()

    #出力パラメータ―を指定
    item_key = ['itemName', 'mediumImageUrls', 'itemUrl', 'reviewAverage']

    item_list = []
    for i in range(0, len(json_result['Items'])):
        tmp_item = {}
        item = json_result['Items'][i]['Item']
        for key, value in item.items():
            if key in item_key:
             tmp_item[key] = value
        item_list.append(tmp_item.copy())
    
    # データフレームの表示の省略化を無効化
    pd.set_option('display.max_colwidth', 1000)
    
    # データフレームを作成
    items_df = pd.DataFrame(item_list)
    
    # 列の順番を入れ替える
    items_df = items_df.reindex(columns=['itemName', 'mediumImageUrls', 'itemUrl', 'reviewAverage'])

    # 列名と行番号を変更する:列名は日本語に、行番号は1からの連番にする
    items_df.columns = ['商品名', '商品画像URL', '商品URL', 'レビュー']
    items_df.index = np.arange(1, 31)

    imageurl = []
    for i in range(1, 31):
        f_1 = items_df.loc[i, ['商品画像URL']]
        f_2 = f_1.values.tolist()
        f_3 = f_2[0][0]
        f_4 = f_3['imageUrl']
        f_5 = f_4.replace('?_ex=128x128', '')
        imageurl.append(f_5)
        
    itemname = items_df.loc[:, ['商品名']]
    itemurl = items_df.loc[:, ['商品URL']]
    review = items_df.loc[:, ['レビュー']]
    
    return(itemname, imageurl, itemurl, review)
    
if __name__ == "__main__":
    output = api()
    print(output)
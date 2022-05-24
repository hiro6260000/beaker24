import requests
import streamlit as st
from transmit import SearchResult


def search_product(search_options):
    # 楽天商品検索APIリクエストURL
    image_url = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"
    # 入力パラメーターを指定
    params = {
        "applicationId": st.secrets.AppID,
        "keyword": "おもしろ",
        "format": "json",
        "imageFlag": 1,
        "minPrice": search_options.minPrice,
        "maxPrice": search_options.maxPrice,
        "genreId": search_options.genreId,
        "asurakuFlag": search_options.asurakuFlag,
        "giftFlag": search_options.giftFlag
    }
    if search_options.asurakuFlag is True:
        params["asurakuArea"] = search_options.asurakuArea

    # APIを実行して結果を取得する
    result = requests.get(image_url, params)

    # jsonにデコードする
    json_result = result.json()
    return reshape_result(json_result)


def reshape_result(json_result):
    item_list = []
    for i in range(0, len(json_result["Items"])):
        item = json_result["Items"][i]["Item"]  # これが一つの商品データ
        item_name = item["itemName"]
        item_url = item["itemUrl"]
        image_urls = item["mediumImageUrls"]
        image_url = image_urls[0]["imageUrl"].replace("?_ex=128x128", "")
        review = item["reviewAverage"]
        n_review = item["reviewCount"]
        asuraku_flag = item["asurakuFlag"]
        asuraku_area = item["asurakuArea"]
        item_price = item["itemPrice"]
        search_result = SearchResult(
            item_name, item_url, image_url, review, n_review, asuraku_flag, asuraku_area, item_price)
        item_list.append(search_result)
    return item_list

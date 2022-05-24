import streamlit as st
import streamlit.components.v1 as stc
import json
from api import search_product
from transmit import SearchOptions
import time


def sidebar(search_options):
    # 都道府県データの読み込み
    with open("./prefectures.json", mode="r", encoding="utf-8") as f:
        raw = f.read()
        prefec_codes = json.loads(raw)

    # カテゴリデータの読み込み
    with open("./categories.json", mode="r", encoding="utf-8") as f:
        raw = f.read()
        category_codes = json.loads(raw)

    # htmlの読み込み
    with open("./layout/sidebar.html", "r", encoding="utf-8") as f:
        sidebar_html = f.read()

    with st.sidebar:
        stc.html(sidebar_html)

        budget = st.radio(
            "プレゼントの予算",
            ("1000~3000円", "3000~5000円", "5000~7000円", "7000~1万円", "1万円以上")
        )
        category = st.radio(
            "カテゴリ",
            category_codes.keys()
        )
        category_code = category_codes[category]
        next_day_delivery = st.radio(
            "翌日配送",
            ("指定なし", "希望する")
        )
        if next_day_delivery == "希望する":
            prefec = st.selectbox(
                "配送先の都道府県を選んでください",
                prefec_codes.keys())
            prefec_code = prefec_codes[prefec]
        else:
            prefec_code = None
        wrapping = st.radio(
            "ラッピング",
            ('指定なし', '希望する')
        )

    search_button = st.sidebar.button("検索")
    if search_button:
        search_options.set(budget, category_code, next_day_delivery, prefec_code, wrapping)
        return True


def main():
    with open("./layout/title.html", "r", encoding="utf-8") as f:
        title_html = f.read()
    stc.html(title_html)

    # last_clickがsession_stateに追加されていない場合0で初期化
    if "last_click" not in st.session_state:
        st.session_state.last_click = 0

    search_options = SearchOptions()
    ret = sidebar(search_options)

    # 1秒経たないと検索できないように制限
    if ret is not None and time.time() - st.session_state.last_click > 1:
        st.session_state.last_click = time.time()

        # api.pyで検索
        items = search_product(search_options)

        if len(items) != 0:
            for i, item in enumerate(items):
                st.image(item.imageUrl, width=400)
                expander = st.expander(f"プレゼント候補 {i + 1} の詳細")
                expander.markdown(f"###### 商品名：{item.itemName}")
                expander.markdown(f"###### 値段：{item.itemPrice}円")
                expander.markdown(f"###### レビュー({item.n_review}件)：{item.review}")
                expander.markdown(f"URL：{item.itemUrl}")
                expander.markdown(f"###### 翌日配送：{item.nextDayDelivery}")
                if item.nextDayDelivery == "可":
                    expander.caption("～対象地域～")
                    expander.caption(item.asurakuArea)
        else:
            st.write("お求めの商品はありませんでした。")
    st.image("https://webservice.rakuten.co.jp/img/credit_31130.gif")


if __name__ == "__main__":
    main()

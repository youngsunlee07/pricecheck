import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["FULL DESCRIPTION"] = df["PRODUCT DESCRIPTION"].astype(str) + " " + df["Size"].astype(str)
    df["ITEM NO."] = df["ITEM NO."].astype(str).str.replace(".0", "", regex=False)
    return df

df = load_data()
visible_columns = [col for col in df.columns if col != "FULL DESCRIPTION"]

# 제목
st.title("UBP Price Checker")

# 검색 함수: 사용자가 입력한 글자에 따라 후보 반환
def search_products(query: str):
    if not query:
        return []
    matches = df[df["FULL DESCRIPTION"].str.contains(query, case=False, na=False)]
    results = [
        f"{row['ITEM NO.']} - {row['PRODUCT DESCRIPTION']}"
        for _, row in matches.iterrows()
    ]
    return results[:10]  # 최대 10개 추천

# streamlit-searchbox로 자동완성 드롭다운 구현
selection = st_searchbox(
    search_products,
    placeholder="Type product size or name (e.g., '1oz')",
    key="product_search"
)

# 선택된 항목 출력
if selection:
    selected_item_no = selection.split(" - ")[0]  # ITEM NO. 추출
    result = df[df["ITEM NO."] == selected_item_no]
    st.write(f"{len(result)} result(s) found")
    st.dataframe(result[visible_columns], use_container_width=True)

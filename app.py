import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox

# --- 데이터 로딩 ---
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["FULL DESCRIPTION"] = df["PRODUCT DESCRIPTION"].astype(str) + " " + df["Size"].astype(str)
    df["ITEM NO."] = df["ITEM NO."].astype(str).str.replace(".0", "", regex=False)
    return df

df = load_data()
visible_columns = [col for col in df.columns if col != "FULL DESCRIPTION"]

# --- UI ---
st.title("UBP Price Checker")

# --- 검색 함수: 모든 단어가 포함된 항목만 반환 ---
def search_products(query: str):
    if not query:
        return []
    terms = query.lower().split()
    filtered = df.copy()
    for term in terms:
        filtered = filtered[filtered["FULL DESCRIPTION"].str.lower().str.contains(term, na=False)]
    results = [
        f"{row['ITEM NO.']} - {row['PRODUCT DESCRIPTION']}"
        for _, row in filtered.iterrows()
    ]
    return results[:10]

# --- 자동완성 검색창 ---
selection = st_searchbox(
    search_products,
    placeholder="Type product name, size, or keyword (e.g., 'glue 1oz')",
    key="product_search"
)

# --- 선택 결과 출력 ---
if selection:
    selected_item_no = selection.split(" - ")[0]  # ITEM NO. 추출
    result = df[df["ITEM NO."] == selected_item_no]
    st.write(f"{len(result)} result(s) found")
    st.dataframe(result[visible_columns], use_container_width=True)

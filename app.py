import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox

# --- 데이터 로딩 ---
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["ITEM NO."] = df["ITEM NO."].astype(str).str.replace(".0", "", regex=False)
    df["PRODUCT CODE"] = df["PRODUCT CODE"].astype(str)
    return df

df = load_data()

# --- 출력할 컬럼 지정 (존재하는 컬럼만 필터링) ---
preferred_columns = [
    "ITEM NO.", "PRODUCT DESCRIPTION", "PRODUCT CODE", "INNER CS",
    "MASTER CS", "WS UNIT PRICE", "WS CASE PRICE", "RT UNIT PRICE"
]
visible_columns = [col for col in preferred_columns if col in df.columns]

# --- 타이틀 ---
st.title("UBP Price Checker")

# --- 검색 함수 ---
def search_products(query: str):
    if not query:
        return []
    terms = query.lower().split()
    filtered = df.copy()
    for term in terms:
        filtered = filtered[
            filtered["PRODUCT DESCRIPTION"].str.lower().str.contains(term, na=False) |
            filtered["ITEM NO."].str.lower().str.contains(term, na=False) |
            filtered["PRODUCT CODE"].str.lower().str.contains(term, na=False)
        ]
    return [
        f"{row['ITEM NO.']} - {row['PRODUCT DESCRIPTION']}"
        for _, row in filtered.iterrows()
    ]

# --- 검색창 ---
selection = st_searchbox(
    search_products,
    placeholder="Enter ITEM NO., PRODUCT DESCRIPTION, or PRODUCT CODE",
    key="product_search",
    clear_on_submit=True
)

# --- 결과 출력 ---
if selection:
    selected_item_no = selection.split(" - ")[0]
    result = df[df["ITEM NO."] == selected_item_no]
    st.write(f"{len(result)} result(s) found")

    display_df = result[visible_columns].reset_index(drop=True)
    display_df.index = [""] * len(display_df)
    st.dataframe(display_df, use_container_width=True)


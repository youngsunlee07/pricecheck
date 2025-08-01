import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox

# --- 데이터 로딩 ---
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx", dtype={"ITEM NO.": str, "PRODUCT CODE": str})
    df.columns = [col.strip() for col in df.columns]
    df["ITEM NO."] = df["ITEM NO."].astype(str)
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
        {"label": f"{row['ITEM NO.']} - {row['PRODUCT DESCRIPTION']}", "value": row['ITEM NO.']}
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
    result = df[df["ITEM NO."] == selection]  # selection은 ITEM NO.의 정확한 문자열
    st.write(f"{len(result)} result(s) found")

    display_df = result[visible_columns].reset_index(drop=True)
    display_df.index = [""] * len(display_df)
    st.dataframe(display_df, use_container_width=True)

    st.session_state.selection = None

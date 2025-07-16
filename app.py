import pandas as pd
import streamlit as st

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

# --- 검색창 (텍스트 입력 기반) ---
query = st.text_input("Search by ITEM NO., PRODUCT DESCRIPTION, or PRODUCT CODE:")

# --- 실시간 필터링 ---
if query:
    terms = query.lower().split()
    filtered = df.copy()
    for term in terms:
        filtered = filtered[
            filtered["PRODUCT DESCRIPTION"].str.lower().str.contains(term, na=False) |
            filtered["ITEM NO."].str.lower().str.contains(term, na=False) |
            filtered["PRODUCT CODE"].str.lower().str.contains(term, na=False)
        ]

    if not filtered.empty:
        st.write(f"🔍 {len(filtered)} result(s) found")
        display_df = filtered[visible_columns].reset_index(drop=True)
        display_df.index = [""] * len(display_df)
        st.dataframe(display_df, use_container_width=True)
    else:
        st.warning("No matching results found.")

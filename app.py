import pandas as pd
import streamlit as st
from streamlit_searchbox import st_searchbox

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["FULL DESCRIPTION"] = df["PRODUCT DESCRIPTION"].astype(str) + " " + df["Size"].astype(str)
    df["ITEM NO."] = df["ITEM NO."].astype(str).str.replace(".0", "", regex=False)
    return df

df = load_data()
visible_columns = [col for col in df.columns if col != "FULL DESCRIPTION"]

# --- UI 타이틀 ---
st.title("UBP Price Checker")

# --- 검색 함수 (모든 단어 포함 필터) ---
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

# --- 선택 저장용 세션 변수 ---
if "selection" not in st.session_state:
    st.session_state.selection = None

# --- 자동완성 입력창 ---
selection = st_searchbox(
    search_products,
    placeholder="Enter keyword to search",
    key="product_search"
)

# --- 선택 결과 출력 후 입력창 초기화 ---
if selection:
    st.session_state.selection = selection  # 저장
    selected_item_no = selection.split(" - ")[0]
    result = df[df["ITEM NO."] == selected_item_no]
    st.write(f"{len(result)} result(s) found")
    st.dataframe(result[visible_columns], use_container_width=True)

    # 👉 입력창을 초기화하려면 rerun으로 전체 새로고침
    st.session_state.selection = None
    st.rerun()

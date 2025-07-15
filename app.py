import pandas as pd
import streamlit as st

# --- 데이터 로드 ---
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["FULL DESCRIPTION"] = df["PRODUCT DESCRIPTION"].astype(str) + " " + df["Size"].astype(str)
    return df

df = load_data()
visible_columns = [col for col in df.columns if col != "FULL DESCRIPTION"]

# --- 검색어 입력창 ---
st.title("UBP Price Checker")
query = st.text_input("Enter ITEM NO. or PRODUCT DESCRIPTION").strip()

# --- 자동완성 후보 생성 ---
matches_item = df[df['ITEM NO.'].astype(str).str.contains(query, case=False, na=False)][['ITEM NO.']]
matches_desc = df[df['FULL DESCRIPTION'].str.contains(query, case=False, na=False)][['PRODUCT DESCRIPTION']]

suggestions = pd.concat([matches_item, matches_desc]).drop_duplicates().astype(str)
suggestion_list = [s for s in suggestions.values.flatten().tolist() if pd.notna(s)]

# --- 결과 출력 함수 ---
def show_results(search_term):
    mask = df['ITEM NO.'].astype(str).str.contains(search_term, case=False, na=False) | \
           df['FULL DESCRIPTION'].str.contains(search_term, case=False, na=False)
    filtered = df[mask]
    st.write(f"{len(filtered)} result(s) found")
    st.dataframe(filtered[visible_columns], use_container_width=True)

# --- 자동완성 제안 목록 (버튼으로 출력) ---
if query:
    st.subheader("Suggestions:")
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestion_list[:10]):  # 최대 10개
        with cols[i % 2]:
            if st.button(suggestion, key=f"suggestion_{i}"):
                show_results(suggestion)
                st.stop()  # 버튼 클릭 시 나머지 실행 중단

    # 엔터만 눌렀을 때는 query 자체로 검색
    if suggestion_list and query and "button_clicked" not in st.session_state:
        show_results(query)
        st.session_state["button_clicked"] = False
else:
    st.info("Please type a keyword to search.")


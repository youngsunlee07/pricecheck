import pandas as pd
import streamlit as st

# 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["FULL DESCRIPTION"] = df["PRODUCT DESCRIPTION"].astype(str) + " " + df["Size"].astype(str)
    return df

df = load_data()
visible_columns = [col for col in df.columns if col != "FULL DESCRIPTION"]

# UI 제목 및 입력
st.title("UBP Price Checker")
query = st.text_input("Enter ITEM NO. or PRODUCT DESCRIPTION").strip()

# 결과 필터링 함수
def show_results(search_term):
    mask = df['ITEM NO.'].astype(str).str.contains(search_term, case=False, na=False) | \
           df['FULL DESCRIPTION'].str.contains(search_term, case=False, na=False)
    filtered = df[mask]
    st.write(f"{len(filtered)} result(s) found")
    st.dataframe(filtered[visible_columns], use_container_width=True)

# 후보 자동완성
if query:
    matches_item = df[df['ITEM NO.'].astype(str).str.contains(query, case=False, na=False)][['ITEM NO.']]
    matches_desc = df[df['FULL DESCRIPTION'].str.contains(query, case=False, na=False)][['PRODUCT DESCRIPTION']]
    suggestions = pd.concat([matches_item, matches_desc]).drop_duplicates().astype(str)

    # nan 제거 및 정렬
    suggestion_list = sorted([s for s in suggestions.values.flatten().tolist() if pd.notna(s) and s.strip() != ""], key=str.lower)

    # 후보 목록 표시 (세로 정렬)
    if suggestion_list:
        st.subheader("Suggestions:")
        for i, suggestion in enumerate(suggestion_list[:10]):
            if st.button(suggestion, key=f"suggestion_{i}"):
                show_results(suggestion)
                st.stop()

    # 엔터만 눌렀을 때
    show_results(query)
else:
    st.info("Please type a keyword to search.")

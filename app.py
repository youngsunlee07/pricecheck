import pandas as pd
import streamlit as st

# 엑셀 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_excel("UBP_Price.xlsx")
    df.columns = [col.strip() for col in df.columns]
    df["FULL DESCRIPTION"] = df["PRODUCT DESCRIPTION"].astype(str) + " " + df["Size"].astype(str)
    return df

df = load_data()
visible_columns = [col for col in df.columns if col != "FULL DESCRIPTION"]

# 검색어 입력
st.title("UBP Price Checker")
query = st.text_input("Enter ITEM NO. or PRODUCT DESCRIPTION").strip()

# 후보 자동완성 리스트 만들기
matches_item = df[df['ITEM NO.'].astype(str).str.contains(query, case=False, na=False)]
matches_desc = df[df['FULL DESCRIPTION'].str.contains(query, case=False, na=False)]

suggestions = pd.concat([
    matches_item[['ITEM NO.']],
    matches_desc[['PRODUCT DESCRIPTION']]
]).drop_duplicates().astype(str)

suggestion_list = suggestions.values.flatten().tolist()

# 결과 출력 함수
def show_results(search_term):
    mask = df['ITEM NO.'].astype(str).str.contains(search_term, case=False, na=False) | \
           df['FULL DESCRIPTION'].str.contains(search_term, case=False, na=False)
    filtered = df[mask]
    st.write(f"🔍 {len(filtered)} result(s) found")
    st.dataframe(filtered[visible_columns], use_container_width=True)

# 자동완성 버튼 리스트
if query:
    st.write("Suggestions:")
    cols = st.columns(2)
    for i, suggestion in enumerate(suggestion_list[:10]):  # 최대 10개만 보여줌
        with cols[i % 2]:
            if st.button(suggestion):
                show_results(suggestion)
                st.stop()  # 클릭 시 중복 실행 방지

    # 사용자가 아무 것도 클릭하지 않고 엔터만 친 경우
    if query and st.session_state.get("enter_pressed", False):
        show_results(query)
        st.session_state.enter_pressed = False  # 리셋

# 엔터 입력 감지
if query and st.session_state.get("last_query") != query:
    st.session_state.last_query = query
    st.session_state.enter_pressed = True

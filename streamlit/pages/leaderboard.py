import streamlit as st
import pandas as pd
from services.api import get_leaderboard

st.markdown("""
<div class="bg-red-500 text-white p-8 text-4xl">
</div>
""", unsafe_allow_html=True)

# Home routing
col_back, col_title = st.columns([1.5, 8])

with col_back:
    st.write("")
    if st.button("Back", icon=":material/arrow_back:", use_container_width=True):
        st.switch_page("pages/home.py")

st.title("Leaderboard")

data = get_leaderboard()

if data:
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data atau gagal mengambil leaderboard.")
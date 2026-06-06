import streamlit as st
import pandas as pd
from services.api import get_leaderboard

st.title("Leaderboard")

data = get_leaderboard()

if data:
    # Mengubah list of dict dari API menjadi DataFrame agar tabelnya rapi
    df = pd.DataFrame(data)
    # Asumsi API mengembalikan [{"username": "player1", "score": 1500}, ...]
    st.dataframe(df, use_container_width=True)
else:
    st.info("Belum ada data atau gagal mengambil leaderboard.")
import streamlit as st

st.set_page_config(page_title="Battleship API", layout="wide")

# Inisialisasi variabel global di session state
if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None
if "game_id" not in st.session_state:
    st.session_state.game_id = None

st.title("Battleship FastAPI + Streamlit")

if st.session_state.token:
    st.success(f"Selamat datang, {st.session_state.username}! Silakan navigasi ke menu **Game** di sidebar.")
else:
    st.info("Silakan Login atau Register melalui menu di sidebar untuk mulai bermain.")
import streamlit as st
from utils.theme import load_css
from utils.auth import cookies

load_css()

st.set_page_config(page_title="Battleship API", layout="wide")

# Inisialisasi variabel global di session state
if "token" not in st.session_state:
    st.session_state.token = cookies.get("token")

if "username" not in st.session_state:
    st.session_state.username = cookies.get("username")

# Definisikan halaman-halaman yang ada
home_page = st.Page("pages/home.py", title="Home")
login_page = st.Page("pages/login.py", title="Login")
register_page = st.Page("pages/register.py", title="Register")
game_page = st.Page("pages/game.py", title="Game")
leaderboard_page = st.Page("pages/leaderboard.py", title="Leaderboard")

# Konfigurasi navigasi dan SEMBUNYIKAN sidebar
pg = st.navigation(
    [
        home_page,
        login_page,
        register_page,
        game_page,
        leaderboard_page
    ],
    position="hidden"
)

# Jalankan halaman yang sedang aktif
pg.run()
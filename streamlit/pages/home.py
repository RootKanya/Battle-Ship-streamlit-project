import streamlit as st
from utils.auth import cookies
from utils.theme import load_css

st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# Header
col_title, col_auth1, col_auth2 = st.columns([10, 3, 3])

with col_title:
    st.markdown('<div class="text-5xl font-extrabold text-white-600 mb-4"><i class="fa-solid fa-ship mr-3"></i>Battleship Game</div>', unsafe_allow_html=True)

is_logged_in = st.session_state.get("token") is not None

if not is_logged_in:
    with col_auth1:
        if st.button("Login", icon=":material/login:", use_container_width=True):
            st.switch_page("pages/login.py")
    with col_auth2:
        if st.button("Register", icon=":material/person_add:", type="primary", use_container_width=True):
            st.switch_page("pages/register.py")
else:
    with col_auth1:
        st.markdown(f'<div class="text-lg font-semibold text-gray-700 text-right mt-4"><i class="fa-regular fa-user mr-2"></i>{st.session_state.username}</div>', unsafe_allow_html=True)
    with col_auth2:
        if st.button("Logout"):
            cookies["token"] = ""
            cookies["username"] = ""
            cookies.save()

            st.session_state.token = None
            st.session_state.username = None

            st.rerun()

st.divider()

# Game Mode
st.markdown('<div class="text-2xl font-bold text-white-800 mb-6"><i class="fa-solid fa-gamepad mr-2"></i>Choose Game Mode</div>', unsafe_allow_html=True)

col_1p, col_space, col_2p = st.columns([1, 0.1, 1])

# 1P Card
with col_1p:
    with st.container(border=True):
        st.markdown("""
        <div class="flex flex-col items-center justify-center p-6">
            <i class="fa-solid fa-robot text-6xl text-red-500 mb-4"></i>
            <h3 class="text-3xl font-bold text-gray-800">1 Player</h3>
            <p class="text-gray-500 mt-2 text-center text-lg">Battle with AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("PLAY 1P", icon=":material/play_arrow:", use_container_width=True, type="primary", key="btn_1p"):
            if is_logged_in:
                st.session_state.game_mode = "1p" 
                st.switch_page("pages/game.py")
            else:
                st.warning("Login untuk bermain!", icon=":material/warning:")

# 2P Card
with col_2p:
    with st.container(border=True):
        st.markdown("""
        <div class="flex flex-col items-center justify-center p-6">
            <i class="fa-solid fa-users text-6xl text-red-500 mb-4"></i>
            <h3 class="text-3xl font-bold text-gray-800">2 Players</h3>
            <p class="text-gray-500 mt-2 text-center text-lg">Battle with your friend</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("PLAY 2P", icon=":material/play_arrow:", use_container_width=True, type="primary", key="btn_2p"):
            if is_logged_in:
                st.session_state.game_mode = "2p"
                st.switch_page("pages/game.py")
            else:
                st.warning("Login untuk bermain!", icon=":material/warning:")

st.divider()

# Leaderboard
with st.container(border=True):
    col_icon, col_info, col_btn = st.columns([1, 4, 2])
    
    with col_icon:
        st.markdown('<div class="flex justify-center items-center h-full"><i class="fa-solid fa-trophy text-6xl text-red-400 mt-4"></i></div>', unsafe_allow_html=True)
        
    with col_info:
        st.markdown("""
        <div class="flex flex-col justify-center h-full mt-4 mb-4">
            <h3 class="text-3xl font-bold text-gray-800">Global Leaderboard</h3>
        </div>
        """, unsafe_allow_html=True)
        
    with col_btn:
        st.write("")
        if st.button("GLOBAL RANKING", icon=":material/trophy:", use_container_width=True, key="btn_lead"):
            if is_logged_in:
                st.switch_page("pages/leaderboard.py")
            else:
                st.warning("Login untuk mengakses Leaderboard.", icon=":material/lock:")
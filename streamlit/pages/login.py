import streamlit as st
from services.api import login_user
from utils.theme import load_css
from utils.auth import cookies

col_spacer1, col_main, col_spacer2 = st.columns([1, 1.5, 1])

with col_main:
    st.write("")
    st.write("")
    
    st.title("Log In")

    # Login form
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        submit_btn = st.form_submit_button("Masuk", type="primary", use_container_width=True)

    if submit_btn:
        res = login_user(username, password)
        if res.status_code == 200:
            data = res.json()

            token = data["access_token"]

            st.session_state.token = token
            st.session_state.username = username

            cookies["token"] = token
            cookies["username"] = username
            cookies.save()

            st.switch_page("pages/home.py") 
        else:
            st.error("Username atau password salah!", icon=":material/error:")

    st.divider()

    # Registration routing
    st.write("Belum memiliki akun?")
    if st.button("Daftar Sekarang", icon=":material/person_add:", use_container_width=True):
        st.switch_page("pages/register.py")
        
    st.write("")
    
    # Home routing
    if st.button("Kembali ke Halaman Utama", icon=":material/home:", use_container_width=True):
        st.switch_page("pages/home.py")
import streamlit as st
from services.api import register_user
from utils.theme import load_css

col_spacer1, col_main, col_spacer2 = st.columns([1, 1.5, 1])

with col_main:
    st.write("")
    st.write("")
    
    st.title("Register")

    # Register form
    with st.form("register_form"):
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")
        
        submit_btn = st.form_submit_button("Daftar", type="primary", use_container_width=True)

    # Submit
    if submit_btn:
        if new_user and new_pass:
            res = register_user(new_user, new_pass)
            if res.status_code == 200:
                st.success("Registrasi berhasil! Silakan login menggunakan akun baru Anda.", icon=":material/check_circle:")
            else:
                st.error("Gagal mendaftar. Username mungkin sudah ada.", icon=":material/error:")
        else:
            st.warning("Isi username dan password!", icon=":material/warning:")

    st.divider()

    # Login routing
    st.write("Sudah punya akun?")
    if st.button("Masuk di sini", icon=":material/login:", use_container_width=True):
        st.switch_page("pages/login.py")
        
    st.write("") 
    
    # Home routing
    if st.button("Kembali ke Halaman Utama", icon=":material/home:", use_container_width=True):
        st.switch_page("pages/home.py")
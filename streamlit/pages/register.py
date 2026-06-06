import streamlit as st
from services.api import register_user

st.title("Register")

with st.form("register_form"):
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    submit_btn = st.form_submit_button("Daftar")

if submit_btn:
    if new_user and new_pass:
        res = register_user(new_user, new_pass)
        if res.status_code == 200:
            st.success("Registrasi berhasil! Silakan login.")
        else:
            st.error("Gagal mendaftar. Username mungkin sudah ada.")
    else:
        st.warning("Isi username dan password!")
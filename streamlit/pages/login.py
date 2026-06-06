import streamlit as st
from services.api import login_user

st.title("Log In")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_btn = st.form_submit_button("Masuk")

if submit_btn:
    res = login_user(username, password)
    if res.status_code == 200:
        data = res.json()
        st.session_state.token = data.get("access_token")
        st.session_state.username = username
        st.success("Login berhasil!")
        st.rerun()
    else:
        st.error("Username atau password salah!")
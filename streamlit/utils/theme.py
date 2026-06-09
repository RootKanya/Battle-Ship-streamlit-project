import streamlit as st
from pathlib import Path

CSS_FILE = Path(__file__).parent.parent / "assets" / "style.css"

@st.cache_data
def get_css():
    return CSS_FILE.read_text()

def load_css():
    st.markdown(
        f"<style>{get_css()}</style>",
        unsafe_allow_html=True
    )
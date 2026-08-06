import streamlit as st
from authentication.signup import show_signup

st.set_page_config(
    page_title="Retail Detective AI",
    page_icon="🛍️",
    layout="centered"
)

st.title("🛍️ Retail Detective AI")

show_signup()
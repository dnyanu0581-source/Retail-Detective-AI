import streamlit as st

from authentication.login import show_login
from authentication.signup import show_signup
from pages.dashboard import show_dashboard


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Retail Detective AI",
    page_icon="🛍️",
    layout="wide"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "username" not in st.session_state:
    st.session_state.username = None

if "email" not in st.session_state:
    st.session_state.email = None


# --------------------------------------------------
# Main Application
# --------------------------------------------------
if st.session_state.logged_in:

    show_dashboard()

else:

    st.title("🛍️ Retail Detective AI")
    st.subheader("AI-Powered Business Intelligence & Decision Support System")

    login_tab, signup_tab = st.tabs(
        ["🔑 Login", "📝 Sign Up"]
    )

    with login_tab:
        show_login()

    with signup_tab:
        show_signup()
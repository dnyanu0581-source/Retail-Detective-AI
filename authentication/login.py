import streamlit as st
from authentication.auth import get_user_by_email, verify_password


def show_login():

    st.subheader("🔑 Login")

    email = st.text_input(
        "Email",
        key="login_email"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login", width="stretch"):

        # Empty Fields
        if not email or not password:
            st.error("Please enter your email and password.")
            return

        # Fetch user
        user = get_user_by_email(email)

        if user is None:
            st.error("No account found with this email.")
            return

        # Verify Password
        if verify_password(password, user["password_hash"]):

            st.session_state.logged_in = True
            st.session_state.user_id = user["id"]
            st.session_state.username = user["username"]
            st.session_state.email = user["email"]

            st.success(f"Welcome, {user['username']}!")
            st.rerun()

        else:
            st.error("Incorrect password.")
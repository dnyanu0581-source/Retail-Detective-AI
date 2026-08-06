import streamlit as st
from authentication.auth import user_exists, create_user


def show_signup():

    st.subheader("📝 Create New Account")

    username = st.text_input("Username", key="signup_username")

    email = st.text_input("Email", key="signup_email")

    password = st.text_input(
        "Password",
        type="password",
        key="signup_password"
    )

    confirm_password = st.text_input(
        "Confirm Password",
        type="password",
        key="signup_confirm_password"
    )

    if st.button("Create Account", width="stretch"):

        # Empty fields
        if not username or not email or not password or not confirm_password:
            st.error("Please fill in all fields.")
            return

        # Password length
        if len(password) < 8:
            st.error("Password must contain at least 8 characters.")
            return

        # Password match
        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        # User already exists
        if user_exists(email):
            st.warning("Email is already registered.")
            return

        # Create account
        if create_user(username, email, password):
            st.success("🎉 Account created successfully!")
            st.info("Please switch to the Login tab.")
        else:
            st.error("Unable to create account.")
import streamlit as st

from authentication.auth import (
    user_exists,
    create_user
)


def show_signup():

    st.subheader("📝 Create New Account")

    username = st.text_input(
        "Username",
        key="signup_username"
    )

    email = st.text_input(
        "Email",
        key="signup_email"
    )

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

    if st.button(
        "Create Account",
        key="signup_button",
        use_container_width=True
    ):

        # --------------------------------------------------
        # Validate fields
        # --------------------------------------------------

        if not username or not email or not password or not confirm_password:
            st.error("Please fill in all fields.")
            return

        username = username.strip()
        email = email.strip().lower()

        # --------------------------------------------------
        # Validate username
        # --------------------------------------------------

        if len(username) < 3:
            st.error("Username must contain at least 3 characters.")
            return

        # --------------------------------------------------
        # Validate password
        # --------------------------------------------------

        if len(password) < 8:
            st.error("Password must contain at least 8 characters.")
            return

        if password != confirm_password:
            st.error("Passwords do not match.")
            return

        # --------------------------------------------------
        # Check whether user already exists
        # --------------------------------------------------

        if user_exists(email):
            st.warning(
                "An account with this email already exists."
            )
            return

        # --------------------------------------------------
        # Create account
        # --------------------------------------------------

        success = create_user(
            username,
            email,
            password
        )

        if success:

            st.success(
                "🎉 Account created successfully!"
            )

            st.info(
                "Your account has been created. "
                "Please switch to the Login tab."
            )

        else:

            st.error(
                "Unable to create account. "
                "Please try again."
            )
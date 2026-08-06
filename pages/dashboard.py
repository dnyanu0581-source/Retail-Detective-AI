import streamlit as st


def show_dashboard():

    st.title("🛍️ Retail Detective AI")

    st.success(f"Welcome, {st.session_state.username}! 👋")

    st.markdown("---")

    st.header("Dashboard")

    st.info("Authentication successful.")

    st.write("You are now logged in.")

    st.markdown("---")

    if st.button("🚪 Logout", width="stretch"):

        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.email = None

        st.rerun()
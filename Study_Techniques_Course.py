import streamlit as st

from common import show_toc, setup_sidebar, setup_navigation


def show_ui():
    setup_sidebar()

    st.title("Study Techniques Course")

    st.write("Use the left sidebar to navigate to the course.")

    show_toc()

setup_navigation()

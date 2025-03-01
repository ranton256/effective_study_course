import streamlit as st

from common import show_page_controls, show_toc, setup_sidebar, show_markdown_for_page

setup_sidebar()

show_markdown_for_page(__file__)
st.header("Lessons")

show_toc()

show_page_controls(__file__)

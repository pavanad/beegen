import os

import streamlit as st

CURRENT_DIR = os.path.dirname(__file__)


def set_config():
    favicon_path = os.path.join(CURRENT_DIR, "images/favicon.ico")
    st.set_page_config(
        page_title="BeeGen - Chat",
        page_icon=favicon_path,
        layout="wide",
    )

    hide_decoration_bar_style = """
        <style>
            header {visibility: hidden;}
        </style>
    """
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)


def set_page_header():
    image_path = os.path.join(CURRENT_DIR, "images/beegen.png")
    st.logo(image_path)

    with st.sidebar:
        st.image(image_path, use_column_width=True)
        st.subheader("BeeGen's Chat Interface")
        st.markdown(
            """
            BeeGen's chat was created to facilitate testing on any type of
            agent using API, thus allowing the use of any type of LLM or framework.
            """
        )
        st.divider()

        st.page_link("app.py", label="Settings", icon=":material/settings:")
        st.page_link("pages/playground.py", label="PlayGround", icon=":material/chat:")

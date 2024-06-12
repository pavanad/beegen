import json

import streamlit as st
from streamlit_ace import st_ace

from beegen.services.chat.components import page_config

DEFAULT_CHAT_SETTINGS = {
    "endpoint": "",
    "request_body": "",
    "response_type": "",
    "response_type_index": 0,
    "full_json": False,
    "json_key": "",
}


def settings():
    setup_page()
    display_settings()


def setup_page():
    page_config.set_config()
    page_config.set_page_header()

    st.header("Settings", divider="orange")
    st.markdown("#### Configure the communication API with your model")


def display_settings():
    display_endpoint_setting()
    display_request_body_settings()
    display_response_settings()


def display_endpoint_setting():
    chat_settings = load_settings()

    with st.container(border=True):
        endpoint = st.text_input(
            "Endpoint",
            placeholder="Enter endpoint",
            value=chat_settings.get("endpoint"),
        )
        st.info(
            "The request to the endpoint will always be of type :orange[POST]",
            icon=":material/info:",
        )
        st.session_state.chat_settings["endpoint"] = endpoint


def display_request_body_settings():
    chat_settings = load_settings()

    with st.expander("Request Body"):
        st.markdown(
            """
            The request body will be sent as a JSON object.\n
            Use the variable :orange[{prompt}] to insert the text typed by the user
            in the chat, for example:
            """
        )
        st.code(
            """
            {
                "model": "llama3",
                "prompt": "{prompt}",
                "stream": false
            }
            """,
            language="json",
        )
        st.write("Define the request body:")
        request_body = st_ace(
            language="json",
            keybinding="vscode",
            min_lines=10,
            max_lines=None,
            font_size=14,
            tab_size=4,
            wrap=False,
            show_gutter=True,
            show_print_margin=False,
            readonly=False,
            annotations=None,
            theme="chaos",
            value=chat_settings.get("request_body"),
        )
        st.session_state.chat_settings["request_body"] = request_body
        if not is_valid_json(request_body):
            st.session_state.chat_settings["request_body"] = ""
            st.error("The JSON provided for the request body is invalid")


def display_response_settings():
    chat_settings = load_settings()

    with st.expander("Response"):
        options = ["json", "text"]
        response_type = st.radio(
            "Select your response type",
            options,
            captions=[
                "The response is a json object.",
                "The response is a text in a string.",
            ],
            index=chat_settings.get("response_type_index", 0),
        )
        response_type_index = options.index(response_type)

        json_key = ""
        full_json = False

        if response_type == "json":
            full_json = st.checkbox(
                "Check to return the complete JSON in the chat",
                value=chat_settings.get("full_json", False),
            )
            if not full_json:
                json_key = st.text_input(
                    "JSON Key",
                    placeholder="Set the key from which the value will be returned",
                    value=chat_settings.get("json_key", ""),
                )
        st.session_state.chat_settings.update(
            {
                "response_type": response_type,
                "response_type_index": response_type_index,
                "full_json": full_json,
                "json_key": json_key,
            }
        )


def load_settings() -> dict:
    if "chat_settings" not in st.session_state:
        st.session_state["chat_settings"] = DEFAULT_CHAT_SETTINGS.copy()
    return st.session_state.chat_settings


def is_valid_json(json_string: str) -> bool:
    try:
        if json_string:
            json.loads(json_string)
        return True
    except json.JSONDecodeError:
        return False

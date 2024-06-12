import requests
import streamlit as st
from components import page_config
from requests import Response


def main():
    setup_page()
    chat_settings = st.session_state.get("chat_settings", {})

    if not chat_settings.get("endpoint"):
        st.warning("Endpoint not found. Please set endpoint in chat settings first")
        return

    if not chat_settings.get("request_body"):
        st.warning(
            "Request body not found. Please set request body in chat settings first"
        )
        return

    generate_chat()


def setup_page():
    page_config.set_config()
    page_config.set_page_header()
    st.header("PlayGround", divider="orange")


def generate_chat():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "type": "text",
                "content": "How can I help you today?",
            }
        ]

    render_previous_messages()

    prompt = st.chat_input("Send a message")
    if not prompt:
        return

    st.session_state.messages.append(
        {"role": "user", "type": "text", "content": prompt}
    )
    st.chat_message("user").write(prompt)

    with st.spinner("Waiting for response..."):
        try:
            response = request_model(prompt)
            handle_response(response)
        except Exception as e:
            st.error(f"An error occurred in communication with the model: {e}")


def render_previous_messages():
    """Render previous chat messages from session state."""
    message_type = {"text": st.write, "code": st.code}
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            content = msg["content"]
            message_type.get(msg["type"], st.write)(content)


def request_model(prompt: str) -> Response:
    """Send a request to the model with the given prompt."""
    headers = {"Content-Type": "application/json"}
    url = st.session_state.chat_settings.get("endpoint")
    data = st.session_state.chat_settings.get("request_body", "").replace(
        "{prompt}", prompt
    )

    return requests.post(url, headers=headers, data=data)


def handle_response(response: Response):
    """Handle the model's response and update chat messages."""

    if response.status_code != 200:
        raise Exception(response.content)

    full_json = st.session_state.chat_settings.get("full_json", True)
    response_type = st.session_state.chat_settings.get("response_type", "json")

    if response_type == "text":
        content = response.text
        add_message("assistant", "text", content)
        return

    content = response.json()
    if full_json:
        add_message("assistant", "code", content)
        return

    json_key = st.session_state.chat_settings.get("json_key", "")
    content = content.get(
        json_key,
        (
            f"The JSON key :orange[{json_key}] is not valid for the response.\n"
            "Please check the JSON key in settings and try again."
        ),
    )
    add_message("assistant", "text", content)


def add_message(role: str, msg_type: str, content: str):
    """Add a new message to the session state and display it."""
    st.session_state.messages.append(
        {"role": role, "type": msg_type, "content": content}
    )
    if msg_type == "text":
        st.chat_message(role).write(content)
    else:
        st.chat_message(role).code(content)


if __name__ == "__main__":
    main()

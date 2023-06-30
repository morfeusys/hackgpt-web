import streamlit as st
from chat.chat import create_agent
from chat.chat import init_chat

container = st.empty()
if st.session_state.get("api_conversation_id"):
    init_chat(container, "api_conversation_id")
else:
    with container.form("api_form", clear_on_submit=True):
        st.markdown("# API")
        st.markdown("_This agent answers your questions using any HTTP API_")
        st.divider()

        url = st.text_input(label="URL that points to OpenAPI JSON, or a website where ChatGPT plugin is hosted", placeholder="for example https://www.klarna.com")
        prompt = st.text_area(label="System prompt that should be appended to the API description (optional)")
        model = st.selectbox(label="GPT model to use", options=["gpt-4-0613", "gpt-3.5-turbo-0613"])
        if st.form_submit_button("Create"):
            if url:
                create_agent(container, "api_conversation_id", "api", params={"url": url, "model": model, "prompt": prompt, "noParse": True})

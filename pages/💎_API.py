import streamlit as st
from chat.chat import init_agent


def form(init):
    st.markdown("# 💎 API")
    st.markdown("_This agent answers your questions using any HTTP API_")
    st.divider()

    url = st.text_input(label="URL that points to OpenAPI JSON, or a website where ChatGPT plugin is hosted", placeholder="for example https://www.klarna.com")
    prompt = st.text_area(label="System prompt that should be appended to the API description (optional)")
    model = st.selectbox(label="GPT model to use", options=["gpt-4-0613", "gpt-3.5-turbo-0613"])

    if st.form_submit_button("Create"):
        if url:
            init({
                "type": "api",
                "info": {
                    "icon": "💎",
                    "title": "API",
                    "prompt": f'_Ready! Now you can send me any queries and I will try to answer using {url}_',
                },
                "params": {
                    "url": url,
                    "model": model,
                    "prompt": prompt
                },
                "schema": {
                    "noParse": True
                }
            })


st.set_page_config(page_title="API agent", page_icon="💎")
init_agent("api_conversation", form)

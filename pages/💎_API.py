import streamlit as st
from agent.chat import init_agent


def form(init):
    url = st.text_input(label="API address", placeholder="for example https://www.klarna.com", help="URL that points to OpenAPI JSON, or a website where ChatGPT plugin is hosted")
    prompt = st.text_area(label="Prompt that should be appended to the API description _(optional)_", help="Describe how assistant should act with this API")
    model = st.selectbox(label="GPT model to use", options=["gpt-4-0613", "gpt-3.5-turbo-0613"], help="GPT-3.5 is faster and cheaper, but GPT-4 is much better for complex tasks")
    no_parse = st.checkbox(label="Disable link parsing", help="Agent will not parse any URLs you send trying to retrieve texts")

    if st.form_submit_button("Create"):
        if url:
            init({
                "url": url,
                "model": model,
                "prompt": prompt,
                "noParse": no_parse
            })


init_agent(
    key="api_conversation",
    form_builder=form,
    agent_type="api",
    agent_info={
        "icon": "💎",
        "title": "API",
        "description": "This agent answers your questions using any HTTP API",
        "prompt": "Ready! Now you can send me any queries and I will try to answer using {url}"
    }
)

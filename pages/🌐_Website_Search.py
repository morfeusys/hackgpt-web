import streamlit as st
from agent.chat import init_agent


def form(init):
    url = st.text_input(label="URL of starting page to parse", placeholder="For ex: https://just-ai.com/blog")
    noCache = st.checkbox(label="Disable caching", help="Agent will parse entire website each time if checked")

    if st.form_submit_button("Create"):
        if url:
            init({
                "url": url,
                "noCache": noCache
            })


init_agent(
    key="websearch_conversation",
    form_builder=form,
    agent_type="retrievalqa",
    agent_info={
        "icon": "🌐",
        "title": "Website search",
        "description": "This agent answers any questions through the entire website",
        "prompt": "Ready! Now send me any questions regarding the content of {url}"
    }
)

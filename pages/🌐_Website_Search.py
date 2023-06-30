import streamlit as st
from chat.chat import create_agent
from chat.chat import init_chat

container = st.empty()
if st.session_state.get("websearch_conversation_id"):
    init_chat(container, "websearch_conversation_id")
else:
    with container.form("websearch_form", clear_on_submit=True):
        st.markdown("# Website search")
        st.markdown("_This agent answers any questions through the entire website_")
        st.divider()

        url = st.text_input(label="Paste here a URL of starting page to parse")
        noCache = st.checkbox(label="Disable caching")
        if st.form_submit_button("Create"):
            if url:
                create_agent(container, "websearch_conversation_id", "retrievalqa", params={"url": url, "noCache": noCache})

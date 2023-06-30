import streamlit as st
from chat.chat import create_agent
from chat.chat import init_chat

container = st.empty()
if st.session_state.get("summarizer_conversation_id"):
    init_chat(container, "summarizer_conversation_id")
else:
    with container.form("summarizer_form", clear_on_submit=True):
        st.markdown("# Summarizer")
        st.markdown("_This agent summarizes any documents with defined rules_")
        st.divider()

        link = st.text_input(label="Paste here a direct link to your document")
        uploaded_file = st.file_uploader(label="Or upload file", type=["pdf", "doc", "docx", "xlsx", "txt", "mp3", "wav", "text", "md"])
        sentences = st.number_input(label="The number of sentences in summary", min_value=1)
        fields = st.text_input(label="Comma separated fields that should be included in summary (optional)")

        if st.form_submit_button("Create"):
            if link or uploaded_file:
                create_agent(container, "summarizer_conversation_id", "summarize", params={"sentences": sentences, "fields": fields}, firstRequest=(link if link else uploaded_file))

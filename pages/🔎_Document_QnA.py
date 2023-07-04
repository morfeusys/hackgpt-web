import streamlit as st
from agent.chat import init_agent


def form(init):
    st.markdown("# 🔎 Document QnA")
    st.markdown("_This agent answers any questions through the uploaded document or link_")
    st.divider()

    link = st.text_input(label="Paste here a direct link to the document or page")
    uploaded_file = st.file_uploader(label="Or upload file", type=["pdf", "doc", "docx", "xlsx", "txt", "mp3", "wav", "text", "md"])

    if st.form_submit_button("Create"):
        if link or uploaded_file:
            init({
                "type": "retrievalqa",
                "info": {
                    "icon": "🔎",
                    "title": "Document QnA",
                    "prompt": "Okay! Now you can ask me anything about this document in conversational manner and I will try to answer."
                },
                "params": {
                    "document": uploaded_file if uploaded_file else link
                }
            })


st.set_page_config(page_title="Document QnA agent", page_icon="🔎")
init_agent("qna_conversation", form)

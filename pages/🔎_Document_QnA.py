import streamlit as st
from agent.chat import init_agent


def form(init):
    link = st.text_input(label="Link to the document or web page")
    uploaded_file = st.file_uploader(label="Or upload document file", type=["pdf", "doc", "docx", "xlsx", "pptx", "txt", "mp3", "wav", "text", "md"])

    if st.form_submit_button("Create"):
        if link or uploaded_file:
            init({
                "document": uploaded_file if uploaded_file else link
            })


init_agent(
    key="qna_conversation",
    form_builder=form,
    agent_type="retrievalqa",
    agent_info={
        "icon": "🔎",
        "title": "Document QnA",
        "description": "This agent answers any questions about the uploaded document or link content",
        "prompt": "Okay! Now you can ask me anything about this document in conversational manner and I will try to answer."
    }
)

import streamlit as st
from chat.chat import create_agent
from chat.chat import init_chat

container = st.empty()
if st.session_state.get("qna_conversation_id"):
    init_chat(container, "qna_conversation_id")
else:
    with container.form("qna_form", clear_on_submit=True):
        st.markdown("# Document QnA")
        st.markdown("_This agent answers any questions through the uploaded document or link_")
        st.divider()

        link = st.text_input(label="Paste here a direct link to your document")
        uploaded_file = st.file_uploader(label="Or upload file", type=["pdf", "doc", "docx", "xlsx", "txt", "mp3", "wav", "text", "md"])
        if st.form_submit_button("Create"):
            if link or uploaded_file:
                create_agent(container, "qna_conversation_id", "retrievalqa", firstRequest=(link if link else uploaded_file))

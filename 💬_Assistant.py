import streamlit as st
from chat.chat import create_agent
from chat.chat import init_chat

container = st.empty()
if st.session_state.get("assistant_conversation_id"):
    init_chat(container, "assistant_conversation_id")
else:
    with container.form("assistant_form", clear_on_submit=True):
        st.markdown("# Assistant")
        st.markdown("_This agent chats with you as you wish_")
        st.divider()

        role = st.text_area(label="Assistant role")
        if st.form_submit_button("Create"):
            create_agent(container, "assistant_conversation_id", "chat", params={
                "prompt": role
            })

import streamlit as st
from agent.chat import init_agent


def form(init):
    st.markdown("# 💬 Assistant")
    st.markdown("_This agent chats with you as you wish_")
    st.divider()

    role = st.text_area(
        key="assistant_role",
        label="Assistant role _(optional)_",
        placeholder="For example: Act as a Python developer, write clean and beautiful code"
    )

    if st.form_submit_button("Create"):
        init({
            "type": "chat",
            "info": {
                "icon": "💬",
                "title": "Assistant",
                "prompt": "_I'm ready! Let's chat!_",
            },
            "params": {
                "prompt": role
            }
        })


st.set_page_config(page_title="Assistant agent", page_icon="💬")
init_agent("assistant_conversation", form)

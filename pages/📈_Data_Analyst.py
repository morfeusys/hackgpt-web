import streamlit as st
from chat.chat import create_agent
from chat.chat import init_chat

container = st.empty()
if st.session_state.get("data_analyst_conversation_id"):
    init_chat(container, "data_analyst_conversation_id")
else:
    with container.form("data_analyst_form", clear_on_submit=True):
        st.markdown("# Data Analyst")
        st.markdown("_This agent analyses your datasets and answers in conversational manner_")
        st.divider()

        dataset = st.text_input(label="A link to the dataset you wish to analyse.")
        if st.form_submit_button("Create"):
            if dataset:
                create_agent(container, "data_analyst_conversation_id", "api", params={"url": "https://hackgpt-test.just-ai.com/jupychat",  "model": "gpt-4-0613", "prompt": ("Act as a data scientist. Use this dataset " + dataset), "noParse": True})

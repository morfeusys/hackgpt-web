import streamlit as st
from agent.chat import init_agent


def form(init):
    st.markdown("# 📈 Data Analyst")
    st.markdown("_This agent analyses your datasets and answers in conversational manner_")
    st.divider()

    dataset = st.text_input(label="A link to CSV dataset you wish to analyse.")
    uploaded_file = st.file_uploader(label="Or upload your dataset here", type=["csv", "tsv"])

    if st.form_submit_button("Create"):
        if dataset or uploaded_file:
            init({
                "type": "api",
                "startRequest": uploaded_file if uploaded_file else dataset,
                "info": {
                    "icon": "📈",
                    "title": "Data Analyst",
                    "prompt": "Okay, now please tell what would you like to fetch from this dataset."
                },
                "params": {
                    "url": "https://hackgpt-test.just-ai.com/jupychat",
                    "model": "gpt-4-0613",
                    "prompt": "Act as a data scientist."
                },
                "schema": {
                    "noParse": True
                }
            })


st.set_page_config(page_title="Data Analyst agent", page_icon="📈")
init_agent("data_analyst_conversation", form)

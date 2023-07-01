import streamlit as st
from chat.chat import init_agent


def form(init):
    st.markdown("# 📈 Data Analyst")
    st.markdown("_This agent analyses your datasets and answers in conversational manner_")
    st.divider()

    dataset = st.text_input(label="A link to CSV dataset you wish to analyse.")
    uploaded_file = st.file_uploader(label="Or upload your dataset here", type=["csv", "tsv"])

    if st.form_submit_button("Create"):
        if dataset or uploaded_file:
            init(
                type="api",
                first_request=(dataset if dataset else uploaded_file),
                params={
                    "url": "https://hackgpt-test.just-ai.com/jupychat",
                    "model": "gpt-4-0613",
                    "prompt": "Act as a data scientist.",
                    "noParse": True
                }
            )


st.set_page_config(page_title="Data Analyst agent", page_icon="📈")
init_agent("data_analyst_conversation", form)

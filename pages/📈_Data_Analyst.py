import streamlit as st
from agent.chat import init_agent


def form(init):
    dataset = st.text_input(label="A link to CSV dataset")
    uploaded_file = st.file_uploader(label="Or upload your dataset file", type=["csv", "tsv"])

    if st.form_submit_button("Create"):
        if dataset or uploaded_file:
            init({
                "dataset": uploaded_file if uploaded_file else dataset,
                "url": "https://hackgpt-test.just-ai.com/jupychat",
                "model": "gpt-4-0613",
                "prompt": "Act as a data scientist. {#dataset}Use this dataset {dataset}{/dataset}.",
                "noParse": True
            })


init_agent(
    key="data_analyst_conversation",
    form_builder=form,
    agent_type="api",
    agent_info={
        "icon": "📈",
        "title": "Data Analyst",
        "description": "This agent analyses your datasets and answers in conversational manner",
        "prompt": "Okay, {#dataset}now please tell what would you like to fetch from this dataset.{/dataset}{^dataset}now please send me any dataset file or even a public link to file, and then you could ask me to analyse it as you wish!{/dataset}"
    }
)

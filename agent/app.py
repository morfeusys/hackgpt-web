import streamlit as st
from chat import create_agent_from_template


params = st.experimental_get_query_params()

if "id" in params:
    template_id = params["id"][0]
    if template_id:
        create_agent_from_template(template_id)

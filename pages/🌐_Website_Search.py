import streamlit as st
from chat.chat import init_agent


def form(init):
    st.markdown("# 🌐 Website search")
    st.markdown("_This agent answers any questions through the entire website_")
    st.divider()

    url = st.text_input(label="Paste here a URL of starting page to parse")
    noCache = st.checkbox(label="Disable caching")
    if st.form_submit_button("Create"):
        if url:
            init(
                type="retrievalqa",
                prompt=f'_Ready! Now send me any questions regarding the content of {url}_',
                params={
                    "url": url,
                    "noCache": noCache
                }
            )


st.set_page_config(page_title="Website search agent", page_icon="🌐")
init_agent("websearch_conversation", form)

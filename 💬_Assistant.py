import streamlit as st
from agent.chat import init_agent


def form(init):
    model = st.selectbox(
        label="GPT model",
        options=["gpt-3.5-turbo", "gpt-4"],
        help="GPT-3.5 is faster and cheaper, but GPT-4 is better for complex tasks"
    )

    role = st.text_area(
        key="assistant_role",
        label="Assistant role _(optional)_",
        placeholder="For example: Act as a Python developer, write clean and beautiful code",
        help="This is a prompt that controls the assistant behaviour"
    )

    st.caption("[Find here](https://prompts.chat/) some great prompt examples")

    if st.form_submit_button("Create"):
        init({
            "prompt": role,
            "model": model
        })


init_agent(
    key="assistant_conversation",
    form_builder=form,
    agent_type="chat",
    agent_info={
        "icon": "💬",
        "title": "Assistant",
        "description": "This agent chats with you as you wish",
        "prompt": "I'm ready! Let's chat!",
    }
)

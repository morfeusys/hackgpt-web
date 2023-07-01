import io

import streamlit as st
import requests
import json
import random
import time

agents_url = "https://hackgpt-test.just-ai.com"


def init_agent(key, formBuilder, file_input=False):
    container = st.empty()
    if st.session_state.get(key):
        init_chat(container, key, file_input=file_input)
    else:
        def init(type, params={}, prompt=None, first_request=None):
            create_agent(container, key, type, params, prompt, first_request, file_input)

        with container.form(key + "_form", clear_on_submit=True):
            formBuilder(init)


def clean_session(key):
    conversation_id = st.session_state[key]
    del st.session_state[key]
    del st.session_state["chat_history_" + conversation_id]


def create_agent(container, key, type, params={}, prompt=None, first_request=None, file_input=False):
    container.info("⏳ Please wait, while I am building your agent...")
    config = {"type": type, "params": params}
    response = requests.post(agents_url + "/agent/create", data=json.dumps(config), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        st.session_state[key] = response.text
        init_chat(container, key, prompt, first_request, file_input)
    else:
        container.error("Cannot create agent: " + str(response.status_code))


def init_chat(container, key, prompt=None, first_request=None, file_input=False):
    if st.sidebar.button("🧹 Close this conversation", use_container_width=True):
        clean_session(key)
        st.experimental_rerun()

    conversation_id = st.session_state[key]
    history_key = "chat_history_" + conversation_id

    if st.session_state.get(history_key):
        for message in st.session_state[history_key]:
            st.chat_message("user" if message["type"] == "request" else "assistant").markdown(message["text"])
    else:
        container.info("⏳ Loading conversation... Please wait...")
        response = requests.get(agents_url + "/agent/conversation/" + conversation_id)
        if response.status_code == 200:
            data = response.json()
            st.session_state[history_key] = data["history"]
            for message in data["history"]:
                st.chat_message("user" if message["type"] == "request" else "assistant").markdown(message["text"])
        else:
            container.error("Sorry, but I cannot load this chat...")
            st.stop()

    if first_request is not None:
        container.info("⏳ Processing...")
        if isinstance(first_request, io.IOBase):
            response = requests.post(agents_url + "/agent/conversation/" + conversation_id, files={"file": first_request})
        else:
            response = requests.post(agents_url + "/agent/conversation/" + conversation_id, data=first_request.encode("utf-8"), headers={'Content-Type': 'text/plain'})

        if response.status_code == 200:
            data = response.json()["response"]
            data.update({"type": "response"})
            st.session_state[history_key].append(data)
            st.experimental_rerun()
        else:
            container.error("Sorry, but I cannot proceed this request: " + str(response.status_code))
            st.stop()
    elif prompt is not None and len(prompt):
        st.session_state[history_key].append({"type": "response", "text": prompt})
        st.experimental_rerun()

    if file_input:
        file = container.file_uploader(label="Upload your file here", type=file_input)
        if file:
            st.session_state[history_key].append({"type": "request", "text": file.name})
            st.chat_message("user").text(file.name)
            process_query(conversation_id, history_key, file)
    elif query := container.chat_input("What you want to ask"):
        st.chat_message("user").markdown(query)
        st.session_state[history_key].append({"type": "request", "text": query})
        process_query(conversation_id, history_key, query)


def process_query(conversation_id, history_key, query):
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder_message = ""
        for chunk in random.choice(waiting_messages).split():
            placeholder_message += chunk + " "
            time.sleep(0.07)
            placeholder.text(placeholder_message + "▌")
        placeholder.text(placeholder_message)

        if isinstance(query, io.IOBase):
            response = requests.post(
                agents_url + "/agent/conversation/" + conversation_id,
                files={"file": query})
        else:
            response = requests.post(
                agents_url + "/agent/conversation/" + conversation_id,
                data=query.encode("utf-8"),
                headers={'Content-Type': 'text/plain'})

        if response.status_code == 200:
            data = response.json()["response"]
            data.update({"type": "response"})
            st.session_state[history_key].append(data)
            placeholder.markdown(data["text"])
        else:
            placeholder.error("Sorry, but I cannot process you request now... " + str(response.status_code))


waiting_messages = [
    "Just a sec... or two, or three... 🤔",
    "Please wait while I work my magic... or Google it 🧙‍♂️🔍",
    "Hang on tight... or just go take a coffee 💪☕️",
    "One moment please... or the next hour 🕑🕒🕓",
    "Let me check that for you... or just pretend I did 🔍👀",
    "Please hold... or go play with your cat 🤲🐱",
    "Calculating... or just making some random numbers 🔢🤔",
    "Processing... or just scrolling Twitter 🖥️🐦",
    "Searching... or just checking my horoscope 🔍🔮",
    "Analyzing... or just watching cat videos 🧠😹",
    "Thinking... or just daydreaming 🤔🌈",
    "Brainstorming... or just people watching 💡🧐",
    "Meditating... or just napping 🧘‍♀️💤",
    "Considering... or just procrastinating 🤔🕰️",
    "Evaluating... or just making a guess 📈🤔",
    "Mulling it over... or just enjoying the silence 🤔😌",
    "Weighing the options... or just going with the flow 🤔🌊",
    "Making a decision... or just flipping a coin 🤔💰",
    "Contemplating... or just checking my phone 🤔📱",
    "Taking a break... or just watching a funny video 💤😆",
    "Your request is being processed faster than a cheetah on steroids 😎",
    "Hold tight, your request is cooking in the oven 🔥",
    "Your request is being taken care of like a baby 🤱",
    "Don't worry, your request is in the best hands 🤝",
    "Your request is getting handled like a priority 📢",
    "Just a few more minutes and your request will be handled 🤗",
    "I'm working hard to get your request done quickly 💪",
    "Hang on tight, I'm almost finished with your request 🙌",
    "Don't worry, your request is in the best hands of mine 🤝",
    "Get ready for a speedy response to your request from me 🚀",
    "It won't take long, I'm giving this request my full attention 👀",
    "You can count on me to deliver your request on time 🕰",
    "I'm handling your request with utmost care 🤗",
    "Hold tight, your request is cooking in the oven under my watchful eye 🔥"
]
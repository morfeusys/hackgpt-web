import io

import streamlit as st
import requests
import json
import os

agents_url = "https://hackgpt-test.just-ai.com"

def clean_session(key):
    conversation_id = st.session_state[key]
    del st.session_state[key]
    del st.session_state["chat_history_" + conversation_id]

def create_agent(container, key, type, params={}, firstRequest=None):
    container.info("Please wait, while I am building your agent...")
    config = {"type": type, "params": params}
    response = requests.post(agents_url + "/agent/create", data=json.dumps(config), headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        st.session_state[key] = response.text
        init_chat(container, key, firstRequest)
    else:
        container.error("Cannot create agent: " + str(response.status_code))

def init_chat(container, key, firstRequest=None):
    if st.sidebar.button("🧹 Clean session"):
        clean_session(key)
        st.experimental_rerun()

    conversation_id = st.session_state[key]
    history_key = "chat_history_" + conversation_id

    if st.session_state.get(history_key):
        for message in st.session_state[history_key]:
            st.chat_message("user" if message["type"] == "request" else "assistant").markdown(message["text"])
    else:
        container.info("Loading... Please wait...")
        response = requests.get(agents_url + "/agent/conversation/" + conversation_id)
        if response.status_code == 200:
            data = response.json()
            st.session_state[history_key] = data["history"]
            for message in data["history"]:
                st.chat_message("user" if message["type"] == "request" else "assistant").markdown(message["text"])
        else:
            container.error("Sorry, but I cannot load this chat...")
            st.stop()

    if firstRequest is not None:
        if isinstance(firstRequest, io.IOBase):
            response = requests.post(agents_url + "/agent/conversation/" + conversation_id, files={"file": firstRequest})
        else:
            response = requests.post(agents_url + "/agent/conversation/" + conversation_id, data=firstRequest.encode("utf-8"), headers={'Content-Type': 'text/plain'})

        if response.status_code == 200:
            data = response.json()["response"]
            data.update({"type": "response"})
            st.session_state[history_key].append(data)
            st.experimental_rerun()
        else:
            container.error("Sorry, but I cannot proceed this request: " + str(response.status_code))
            st.stop()

    if prompt := container.chat_input("Say something"):
        st.chat_message("user").markdown(prompt)
        st.session_state[history_key].append({"type": "request", "text": prompt})

        response = requests.post(
            agents_url + "/agent/conversation/" + conversation_id,
            data=prompt.encode("utf-8"),
            headers={'Content-Type': 'text/plain'})

        if response.status_code == 200:
            data = response.json()["response"]
            data.update({"type": "response"})
            st.session_state[history_key].append(data)
            st.chat_message("assistant").markdown(data["text"])
        else:
            st.error("Sorry, but I cannot process you request now... " + str(response.status_code))

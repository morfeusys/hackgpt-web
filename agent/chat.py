import io
import chevron
import streamlit as st
import requests
import json
import random
import time
import os


agents_api = os.environ["AGENTS_API"] if "AGENTS_API" in os.environ else "http://localhost:3000"
agents_url = os.environ["AGENTS_URL"] if "AGENTS_URL" in os.environ else "http://localhost:8502"

menu_items = {
    "About": "Created by [Just AI](https://just-ai.com)"
}


def hide_style():
    st.markdown("""
    <style>
        footer {display: none;}
        a[href="https://streamlit.io/cloud"] {display: none;}
        div.stActionButton {display: none;}
    </style>
    """, unsafe_allow_html=True)


def init_agent(key, form_builder, agent_type, agent_info, agent_input=None):
    if agent_input is None:
        agent_input = {"type": "text"}
    st.set_page_config(page_title=agent_info["title"], page_icon=agent_info["icon"], menu_items=menu_items)
    hide_style()
    container = st.empty()
    if st.session_state.get(key):
        init_chat(container, key)
    else:
        def init(params):
            config = {
                "type": agent_type,
                "info": agent_info,
                "params": params,
                "input": agent_input
            }
            create_agent(container, key, config)

        with container.form(key + "_form"):
            st.title(f'{agent_info["icon"]} {agent_info["title"]}')
            st.markdown(f'_{agent_info["description"]}_')
            st.divider()
            form_builder(init)


def upload_file(file):
    response = requests.post(agents_api + "/files/upload", files={"file": file})
    if response.status_code == 200:
        return response.text
    else:
        return None


def clean_session(key):
    conversation = st.session_state[key]
    del st.session_state[key]
    del st.session_state["chat_history_" + conversation["conversation_id"]]
    requests.delete(agents_api + "/agents/conversation/" + conversation["conversation_id"])


def upload_files(params):
    for key, value in params.items():
        if isinstance(value, io.IOBase):
            url = upload_file(value)
            if url:
                params[key] = url
            else:
                raise Exception("cannot upload file")
        elif isinstance(value, dict):
            upload_files(value)


def create_agent_from_template(template_id):
    key = "conversation_" + template_id
    if st.session_state.get(key):
        info = st.session_state[key]["config"]["info"]
        st.set_page_config(page_title=info["title"], page_icon=info["icon"], menu_items=menu_items)
        hide_style()
        st.markdown(f'## {info["icon"]} {info["title"]}')
        st.markdown(f'ℹ️ {info["description"]}')
        st.divider()
        init_chat(st.empty(), key)
    else:
        response = requests.get(agents_api + "/agent/template/" + template_id)
        if response.status_code == 200:
            config = response.json()
            st.set_page_config(page_title=config["info"]["title"], page_icon=config["info"]["icon"], menu_items=menu_items)
            hide_style()
            create_agent(st.empty(), key, config)
        else:
            hide_style()
            st.error("### Sorry, but this agent was not found...\n" +
                            "Please make sure you use the correct link.")


def create_agent(container, key, config):
    container.info("⏳ Please wait, while I am building your agent...")
    try:
        upload_files(config)
    except Exception as e:
        container.error("**Sorry, but I cannot create this agent now**: " + str(e))
        st.stop()

    response = requests.post(agents_api + "/agent/create", data=json.dumps(config),
                             headers={'Content-Type': 'application/json'})
    if response.status_code == 200:
        template = requests.get(agents_api + "/agent/conversation/" + response.text).json()
        st.session_state[key] = {
            "config": config,
            "conversation_id": response.text,
            "template_id": template["templateId"]
        }
        init_chat(container, key)
    else:
        container.error("Cannot create agent: " + str(response.status_code))


def init_chat(container, key):
    conversation = st.session_state[key]
    conversation_id = conversation["conversation_id"]
    config = conversation["config"]
    history_key = "chat_history_" + conversation_id

    show_sidebar = "id" not in st.experimental_get_query_params()
    if show_sidebar:
        publish_button = st.sidebar.button("👋 Publish this agent", use_container_width=True)

        if st.sidebar.button("🔄 Restart this conversation", use_container_width=True):
            params = config["params"] if "params" in config else {}
            del st.session_state[history_key]
            requests.put(agents_api + "/agent/conversation/" + conversation_id, data=json.dumps(params),
                         headers={'Content-Type': 'application/json'})
            st.experimental_rerun()

        if st.sidebar.button("🧹 Close this conversation", use_container_width=True):
            clean_session(key)
            st.experimental_rerun()

    if st.session_state.get(history_key):
        for message in st.session_state[history_key]:
            st.chat_message("user" if message["type"] == "request" else "assistant").markdown(message["text"])
    else:
        container.info("⏳ Loading conversation... Please wait...")
        response = requests.get(agents_api + "/agent/conversation/" + conversation_id)
        if response.status_code == 200:
            data = response.json()
            st.session_state[history_key] = data["history"]
            for message in data["history"]:
                st.chat_message("user" if message["type"] == "request" else "assistant").markdown(message["text"])
        else:
            container.error("Sorry, but I cannot load this chat...")
            st.stop()

    if not st.session_state.get(history_key):
        if "startRequest" in config:
            container.info("⏳ Initializing your agent, please wait a bit...")
            response = requests.post(
                agents_api + "/agent/conversation/" + conversation_id,
                data=config["startRequest"].encode("utf-8"), headers={'Content-Type': 'text/plain'}
            )

            if response.status_code == 200:
                data = response.json()["response"]
                data.update({"type": "response"})
                st.session_state[history_key].append(data)
                st.experimental_rerun()
            else:
                container.error("Sorry, but I cannot start this agent: " + str(response.status_code))
                st.stop()
        elif "prompt" in config["info"]:
            data = {}
            if "params" in config:
                data.update(config["params"])
            if "schema" in config:
                data.update(config["schema"])

            text = render(config["info"]["prompt"], data)
            st.session_state[history_key].append({"type": "response", "text": text})
            st.experimental_rerun()

    if "input" in config and config["input"]["type"] == "file":
        file = container.file_uploader(label="Upload your file here", type=config["input"]["filter"], accept_multiple_files=True)
        if file:
            files = file if isinstance(file, list) else [file]
            for file in files:
                if not any(item["text"] == file.name for item in st.session_state[history_key]):
                    st.session_state[history_key].append({"type": "request", "text": file.name})
                    st.chat_message("user").text(file.name)
                    process_query(conversation_id, history_key, file)

    elif query := container.chat_input("What you want to ask"):
        st.chat_message("user").markdown(query)
        st.session_state[history_key].append({"type": "request", "text": query})
        process_query(conversation_id, history_key, query)

    if show_sidebar and publish_button:
        with st.chat_message("assistant"):
            st.markdown("👋 _Publish this agent to allow others to use it without any settings!_")
            st.markdown("Here you have to define title and description that other users will see.")
            with st.form("publish_agent_form_" + conversation_id):
                st.text_input(key="agent_title_" + key, label="Title", placeholder="Your agent descriptive title",
                              value=config["info"].get("title") or "")
                st.text_area(key="agent_description_" + key, label="Description",
                             placeholder="Make it clear about how this agent works and what input it expects.",
                             value=config["info"].get("description") or "")
                st.form_submit_button("Publish", on_click=publish_agent, args=(key,))


def publish_agent(key):
    title = st.session_state["agent_title_" + key]
    description = st.session_state["agent_description_" + key]
    if title and description:
        conversation = st.session_state[key]
        config = conversation["config"]
        config["info"]["title"] = title
        config["info"]["description"] = description
        history_key = "chat_history_" + conversation["conversation_id"]

        response = requests.post(agents_api + "/agent/template/" + conversation["template_id"], data=json.dumps(config),
                                 headers={'Content-Type': 'application/json'})

        if response.status_code == 200:
            url = agents_url + "?id=" + conversation["template_id"]
            st.session_state[history_key].append(
                {"type": "response", "text": f'👋 **Here is your agent public URL [{title}]({url})**\n\n'
                                             f'Now you can share it with anybody to allow them to interact with your agent.\n\n'
                                             f'_Note that nobody can change your agent configuration._'})
        else:
            st.session_state[history_key].append({"type": "response",
                                                  "text": f'_Sorry, I cannot publish your agent now.., Error code: {response.status_code}_'})


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
                agents_api + "/agent/conversation/" + conversation_id,
                files={"file": query})
        else:
            response = requests.post(
                agents_api + "/agent/conversation/" + conversation_id,
                data=query.encode("utf-8"),
                headers={'Content-Type': 'text/plain'})

        if response.status_code == 200:
            data = response.json()["response"]
            data.update({"type": "response"})
            st.session_state[history_key].append(data)
            placeholder.markdown(data["text"])
        else:
            placeholder.error("Sorry, but I cannot process you request now... " + str(response.status_code))


def render(template, data):
    return chevron.render(template, data, def_ldel='{', def_rdel='}')

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

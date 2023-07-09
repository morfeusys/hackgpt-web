import streamlit as st
from agent.chat import init_agent


def form(init):
    sentences = st.number_input(label="The number of sentences in summary", min_value=1)
    fields = st.text_input(label="Comma separated fields that should be included in summary _(optional)_", help="Only these fileds will be presented in summary if set")
    language = st.selectbox(label="Language of summary", options=[
        "",
        "Afrikaans",
        "Albanian",
        "Amharic",
        "Arabic",
        "Armenian",
        "Azerbaijani",
        "Basque",
        "Belarusian",
        "Bengali",
        "Bosnian",
        "Bulgarian",
        "Catalan",
        "Cebuano",
        "Chichewa",
        "Chinese",
        "Corsican",
        "Croatian",
        "Czech",
        "Danish",
        "Dutch",
        "English",
        "Esperanto",
        "Estonian",
        "Filipino",
        "Finnish",
        "French",
        "Frisian",
        "Galician",
        "Georgian",
        "German",
        "Greek",
        "Gujarati",
        "Haitian Creole",
        "Hausa",
        "Hawaiian",
        "Hebrew",
        "Hindi",
        "Hmong",
        "Hungarian",
        "Icelandic",
        "Igbo",
        "Indonesian",
        "Irish",
        "Italian",
        "Japanese",
        "Javanese",
        "Kannada",
        "Kazakh",
        "Khmer",
        "Kinyarwanda",
        "Korean",
        "Kurdish",
        "Kyrgyz",
        "Lao",
        "Latin",
        "Latvian",
        "Lithuanian",
        "Luxembourgish",
        "Macedonian",
        "Malagasy",
        "Malay",
        "Malayalam",
        "Maltese",
        "Maori",
        "Marathi",
        "Mongolian",
        "Myanmar (Burmese)",
        "Nepali",
        "Norwegian",
        "Odia (Oriya)",
        "Pashto",
        "Persian",
        "Polish",
        "Portuguese",
        "Punjabi",
        "Romanian",
        "Russian",
        "Samoan",
        "Scots Gaelic",
        "Serbian",
        "Sesotho",
        "Shona",
        "Sindhi",
        "Sinhala",
        "Slovak",
        "Slovenian",
        "Somali",
        "Spanish",
        "Sundanese",
        "Swahili",
        "Swedish",
        "Tajik",
        "Tamil",
        "Tatar",
        "Telugu",
        "Thai",
        "Turkish",
        "Turkmen",
        "Ukrainian",
        "Urdu",
        "Uyghur",
        "Uzbek",
        "Vietnamese",
        "Welsh",
        "Xhosa",
        "Yiddish",
        "Yoruba",
        "Zulu"
    ])

    if st.form_submit_button("Create"):
        init({
            "sentences": sentences,
            "fields": fields,
            "language": language
        })


init_agent(
    key="summarizer_conversation",
    form_builder=form,
    agent_type="summarize",
    agent_info={
        "icon": "💡",
        "title": "Summarizer",
        "description": "This agent summarizes any documents with defined rules",
        "prompt": "Now you can send me any web page URL or document, and I will summarize it for you."
    },
    agent_input={
        "type": "file",
        "filter": ["pdf", "doc", "docx", "xlsx", "pptx", "txt", "mp3", "wav", "text", "md", "m4a", "ogg", "opus", "mp4"]
    }
)

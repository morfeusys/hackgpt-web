import streamlit as st
from chat.chat import init_agent


def form(init):
    st.markdown("# 💡 Summarizer")
    st.markdown("_This agent summarizes any documents with defined rules_")
    st.divider()

    sentences = st.number_input(label="The number of sentences in summary", min_value=1)
    fields = st.text_input(label="Comma separated fields that should be included in summary (optional)")
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
            "type": "summarize",
            "input": {
                "type": "file",
                "filter": ["pdf", "doc", "docx", "xlsx", "txt", "mp3", "wav", "text", "md"]
            },
            "info": {
                "icon": "💡",
                "title": "Summarizer"
            },
            "params": {
                "sentences": sentences,
                "fields": fields,
                "language": language
            }
        })


st.set_page_config(page_title="Simmarizer agent", page_icon="💡")
init_agent("summarizer_conversation", form)

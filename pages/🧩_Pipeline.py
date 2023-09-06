import streamlit as st
from agent.chat import init_agent


def form(init):
    with st.expander(label="ℹ️ How to use"):
        """
        #### Short description
        This agent creates a pipeline to process your documents through it to get a resulting text you need.
        
        #### Example
        [Here is an example](https://telegra.ph/Follow-up-example-09-06) of pipeline that processes a document to generate meeting follow-up.
        
        #### How it works
        The created pipeline processes any document using next steps:
        
        1. Parse a document into a raw text
        2. Split raw text into _complete sentences_
        3. Join sentences into _fragments_ using _Fragment chunk size_ parameter
        4. Process _First prompt_ if provided or _Intermediate prompt_ using _templating_ (see below) and collect result
        5. Process _Intermediate prompt_ using _templating_ (see below) for each of rest _fragment_ and collect results
        6. Process _Final prompt_ if provided using _templating_ (see below) and collect result  
        
        
        #### Result
        _Pipeline returns the very last result collected at the end._
        
        #### Templating
        You have to use [Mustache](https://mustache.github.io/mustache.5.html) templating in your prompts to include fragments and other attributes.
        
        > Note that you have to use single `{` and `}` brackets instead of double.
        
        These attributes are available and can be used in prompts:
        
        - `{language}` - selected language
        - `{fragment}` - text of current fragment
        - `{index}` - index number of current fragment (1-based)
        - `{results}` - list of previously collected results, each contains `{text}` and `{index}`
        - `{firstResult}` - text of first item in `{results}`
        - `{lastResult}` - text of last item in `{results}`
        """

    model = st.selectbox(label="Model", help="Which GPT model to use", options=["gpt-3.5-turbo-16k", "gpt-3.5-turbo", "gpt-4"])
    language = st.selectbox(label="Language", help="Will be available via _{language}_ in all your prompts", options=[
        "English",
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
    chunkSize = st.number_input(label="Fragment chunk size", help="Size of text fragment chunk in tokens. Leave 0 to calculate optimal.", value=0)

    systemPrompt = st.text_area(label="System prompt", placeholder="Type here some important rules", help="Applied on each step of pipeline")
    firstPrompt = st.text_area(label="First prompt", placeholder="Type here a prompt that will be applied to first text fragment. Optional.", help="Applied only to very first text fragment")
    intermediatePrompt = st.text_area(label="Intermediate prompt", placeholder="Type here a prompt that will be applied to each text fragment between first and last", help="Applied only to fragments between first and last.")
    finalPrompt = st.text_area(label="Final prompt", placeholder="Type here a prompt that will be applied to the result. Optional.", help="Applied only to the resulting text")

    if st.form_submit_button("Create"):
        init({
            "model": model,
            "language": language,
            "chunkSize": chunkSize,
            "systemPrompt": systemPrompt,
            "firstPrompt": firstPrompt,
            "intermediatePrompt": intermediatePrompt,
            "finalPrompt": finalPrompt
        })


init_agent(
    key="pipeline_conversation",
    form_builder=form,
    agent_type="pipeline",
    agent_info={
        "icon": "🧩",
        "title": "Pipeline",
        "description": "This agent creates pipeline to process documents",
        "prompt": "Now you can send me any document, and I will apply your pipeline to it."
    },
    agent_input={
        "type": "file",
        "filter": ["pdf", "doc", "docx", "xlsx", "pptx", "txt", "mp3", "wav", "text", "md", "m4a", "ogg", "opus", "mp4"]
    }
)
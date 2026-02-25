import streamlit as st
from dotenv import load_dotenv
from langchain_community.llms.oci_generative_ai import Provider
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

import os

from logic.chathelper import chathelper

load_dotenv()

#streamlit page setup
st.set_page_config(
    page_title="AI Chatbot",
    page_icon= "👤", # search from emojiDB for emojis
    layout="centered",

)

st.title("💬 Generative AI Chatbot")


#Initiate chat history
if "chat_history" not in st.session_state:
      st.session_state.chat_history = []

for message in st.session_state.chat_history:
     with st.chat_message(message["role"]):
          st.markdown(message["content"])


# Provider → Models mapping
PROVIDERS = {
    "OpenAI": [
        "gpt-4o-mini",
        "gpt-4o",
        "gpt-4.1",
        "gpt-4.1-2025-04-14"
    ],
    "Gemini": [
        "gemini-2.5-pro",
        "gemini-2.5-flash",
    ],
    "Groq": [
        "llama-3.1-8b-instant",
        "llama-3.3-70b-versatile"
    ],
    "Ollama": [
        "gemma3",
        "llama3.1"
    ]
}

# Provider dropdown

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")

    provider = st.selectbox(
        "Select Provider",
        list(PROVIDERS.keys())
    )

    model = st.selectbox(
        "Select Model",
        PROVIDERS[provider]
    )

    st.write(f"Provider: **{provider}**")
    st.write(f"Model: **{model}**")
user_prompt = st.chat_input("Ask chatbot")
if user_prompt:
   if provider == "OpenAI":
      llm = ChatOpenAI(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
      )
      chathelper(llm,user_prompt)

   elif provider == "Gemini":
        llm = ChatGoogleGenerativeAI(
          model=model,
          google_api_key=os.getenv("GEMINI_API_KEY"),
          temperature=0
         )
        chathelper(llm, user_prompt)
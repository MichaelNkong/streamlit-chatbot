

import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
import traceback
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
        "qwen/qwen3-32b",
        "llama-3.3-70b-versatile",
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
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
      )
      try:
         chathelper(llm, user_prompt)
      except Exception as e:
            st.error(f"Error: {e}")
            st.text(traceback.format_exc())

   elif provider == "Gemini":
        llm = ChatGoogleGenerativeAI(
          model=model,
          google_api_key=os.getenv("GEMINI_API_KEY"),
          temperature=0
         )
        try:
            chathelper(llm, user_prompt)
        except Exception as e:
            st.error(f"Error: {e}")
            st.text(traceback.format_exc())

   elif provider == "Groq":
        llm = ChatGroq(
           model=model,
           api_key=os.getenv("GROQ_API_KEY"),
           temperature=0
        )
        try:
            chathelper(llm, user_prompt)
        except Exception as e:
            st.error(f"Error: {e}")
            st.text(traceback.format_exc())

   elif provider == "Ollama":
        llm = ChatOllama(
           model = model,
           temperature=0
           # other params...
        )
        try:
            chathelper(llm, user_prompt)
        except Exception as e:
            st.error(f"Error: {e}")

            st.text(traceback.format_exc())



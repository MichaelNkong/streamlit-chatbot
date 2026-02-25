import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
import os
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
provider = st.selectbox(
    "Select Provider",
    list(PROVIDERS.keys())
)

# Model dropdown (updates automatically)
model = st.selectbox(
    "Select Model",
    PROVIDERS[provider]
)

st.write(f"Provider: **{provider}**")
st.write(f"Model: **{model}**")
user_prompt = st.chat_input("Ask chatbot")
if provider == "OpenAI":
    llm = ChatOpenAI(
        model=model,
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )

    if user_prompt:
         # Show user message
       st.chat_message("user").markdown(user_prompt)

       # Save user message
       st.session_state.chat_history.append(
           {"role": "user", "content": user_prompt}
        )

       # Build prompt from full chat history
       prompt = ChatPromptTemplate.from_messages(
        st.session_state.chat_history
        )

        # Create chain
       chain = prompt | llm

       # Call model
       response = chain.invoke({})

        # Extract content
       assistant_message = response.content

       # Show assistant message
       st.chat_message("assistant").markdown(assistant_message)

    # Save assistant message
       st.session_state.chat_history.append(
          {"role": "assistant", "content": assistant_message}
       )
elif provider == "Gemini":
    llm = ChatGoogleGenerativeAI(
        model=model,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )
    if user_prompt:
        # Show user message
        st.chat_message("user").markdown(user_prompt)

        # Save user message
        st.session_state.chat_history.append(
            {"role": "user", "content": user_prompt}
        )

        # Convert history to LangChain messages
        messages = []
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            else:
                messages.append(AIMessage(content=msg["content"]))

        # Build prompt
        prompt = ChatPromptTemplate.from_messages(messages)

        # Create chain
        chain = prompt | llm

        # Call model
        response = chain.invoke({})

        assistant_message = response.content

        # Show assistant message
        st.chat_message("assistant").markdown(assistant_message)

        # Save assistant message
        st.session_state.chat_history.append(
            {"role": "assistant", "content": assistant_message}
        )
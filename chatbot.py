import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

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

llm = ChatOpenAI(model = "gpt-4.1-2025-04-14", temperature=0.0)
user_prompt = st.chat_input("Ask chatbot")
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
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage

from langchain_core.prompts import ChatPromptTemplate

def chathelper(llm, user_prompt):
    # Show user message
    st.chat_message("user").markdown(user_prompt)

    # Initialize chat_history if not exists
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Save user message
    st.session_state.chat_history.append(HumanMessage(content=user_prompt))

    # Build prompt from chat history
    prompt = ChatPromptTemplate.from_messages(st.session_state.chat_history)

    # Create chain
    chain = prompt | llm

    # Call model: pass no variables because we already converted messages to concrete HumanMessage/AIMessage
    response = chain.invoke({})

    # Extract content
    assistant_message = response.content

    # Show assistant message
    st.chat_message("assistant").markdown(assistant_message)

    # Save assistant message
    st.session_state.chat_history.append(AIMessage(content=assistant_message))
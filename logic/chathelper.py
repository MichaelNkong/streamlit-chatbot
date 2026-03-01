import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

def chathelper(llm, user_prompt):
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Escape curly braces in user input
    safe_user_prompt = user_prompt.replace("{", "{{").replace("}", "}}")

    # Show user message
    st.chat_message("user").markdown(user_prompt)

    # Save user message
    st.session_state.chat_history.append(
        {"role": "user", "content": safe_user_prompt}
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

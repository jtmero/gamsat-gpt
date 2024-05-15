import streamlit as st
import requests
import time
import openai

# Set API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Create an OpenAI client with your API key
openai_client = openai.Client(api_key=api_key)

# Retrieve the assistant you want to use
assistant = openai_client.beta.assistants.retrieve("asst_3no7SQcpD6vOpUHqMCL2cRUB")
assistant_id = assistant.id  # Extract assistant ID

# Create the title and subheader for the Streamlit page
st.title("GamsatGPT")
st.subheader("You can ask me to generate any kind of GAMSAT SIII question")

# Create a chat input for the prompt
prompt = st.chat_input("Why don't you ask me to make you a question?")

if prompt:
    # Display the user's question
    with st.chat_message("user"):
        st.write(prompt)

    # Create a new thread
    thread = openai_client.beta.threads.create(
        messages=[{"role": "user", "content": prompt}]
    )

    # Stream the question
    with openai_client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant_id,  # Ensure assistant_id is correctly defined
    ) as stream:
        for chunk in stream:
            if 'content' in chunk.delta:
                response_content += chunk.delta['content']
                with st.chat_message("assistant"):
                    st.write(response_content)

    # After the question is generated, ask the user for their answer
    user_answer = st.chat_input("What is your answer?")

    if user_answer:
        with st.chat_message("user"):
            st.write(user_answer)
        response_message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=user_answer
        )

    # Continue streaming to get reasoning
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
        ) as stream:
            for chunk in stream:
            if 'content' in chunk.delta:
                response_content += chunk.delta['content']
                with st.chat_message("assistant"):
                    st.write(response_content)

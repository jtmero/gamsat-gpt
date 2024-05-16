import streamlit as st
from openai import OpenAI

# Set up the chat
st.title("GamsatGPT")
intro = "Welcome to GamsatGPT. You can ask me to generate any kind of GAMSAT SIII question"

# Load the OpenAi client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Retrieve the assistant
assistant = client.beta.assistants.retrieve("asst_3no7SQcpD6vOpUHqMCL2cRUB")

# Initialize session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": intro}]
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your reply"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Append the prompt to the existing thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt)

    # Generate and display the assistant reply
    with st.spinner('Generating response...'):
        stream = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant.id,
            stream=True
        )

        for event in stream:
            response = st.write_stream(event)
            
        st.session_state.messages.append({"role": "assistant", "content": response})

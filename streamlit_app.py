import streamlit as st
from openai import OpenAI

# Set up the chat title and introduction
st.title("GamsatGPT")
intro = "Welcome to GamsatGPT. You can ask me to generate any kind of GAMSAT SIII question"

# Load the OpenAi client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Retrieve the assistant (replace with your assistant's ID)
assistant = client.beta.assistants.retrieve("asst_3no7SQcpD6vOpUHqMCL2cRUB")

# Initialize the session state for storing model and messages
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": intro}]

# Display the previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Enter new messages to chat from the user
if prompt := st.chat_input("Enter your reply"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create a thread
    thread = client.beta.threads.create()

    # Append the prompt to the thread as a message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt)

    # Generate the assistant reply and process the stream
    with st.spinner('Generating response...'):
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
        ) as stream:
            for event in stream:
                if event.type == 'message' and event.role == 'assistant':
                    assistant_response = event.content
                    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                    with st.chat_message("assistant"):
                        st.markdown(assistant_response)
                    break

import streamlit as st
import requests

# Set OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]

# Function to create the assistant
def create_assistant():
    url = "https://api.openai.com/v1/assistants"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "OpenAI-Beta": "assistants=v2"
    }
    data = {
        "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
        "name": "Math Tutor",
        "tools": [{"type": "code_interpreter"}],
        "model": "gpt-4-turbo"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        assistant_data = response.json()
        return assistant_data["id"]
    else:
        st.error(f"Error creating assistant: {response.text}")
        return None

# Create the assistant and store the ID
if "assistant_id" not in st.session_state:
    assistant_id = create_assistant()
    if assistant_id:
        st.session_state.assistant_id = assistant_id
    else:
        st.stop()

# Function to start a session
def start_session():
    url = f"https://api.openai.com/v1/assistants/{st.session_state.assistant_id}/sessions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        session_data = response.json()
        return session_data["id"]
    else:
        st.error(f"Error starting session: {response.text}")
        return None

# Start a session and store the session ID
if "session_id" not in st.session_state:
    session_id = start_session()
    if session_id:
        st.session_state.session_id = session_id
    else:
        st.stop()

# Function to send messages to the assistant
def send_message(messages):
    url = f"https://api.openai.com/v1/assistants/{st.session_state.assistant_id}/sessions/{st.session_state.session_id}/messages"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {"messages": messages}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error sending message: {response.text}")
        return None

# Create the chat interface
st.title("GamsatGPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Why don't you ask me to generate you a question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send message to the assistant
    response_data = send_message(st.session_state.messages)
    if response_data:
        assistant_response = response_data["choices"][0]["message"]["content"]

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

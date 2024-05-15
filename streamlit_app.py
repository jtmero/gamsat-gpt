import streamlit as st
import requests
import json

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

# Function to run a session
def run_session(messages):
    url = f"https://api.openai.com/v1/assistants/{st.session_state.assistant_id}/sessions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {"messages": messages}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error running session: {response.text}")
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

    # Run a session with the assistant
    response_data = run_session(st.session_state.messages)
    if response_data:
        run_id = response_data["id"]

        # Poll the run status
        run_status = response_data["status"]
        while run_status in ["in_progress", "queued"]:
            run_status_response = requests.get(f"https://api.openai.com/v1/assistants/{st.session_state.assistant_id}/sessions/{run_id}", headers=headers)
            run_status_data = run_status_response.json()
            run_status = run_status_data["status"]

        # Retrieve the run messages
        if run_status == "completed":
            messages_response = requests.get(f"https://api.openai.com/v1/assistants/{st.session_state.assistant_id}/sessions/{run_id}/messages", headers=headers)
            if messages_response.status_code == 200:
                messages_data = messages_response.json()
                assistant_response = messages_data["messages"][-1]["content"]
            else:
                assistant_response = "Sorry, there was an error retrieving the messages."
        else:
            assistant_response = "Sorry, the run did not complete successfully."

        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

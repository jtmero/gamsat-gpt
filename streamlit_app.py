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
        "instructions": "You are a helpful assistant.",
        "name": "Test Assistant",
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

st.write(f"Assistant ID: {st.session_state.assistant_id}")

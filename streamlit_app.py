import streamlit as st
import requests

api_key = st.secrets["OPENAI_API_KEY"]

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

if "assistant_id" not in st.session_state:
    assistant_id = create_assistant()
    if assistant_id:
        st.session_state.assistant_id = assistant_id
    else:
        st.stop()

st.write(f"Assistant ID: {st.session_state.assistant_id}")

def send_message(message):
    url = f"https://api.openai.com/v1/assistants/{st.session_state.assistant_id}/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "messages": [{"role": "user", "content": message}]
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        response_data = response.json()
        return response_data["choices"][0]["message"]["content"]
    else:
        st.error(f"Error sending message: {response.text}")
        return None

st.title("Simple OpenAI Assistant")

if prompt := st.text_input("Ask the assistant something:"):
    response = send_message(prompt)
    if response:
        st.write(f"Assistant response: {response}")

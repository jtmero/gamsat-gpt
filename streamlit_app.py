from openai import OpenAI
import streamlit as st
import requests

# Load the model
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
assistant_id = "asst_mCUOQgJSBMtJjNQdCjcQxkxJ"

# Create the chate interface
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

# Prepare the payload for the API request
    payload = {
        "assistant_id": assistant_id,
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    }

    # Headers for the API request
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }

    # Make the request to the custom assistant API
    response = requests.post(f"https://api.openai.com/v1/assistants/{assistant_id}/completions", json=payload, headers=headers)

    if response.status_code == 200:
        response_data = response.json()
        assistant_response = response_data["choices"][0]["message"]["content"]
    else:
        assistant_response = f"Sorry, there was an error communicating with the assistant API. Status code: {response.status_code}. Response: {response.text}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

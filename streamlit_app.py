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

    # Prepare the payload for the initial run
    payload = {
        "assistant_id": assistant_id,
        "messages": [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    }

    # Headers for the API request
    headers = {
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}",
        "Content-Type": "application/json"
    }

    # Initialize the run
    run_response = requests.post(f"https://api.openai.com/v1/assistants/{assistant_id}/runs", json=payload, headers=headers)

    if run_response.status_code == 200:
        run_data = run_response.json()
        run_id = run_data["id"]

        # Poll the run status
        run_status = run_data["status"]
        while run_status in ["in_progress", "queued"]:
            run_status_response = requests.get(f"https://api.openai.com/v1/assistants/{assistant_id}/runs/{run_id}", headers=headers)
            run_status_data = run_status_response.json()
            run_status = run_status_data["status"]

        # Retrieve the run messages
        if run_status == "completed":
            messages_response = requests.get(f"https://api.openai.com/v1/assistants/{assistant_id}/runs/{run_id}/messages", headers=headers)
            if messages_response.status_code == 200:
                messages_data = messages_response.json()
                assistant_response = messages_data["messages"][-1]["content"]
            else:
                assistant_response = "Sorry, there was an error retrieving the messages."
        else:
            assistant_response = "Sorry, the run did not complete successfully."

    else:
        assistant_response = f"Sorry, there was an error initializing the run. Status code: {run_response.status_code}. Response: {run_response.text}"

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(assistant_response)

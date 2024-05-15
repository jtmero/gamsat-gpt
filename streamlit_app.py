import streamlit as st
import requests
import os
import time

# Set API key
api_key = st.secrets["OPENAI_API_KEY"]

# Create an OpenAI client with your API key
openai_client = openai.Client(api_key = api_key)
                              
# Retrieve the assistant you want to use
assistant = openai_client.beta.assistants.retrieve("asst_3no7SQcpD6vOpUHqMCL2cRUB")

# Create the title and subheader for the Streamlit page
st.title("GamsatGPT")
st.subheader("You can ask me to generate any kind of GAMSAT SIII question")

# Ask user for input
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

# Create a new thread with a message that has the uploaded file's ID
thread = openai_client.beta.threads.create(
    messages=[{"role": "user",
               "content": prompt}]
        )

# Create a run with the new thread
run = openai_client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# Check periodically whether the run is done, and update the status
while run.status != "completed":
    time.sleep(5)
    status_box.update(label=f"{run.status}...", state="running")
    run = openai_client.beta.threads.runs.retrieve(
        thread_id=thread.id, run_id=run.id)

# Once the run is complete, update the status box and show the content
status_box.update(label="Complete", state="complete", expanded=True)
messages = openai_client.beta.threads.messages.list(
    thread_id=thread.id)
st.markdown(messages.data[0].content[0].text.value)

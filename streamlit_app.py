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
prompt = st.chat_input("Enter your prompt here:")

if prompt:
    # Debug print statements
    print(f"Prompt: {prompt}")
    print(f"Assistant ID: {assistant_id}")

    # Display the user's question
    st.markdown(f"**You:** {prompt}")

    # Create a new thread with a message that has the uploaded file's ID
    thread = openai_client.beta.threads.create(
        messages=[{"role": "user", "content": prompt}]
    )

    # Print thread details for debugging
    print(f"Thread: {thread}")

    # Create a run with the new thread
    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,  # Ensure assistant_id is correctly defined
    )

    # Print run details for debugging
    print(f"Run: {run}")

    # Create a status box to update the run status
    status_box = st.empty()

    # Check periodically whether the run is done, and update the status
    while run.status != "completed":
        time.sleep(5)
        status_box.text(f"{run.status}...")
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )

    # Once the run is complete, update the status box and show the content
    status_box.text("Complete")
    messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
    
    # Print messages details for debugging
    print(f"Messages: {messages}")

    if messages.data:
        # Extract and clean the text content from the response
        response_content = messages.data[0].content.value
        st.markdown(f"**Assistant:** {response_content}")
    else:
        st.warning("No messages found in the thread.")

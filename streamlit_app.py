import streamlit as st
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
prompt = st.chat_input("Why don't you ask me to make you a question?")
if prompt:
    # Display the user's question
    with st.chat_message("user"):
        st.write(prompt)
        
    # Create a new thread
    thread = openai_client.beta.threads.create(
        messages=[{"role": "user", "content": prompt}]
    )

    # Stream a run
    with openai_client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
    ) as stream:
        with st.chat_message("assistant"):
            question = st.write_stream(stream.text_deltas)
            stream.until_done()

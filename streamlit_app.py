import streamlit as st
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
            st.write(stream.until_done())

    # Ask the user to give an answer
    answer = st.chat_input("What's your answer?")
    if answer:
    # Display the user's question
        with st.chat_message("user"):
            st.write(answer)
        
        # Add to the thread
        response_message = openai_client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=answer
        )

        # Continue streaming to get reasoning
        with openai_client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
        ) as stream:
            with st.chat_message("assistant"):
                st.write(stream.until_done())

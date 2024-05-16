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

# Initialize session state for managing the conversation
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'prompt' not in st.session_state:
    st.session_state.prompt = None
if 'answer' not in st.session_state:
    st.session_state.answer = None

# Create a chat input for the prompt
if st.session_state.prompt is None:
    st.session_state.prompt = st.chat_input("Why don't you ask me to make you a question?")
    if st.session_state.prompt:
        # Display the user's question
        with st.chat_message("user"):
            st.write(st.session_state.prompt)
        
        # Create a new thread
        thread = openai_client.beta.threads.create(
            messages=[{"role": "user", "content": st.session_state.prompt}]
        )
        st.session_state.thread_id = thread.id

        # Stream a run
        with openai_client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
        ) as stream:
            with st.chat_message("assistant"):
                question = st.write_stream(stream.text_deltas)
                stream.until_done()

# Ask the user to give an answer
if st.session_state.prompt and st.session_state.thread_id and st.session_state.answer is None:
    st.session_state.answer = st.chat_input("What's your answer?")
    if st.session_state.answer:
        # Display the user's answer
        with st.chat_message("user"):
            st.write(st.session_state.answer)
        
        # Add to the thread
        response_message = openai_client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=st.session_state.answer
        )

        # Continue streaming to get reasoning
        with openai_client.beta.threads.runs.stream(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant.id,
        ) as stream:
            with st.chat_message("assistant"):
                reasoning = st.write_stream(stream.text_deltas)
                stream.until_done()

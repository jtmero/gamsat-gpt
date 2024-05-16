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

# Initialize session state for managing the conversation
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'prompt' not in st.session_state:
    st.session_state.prompt = None
if 'answer' not in st.session_state:
    st.session_state.answer = None
if 'question_displayed' not in st.session_state:
    st.session_state.question_displayed = False
if 'awaiting_explanation' not in st.session_state:
    st.session_state.awaiting_explanation = False

# Step 1: Get the prompt from the user
if not st.session_state.question_displayed:
    prompt = st.chat_input("Why don't you ask me to make you a question?")
    if prompt:
        st.session_state.prompt = prompt
        
        # Display the user's question
        with st.chat_message("user"):
            st.write(st.session_state.prompt)
        
        # Create a new thread
        thread = openai_client.beta.threads.create(
            messages=[{"role": "user", "content": st.session_state.prompt}]
        )
        st.session_state.thread_id = thread.id

        # Stream a run to get the question
        with openai_client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
        ) as stream:
            with st.chat_message("assistant"):
                st.write_stream(stream.text_deltas)
                stream.until_done()
        
        st.session_state.question_displayed = True
        st.experimental_rerun()

# Step 2: Ask the user to give an answer
if st.session_state.question_displayed and not st.session_state.awaiting_explanation:
    answer = st.chat_input("What's your answer?")
    if answer:
        st.session_state.answer = answer
        with st.chat_message("user"):
            st.write(st.session_state.answer)
        
        # Add the answer to the thread
        response_message = openai_client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=st.session_state.answer
        )
        
        st.session_state.awaiting_explanation = True
        st.experimental_rerun()

# Step 3: Get the assistant's explanation
if st.session_state.awaiting_explanation:
    # Continue streaming to get the explanation
    with openai_client.beta.threads.runs.stream(
        thread_id=st.session_state.thread_id,
        assistant_id=assistant.id,
    ) as stream:
        with st.chat_message("assistant"):
            st.write_stream(stream.text_deltas)
            stream.until_done()

    # Reset state for next interaction
    st.session_state.thread_id = None
    st.session_state.prompt = None
    st.session_state.answer = None
    st.session_state.question_displayed = False
    st.session_state.awaiting_explanation = False
    st.experimental_rerun()

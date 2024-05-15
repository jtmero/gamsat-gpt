import streamlit as st
import openai
import time

# Set API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

# Create an OpenAI client with your API key
openai_client = openai.Client(api_key=api_key)

# Retrieve the assistant you want to use
assistant = openai_client.beta.assistants.retrieve("asst_3no7SQcpD6vOpUHqMCL2cRUB")
assistant_id = assistant.id  # Extract assistant ID

# Initialize session state
if 'thread_id' not in st.session_state:
    st.session_state.thread_id = None
if 'run_id' not in st.session_state:
    st.session_state.run_id = None
if 'feedback_run_id' not in st.session_state:
    st.session_state.feedback_run_id = None
if 'question_generated' not in st.session_state:
    st.session_state.question_generated = False
if 'user_answer_submitted' not in st.session_state:
    st.session_state.user_answer_submitted = False

# Create the title and subheader for the Streamlit page
st.title("GamsatGPT")
st.subheader("You can ask me to generate any kind of GAMSAT SIII question")

if not st.session_state.question_generated:
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
        st.session_state.thread_id = thread.id

        # Create a run with the new thread
        run = openai_client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )
        st.session_state.run_id = run.id

        # Check periodically whether the run is done, and update the status
        while run.status != "completed":
            time.sleep(5)
            run = openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )

        # When the run is complete, retrieve the messages
        if run.status == "completed":
            messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
            # Extract just the response from the message data
            response = messages.data[0].content[0].text.value

            with st.chat_message("assistant"):
                st.write(response)

            st.session_state.question_generated = True

if st.session_state.question_generated and not st.session_state.user_answer_submitted:
    # Ask the user for their answer
    user_answer = st.chat_input("What is your answer?")

    if user_answer:
        with st.chat_message("user"):
            st.write(user_answer)

        # Add user's answer to the thread
        response_message = openai_client.beta.threads.messages.create(
            thread_id=st.session_state.thread_id,
            role="user",
            content=user_answer
        )

        # Create another run to get the assistant's feedback
        feedback_run = openai_client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant_id,
        )
        st.session_state.feedback_run_id = feedback_run.id

        # Check periodically whether the feedback run is done
        while feedback_run.status != "completed":
            time.sleep(5)
            feedback_run = openai_client.beta.threads.runs.retrieve(
                thread_id=st.session_state.thread_id, run_id=feedback_run.id
            )

        # When the feedback run is complete, retrieve the feedback messages
        if feedback_run.status == "completed":
            feedback_messages = openai_client.beta.threads.messages.list(
                thread_id=st.session_state.thread_id)
            # Extract the assistant's feedback from the message data
            feedback_response = feedback_messages.data[-1].content[0].text.value

            with st.chat_message("assistant"):
                st.write(feedback_response)

            st.session_state.user_answer_submitted = True

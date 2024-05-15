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
prompt = st.chat_input("Why don't you ask me to make you a question?")

if prompt:
    # Display the user's question
    with st.chat_message("user"):
        st.write(prompt)

    # Create a new thread
    thread = openai_client.beta.threads.create(
        messages=[{"role": "user", "content": prompt}]
    )

    # Create a run with the new thread
    run = openai_client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id,
    )

    # Check periodically whether the run is done, and update the status
    while run.status != "completed":
        time.sleep(5)
        run = openai_client.beta.threads.runs.retrieve(
            thread_id=thread.id, run_id=run.id
        )

    # When the run is complete, retrieve the messages
    if run.status == "completed":
        messages = openai_client.beta.threads.messages.list(
            thread_id=thread.id
        )
        # Extract just the response from the message data
        response = messages.data[0].content[0].text.value
        
        with st.chat_message("assistant"):
            st.write(response)

        # Ask the user for their answer
        user_answer = st.chat_input("What is your answer?")

        if user_answer:
            with st.chat_message("user"):
                st.write(user_answer)

            # Add user's answer to the thread
            response_message = openai_client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_answer
            )

            # Create another run to get the assistant's feedback
            feedback_run = openai_client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )

            # Check periodically whether the feedback run is done
            while feedback_run.status != "completed":
                time.sleep(5)
                feedback_run = openai_client.beta.threads.runs.retrieve(
                    thread_id=thread.id, run_id=feedback_run.id
                )

            # When the feedback run is complete, retrieve the feedback messages
            if feedback_run.status == "completed":
                feedback_messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
                # Extract the assistant's feedback from the message data
                feedback_response = feedback_messages.data[-1].content[0].text.value
                
                with st.chat_message("assistant"):
                    st.write(feedback_response)


import streamlit as st
import openai

# Set the OpenAI API key from Streamlit secrets
api_key = st.secrets["openai_api_key"]

# Create an OpenAI client with your API key
openai_client = openai.Client(api_key=api_key)

# Retrieve the custom assistant ID
assistant_id = "asst_3no7sqcpd6vopuhqmcl2crub"

# Create the title and subheader for the Streamlit page
st.title("gamsatgpt")
st.subheader("You can ask me to generate any kind of GAMSAT Section III question")

# Create a chat input for the user to start the conversation
user_message = st.empty()
user_input = st.text_input("Type 'make me a question' to get started:")

if user_input == "make me a question":
    user_message.write(user_input)

    # Collect the user's answer using the same chat_input widget
    user_answer = st.text_input("Enter your answer:")

    with st.form(key='answer_form'):
        submit_button = st.form_submit_button(label='Submit')

        if submit_button and user_answer:
            with st.empty():
                st.write(f"Your answer: {user_answer}")

            # Create a new thread
            thread = openai_client.ChatCompletion.create(
                assistant_id=assistant_id,
                messages=[
                    {"role": "user", "content": user_answer},
                    {"role": "assistant"},
                ],
            )

            # Run the thread to receive the assistant's response
            openai_client.ThreadCompletion.create(thread=thread.id)

            # Display the response from the OpenAI assistant
            for message in thread.messages:
                if message.role == "assistant":
                    st.write("Assistant's response:")
                    st.write(message.content)

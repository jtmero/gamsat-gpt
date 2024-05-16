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

# Create a chat input for the user to start the conversation
user_message = st.empty()
user_chat = st.chat_input("You can type 'make me a question' to get started:")
if user_chat:
    user_message.write(user_chat)

    with st.form(key='answer_form'):
        user_answer = st.text_input("Enter your answer:")
        submit_button = st.form_submit_button(label='Submit')

        if submit_button:
            with st.empty():
                st.write(f"Your answer: {user_answer}")

            # Create a new thread
            thread = openai_client.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": user_answer},
                          {"role": "assistant", "content": "That's an interesting answer."}],
                assistant_id=assistant_id
            )

            # Run the thread
            openai_client.ThreadCompletion.create(thread=thread.id)

            # Stream the responses from the OpenAI assistant
            for message in thread.messages:
                if message.role == "assistant":
                    st.chat_message(value=message.content, from_user=False)

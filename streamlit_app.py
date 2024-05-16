from openai import OpenAI
import streamlit as st

# Set up the chat
st.title("GamsatGPT")
intro = "Welcome to GamsatGPT. You can ask me to generate any kind of GAMSAT SIII question"

# Load the OpenAi client and assistant
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
assistant = client.beta.assistants.retrieve("asst_3no7SQcpD6vOpUHqMCL2cRUB")

# Initialize the session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "assistant", "content": intro})

# Display the previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Enter new messages to chat from the user
if prompt := st.chat_input("Enter your reply"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Create a thread
    thread = client.beta.threads.create()
    
    # Append the prompt to the thread as a message
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt)
    
    # Custom event handler to collect the assistant's reply
    class SimpleEventHandler:
        def __init__(self):
            self.messages = []

        def handle_event(self, event):
            if 'choices' in event and event['choices'][0]['delta'].get('content'):
                self.messages.append(event['choices'][0]['delta']['content'])

    # Create an instance of the custom event handler
    event_handler = SimpleEventHandler()
    
    # Generate the assistant reply
    with st.chat_message("assistant"):
        with client.beta.threads.runs.stream(
            thread_id=thread.id,
            assistant_id=assistant.id,
            event_handler=event_handler,
        ) as stream:
            stream.until_done()

        # Collect the response from the messages
        response = "".join(event_handler.messages)

        # Write the response to the Streamlit chat
        st.markdown(response)

    # Append the assistant's message to the session state messages
    st.session_state.messages.append({"role": "assistant", "content": response})

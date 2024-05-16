import streamlit as st
from openai import OpenAI
import re

# Set up the chat
st.title("GamsatGPT")
intro = "Welcome to GamsatGPT. You can ask me to generate any kind of GAMSAT SIII question"

# Load the OpenAi client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Retrieve the assistant
assistant = client.beta.assistants.retrieve("asst_3no7SQcpD6vOpUHqMCL2cRUB")

text = """
( k ) is the rate constant,
( A ) is the pre-exponential factor,
( E_a ) is the activation energy,
( R ) is the universal gas constant ((8.314 , \text{J/mol·K})),
( T ) is the temperature in Kelvin.
Consider a reaction with an activation energy ( E_a ) of ( 50 , \text{kJ/mol} ) and a pre-exponential factor ( A ) of ( 1.2 \times 10^{13} , \text{s}^{-1} ).

Question:
Calculate the rate constant ( k ) at a temperature of ( 300 , \text{K} ).

Options:
A) ( 1.2 \times 10^{-4} , \text{s}^{-1} )
B) ( 3.5 \times 10^{-5} , \text{s}^{-1} )
C) ( 2.5 \times 10^{-6} , \text{s}^{-1} )
"""

# Initialize session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": intro}]
if "thread_id" not in st.session_state:
    thread = client.beta.threads.create()
    st.session_state.thread_id = thread.id

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your reply"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Append the prompt to the existing thread
    client.beta.threads.messages.create(
        thread_id=st.session_state.thread_id,
        role="user",
        content=prompt)

    # Generate and display the assistant reply
    with st.spinner('Generating response...'):
        stream = client.beta.threads.runs.create(
            thread_id=st.session_state.thread_id,
            assistant_id=assistant.id,
            stream=True
        )

        # Loop through the streamed events to find the completed message
        for event in stream:
            if event.event == "thread.message.completed":
                response = event.data.content

                # Loop through the elements to find the text type response
                for block in response:
                    if block.type == 'text':
                        # Extract the text from the `value` field
                        text_content = block.text.value

                        # Replace "(" or ")" surrounded by any amount of whitespace with "$"
                        text_content = re.sub(r'\s+\)', '$', text)
                        text_content = re.sub(r'\(\s+', '$', text_content)
                        
                        # Display this text in Streamlit
                        st.markdown(text_content)
                        
                        # Append this to session state
                        st.session_state.messages.append({"role": "assistant", "content": text_content})

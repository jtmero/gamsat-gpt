from openai import OpenAI
import streamlit as st

# Load the model
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])
assistant_id = "asst_mCUOQgJSBMtJjNQdCjcQxkxJ"

# Create the chate interface
st.title("GamsatGPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Why don't you ask me to generate you a question?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

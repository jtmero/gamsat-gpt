from openai import OpenAI
import streamlit as st
import os

# Get the API key from environment variable
api_key = os.getenv('API_KEY')

# Create the title
st.title("GamsatGPT")

# Load the model
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

prompt = st.chat_input("Ask me to make you a question")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

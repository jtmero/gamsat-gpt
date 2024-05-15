from openai import OpenAI
import streamlit as st

# Get the API key from environment variable
api_key = os.getenv('API_KEY')

# Create the title
st.title("GamsatGPT")

# Load the model
client = OpenAI(api_key = st.secrets["OPENAI_API_KEY"])

prompt = st.chat_input("Why don't you ask me to make you a question?")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

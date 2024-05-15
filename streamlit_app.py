from openai import OpenAI
import streamlit as st

st.title("GamsatGPT")

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

with st.chat_message("user"):
    st.write("Hello 👋")

import streamlit as st
import vertexai
from vertexai.preview.language_models import TextGenerationModel
import os

# Set up the chat
st.title("GamsatGPT (Powered by Gemini)")
st.subheader("Ask me to make you a question!")

# Load the environment variables 
project_id = os.environ["PROJECT_ID"]
location = os.environ["LOCATION"]  

# Initialize Vertex AI 
vertexai.init(project=project_id, location=location)

# Initialize the Gemini Pro 1.5 Flash Model with a system prompt.
model = TextGenerationModel.from_pretrained("models/gemini-1.5-flash-001",
    system_instruction="You are a helpful assistant that makes gamstat style questions")

# Configuration for text generation
generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

# Safety settings to filter out harmful content
safety_settings = {
    vertexai.preview.language_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: vertexai.preview.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    vertexai.preview.language_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: vertexai.preview.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    vertexai.preview.language_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: vertexai.preview.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    vertexai.preview.language_models.HarmCategory.HARM_CATEGORY_HARASSMENT: vertexai.preview.language_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = 1 

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Enter your reply"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # Generate and display the Gemini Pro reply
        with st.spinner('Generating response...'):
            responses = model.generate_text(
                prompt=prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True,
            )

            for response in responses:
                with st.chat_message("assistant"):
                    st.markdown(response.text, end="") 
    except Exception as e:  
        st.error(f"An error occurred: {e}")

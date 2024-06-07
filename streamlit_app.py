import streamlit as st
from google.api_core import client_options as client_options_lib
from google.cloud.aiplatform_v1beta1.services.prediction_service import PredictionServiceClient
from google.cloud.aiplatform_v1beta1.types import prediction_service
import os

# Set up the chat
st.title("GamsatGPT")
st.subheader("Ask me to make you a question!")

# Load environment variables (you'll need to set these for Gemini Pro)
project_id = os.environ["PROJECT_ID"]
endpoint_id = os.environ["ENDPOINT_ID"]
location = os.environ["LOCATION"]  

# Initialize Gemini Pro client (through Vertex AI)
client_options = client_options_lib.ClientOptions(
    api_endpoint=f"{location}-aiplatform.googleapis.com"
)
client = PredictionServiceClient(client_options=client_options)


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

    # Prepare request for Gemini Pro (adapt parameters as needed)
    instance = prediction_service.PredictRequest(
        endpoint=client.endpoint_path(project_id, location, endpoint_id),
        instances=[{"prompt": prompt}]  
    )

    # Generate and display the Gemini Pro reply
    with st.spinner('Generating response...'):
        response = client.predict(request=instance)

        # Extract and process text content from Gemini's response
        # (Adapt this part based on your actual Gemini Pro response structure)
        # Assuming Gemini Pro returns text in a 'text' field within 'predictions'
        text_content = response.predictions[0]['content'] 

        st.session_state.messages.append({"role": "assistant", "content": text_content})

        # Simulate streaming behavior (optional)
        for chunk in text_content.split(" "):  
            with st.chat_message("assistant"):
                st.markdown(chunk + " ")  # Add a space after each chunk

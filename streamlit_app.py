import streamlit as st
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests

# Load the model and tokenizer in a Streamlit cached function

# Show title and description
st.title("💬 Hugging Face Story Generator")
st.write(
    "This chatbot generates engaging stories based on your input using a custom-trained Hugging Face model."
)


# Create a session state variable to store the chat messages
prompt = st.text_input("Enter your prompt:")

# Define the options for the dropdown
options = ["Option 1", "Option 2", "Option 3", "Option 4"]

# Create the dropdown menu
selected_option = st.selectbox("Choose an option:", options)

# Display the selected option
st.write(f"You selected: {selected_option}")

if st.button("Generate Story"):
    if prompt:
        api_url = "https://8083-34-80-6-234.ngrok-free.app/generate/"  # Replace with your ngrok URL
        response = requests.post(api_url, json={"prompt": prompt})
        st.write(response.json()["generated_text"])
    else:
        st.write("Please enter a prompt.")

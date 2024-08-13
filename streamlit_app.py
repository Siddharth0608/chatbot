import streamlit as st
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer in a Streamlit cached function

# Show title and description
st.title("💬 Hugging Face Story Generator")
st.write(
    "This chatbot generates engaging stories based on your input using a custom-trained Hugging Face model."
)


# Create a session state variable to store the chat messages
prompt = st.text_input("Enter your prompt:")

if st.button("Generate Story"):
    if prompt:
        api_url = "http://your_ngrok_url.ngrok.io/generate/"  # Replace with your ngrok URL
        response = requests.post(api_url, json={"prompt": prompt})
        st.write(response.json()["generated_text"])
    else:
        st.write("Please enter a prompt.")

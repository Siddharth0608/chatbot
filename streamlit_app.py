import streamlit as st
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import requests
import re
# Load the model and tokenizer in a Streamlit cached function

# Show title and description
st.title("💬 Story Generator 1.0")
st.write(
    "This Large Language Model generates engaging stories based on your input using Fine-Tuned Dolphin 2  model.")
st.write("The model is currently in the testing phase and may behave unpredictably at times.")
st.write("The main reason behind this test is to understand the relationship between the training data and the model's output."
)


# Create a session state variable to store the chat messages
prompt = st.text_input("Enter your prompt:")

# Define the options for the dropdown
options = ["Romance", "Action", "Adventure", "Fantasy", "Humor", "Erotica", "Crime", "Comics", "Horror", "Paranomal", "Inspirational", "Children", "Historical", "Poetry", "Drama", "Science Fiction", "Scripts-Screenplays", "Thirller-Mystery"]

# Create the dropdown menu
selected_option = st.selectbox("Choose a Genre:", options)

# Display the selected option
prompt = prompt + " " + f"<genre>{selected_option}</genre>"


if st.button("Generate Story"):
    if prompt:
        api_url = "https://e683-34-34-65-55.ngrok-free.app/generate/"  # Replace with your ngrok URL
        response = requests.post(api_url, json={"prompt": prompt})
        match = re.search(r"(?:assistant\s+.*?){2}(.*)", response.json()["generated_text"], re.DOTALL)
        assistant_output = match.group(1).strip()
        st.write(assistant_output)
        
    else:
        st.write("Please enter a prompt.")

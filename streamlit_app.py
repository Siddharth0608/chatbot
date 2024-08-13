import streamlit as st
import torch
from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load the model and tokenizer in a Streamlit cached function
@st.cache_resource
def load_model():
    access_token = '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'  # Replace with your Hugging Face access token
    peft_model_id = "sid0608/Story-Telling-Platform-1.0"
    config = PeftConfig.from_pretrained(peft_model_id, token=access_token)
    model = AutoModelForCausalLM.from_pretrained(config.base_model_name_or_path, return_dict=True, device_map='auto')
    tokenizer = AutoTokenizer.from_pretrained(config.base_model_name_or_path)
    
    # Add custom tokens
    custom_tokens = ['<title>', '</title>', '<b>', '</b>', '<chapter>', '</chapter>', '<genre>', '</genre>']
    tokenizer.add_tokens(custom_tokens, special_tokens=True)
    model.resize_token_embeddings(len(tokenizer))
    
    # Load the PEFT model
    model = PeftModel.from_pretrained(model, peft_model_id, token = access_token, offload_folder = 'offload')
    
    return model, tokenizer

model, tokenizer = load_model()

# Show title and description
st.title("💬 Hugging Face Story Generator")
st.write(
    "This chatbot generates engaging stories based on your input using a custom-trained Hugging Face model."
)

# Create a session state variable to store the chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Create a chat input field
if prompt := st.chat_input("What is up?"):

    # Store and display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a response using the Hugging Face model
    conversation = [
        {"role": "system", "content": "You are a creative and helpful assistant trained to generate engaging stories. Your task is to create well-structured stories based on the user's input."},
        {"role": "user", "content": prompt}
    ]
    
    batch = tokenizer.apply_chat_template(conversation, tokenize=False, add_generation_prompt=True)
    batch = tokenizer(batch, return_tensors='pt')

    with torch.cuda.amp.autocast():
        output_tokens = model.generate(**batch, max_new_tokens=1000)

    response = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

    # Store and display the assistant's response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

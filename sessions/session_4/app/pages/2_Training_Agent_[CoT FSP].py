import streamlit as st
import prompts
import re
from openai import OpenAI
from base_model_utils import call_chat_model, call_image_model

client = OpenAI()

st.set_page_config(layout="wide")

# Header
title = "myfitnessagent"
logo_path = "../../../logo.png"

col1, col2 = st.columns([1, 10])

with col1:
    st.image(logo_path, width=100)

# Display the title in the second column
with col2:
    st.title(title)



if (st.session_state.get("password_correct") == None) or (st.session_state.get("password_correct") == False):
    st.write("Please login first.")
    st.stop()


# Initialize internal and external chat history
if "internal_messages" not in st.session_state:
    st.session_state.internal_messages = [{
    "role":"system", 
    "content": prompts.system_prompt
}]

if "external_messages" not in st.session_state:
    st.session_state.external_messages = []

# Initialize trackers
if "nutrition_tracker" not in st.session_state:
    st.session_state.nutrition_tracker = ""
if "training_tracker" not in st.session_state:
    st.session_state.training_tracker = ""

# Function to extract tracker tags from response
def parse_messages(text):
    message_pattern = r"<message>(.*?)</message>"
    nutrition_pattern = r"<nutrition_plan>(.*?)</nutrition_plan>"
    training_pattern = r"<training_plan>(.*?)</training_plan>"

    message = re.findall(message_pattern, text, re.DOTALL)
    nutrition = re.findall(nutrition_pattern, text, re.DOTALL)
    training = re.findall(training_pattern, text, re.DOTALL)

    return message[0] if message else "", nutrition[0] if nutrition else "", training[0] if training else ""

# Create two columns
col1, col2 = st.columns([1,1])

with col1:
    st.header("Chat with coach")

    # Create a container for chat messages
    chat_container = st.container(height=400)
    
    # Create a container for the input box
    input_container = st.container()

    # Display chat messages from history on app rerun
    with chat_container:
        for message in st.session_state.external_messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Accept user input
    with input_container:
        upload_col1, upload_col2 = st.columns([4,1])

        with upload_col1:
            # image upload and processing
            uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"], label_visibility="collapsed")

            if uploaded_file is not None:
                with upload_col2:
                    if st.button("Process Image"):
                        st.write('Processing image...')
                        st.session_state.internal_messages.append({"role": "user", "content": "Uploaded a photo of food"})
                        st.session_state.external_messages.append({"role": "user", "content": "Uploaded a photo of food"})
                        
                        message, nutrition_tracker = call_image_model(client, uploaded_file)

                        if nutrition_tracker:
                                st.session_state.nutrition_tracker = nutrition_tracker
                        
                        st.session_state.internal_messages.append({"role": "assistant", "content": message})
                        st.session_state.external_messages.append({"role": "assistant", "content": message})

                        st.rerun()

        
        if prompt := st.chat_input("Enter text..."):
            # Add user message to chat history
            st.session_state.internal_messages.append({"role": "user", "content": prompt})
            st.session_state.external_messages.append({"role": "user", "content": prompt})

            with chat_container:
                # Display user message in chat message container
                with st.chat_message("user"):
                    st.markdown(prompt)

            # with chat_container:
                with st.chat_message("assistant"):
                    messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.internal_messages]
                    
                    completion = call_chat_model(client, messages)
                    
                    response = completion.choices[0].message.content

                    print('***RAW OUTPUTS***')
                    print(response)
                    
                    st.session_state.internal_messages.append({"role": "assistant", "content": response})

                    message, nutrition_tracker, training_tracker = parse_messages(response)

                    st.session_state.external_messages.append({"role": "assistant", "content": message})
                    
                    # Update session state trackers
                    if nutrition_tracker:
                        st.session_state.nutrition_tracker = nutrition_tracker
                    if training_tracker:
                        st.session_state.training_tracker = training_tracker
                    st.rerun()

with col2:
    st.header("Training and Nutrition Log")
    training_log_container = st.container(height=260)
    with training_log_container:
        st.write("### Training Plan")
        if len(st.session_state.training_tracker) > 0:
            st.write(st.session_state.training_tracker)

    nutrition_log_container = st.container(height=260)
    with nutrition_log_container:
        st.write("### Nutrition Plan")
        if len(st.session_state.nutrition_tracker) > 0:
            st.write(st.session_state.nutrition_tracker)


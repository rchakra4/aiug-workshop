import streamlit as st
import requests

st.set_page_config(layout="wide")

# Header
title = "myfitnessagent"
logo_path = "../../../logo.png"

if "nutrition_response" not in st.session_state:
    st.session_state.nutrition_response = ""

col1, col2 = st.columns([1, 10])

with col1:
    st.image(logo_path, width=100)

# Display the title in the second column
with col2:
    st.title(title)



if (st.session_state.get("password_correct") == None) or (st.session_state.get("password_correct") == False):
    st.write("Please login first.")
    st.stop()


st.subheader("Let me help you find specific meal options based on your diet (e.g., Mediterranean, Keto, Vegan, etc.)!")
user_input = st.text_input(label="nutrition_agent", label_visibility="hidden", placeholder="What are some Mediterranean breakfast options?")

# button to submit request
if st.button("Request nutrition options"):
    with st.spinner(f'Retrieving...'):
        data = requests.post("http://127.0.0.1:8000/nutrition").json()
        st.session_state.nutrition_response = data["response"]
    
st.write(st.session_state.nutrition_response)

import streamlit as st
import base64
import re

def call_chat_model(client, messages):
    return client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=1,
        max_tokens=4096
    )

def call_image_model(client, file):
    
    # Read the file-like object (uploaded_file)
    image_data = file.read()
    # Encode the file data in base64
    base64_image = base64.b64encode(image_data).decode('utf-8')

    # Create API request
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""You are given an image of the user's food.
                         This is their nutrition plan: <nutrition_plan>{st.session_state.nutrition_tracker}</nutrition_plan).
                         Figure out what kind of food is in the image (and its nutrition facts) and adjust the user's nutrition plan to include the food items in the image.
                         Respond back to the user using <message></message> tags briefly explaining to them how you changed their nutrition plan based on the image they uploaded.
                          Also provide the updated nutrition plan using <nutrition_plan></nutrition_plan> tags.""",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    }
                ],
            }
        ],
        max_tokens=4096,
    )

    # Parse the response content
    content = response.choices[0].message.content

    # Use regex to extract tags
    message_pattern = r"<message>(.*?)</message>"
    nutrition_pattern = r"<nutrition_plan>(.*?)</nutrition_plan>"
    message = re.findall(message_pattern, content, re.DOTALL)
    nutrition = re.findall(nutrition_pattern, content, re.DOTALL)

    return message[0] if message else "", nutrition[0] if nutrition else ""
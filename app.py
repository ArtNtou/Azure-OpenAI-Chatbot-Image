# streamlit run app.py
import os
import streamlit as st

from io import BytesIO
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image

from image_functions import initialize_chat, new_question_to_chat

with st.sidebar:
    st.title("🎉 Image Chatbot! 💬")
    st.markdown('''
    - Upload images, get enchanting descriptions, and insightful answers.
    - It is used gpt-4 with vision of Azure OpenAI
    - Provide an Image
    - Ask something about the image and then continue chatting if you feel so
    - ⏳ Please be patient; complex questions may take a moment to answer
    - 🚀 Set Sail on the Chatbot Adventure
    - [GPT-4 Vision - Azure](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/gpt-with-vision)
    - [Streamlit](https://streamlit.io/)'''
                )


def main():
    # Display app header
    st.header("Chat using an Image 🤖🖼️")

    # Placeholder for uploaded image_file
    image_file = None

    payload = None

    message = 0

    initial_text = None

    # when they add image this button will disappear
    if image_file is None:
        # Create a placeholder for the file uploader
        file_uploader_placeholder = st.empty()

        image_file = file_uploader_placeholder.file_uploader("Upload your Image", type=['png', 'jpg'],
                                                             accept_multiple_files=False)

    if initial_text is None:
        # create a placeholder to write text
        initial_text_placeholder = st.empty()

        # Write first question
        # initial_text = 'describe me this image'
        initial_text = initial_text_placeholder.text_input(
            "Enter first question or initial text about the image",
            label_visibility="visible",
            placeholder="Write text here",
            value=None
        )

    # it will not run until they provide an image
    if image_file is not None:

        file_uploader_placeholder.empty()

        if initial_text is not None:

            initial_text_placeholder.empty()

            # Read image file as BytesIO
            # with open('santaclaus.jpg', 'rb') as file:
            image_bytes = BytesIO(image_file.read())

            # Decode image using PIL
            img = Image.open(image_bytes)

            # Show uploaded image
            st.image(img, caption="Uploaded Image", use_column_width=True)

            # Initialize chat
            if message == 0 and initial_text is not None:

                # Initialize streamlit chat
                st.session_state.messages = [{"role": "user", "content": initial_text}]

                # Initialize chat and get response from model
                response, payload, headers = initialize_chat(image_bytes, initial_text)
                message += 1

                # Update chat history with assistant's response
                st.session_state.messages.append({"role": "assistant", "content": response})

            # Display existing chat history
            if message > 0:
                for msg in st.session_state.messages:
                    st.chat_message(msg["role"]).write(msg["content"])

            # Get user input
            if query := st.chat_input():

                # Write new message
                st.session_state.messages.append({"role": "user", "content": query})
                st.chat_message("user").write(query)

                # Get response from chat-gpt
                response, payload = new_question_to_chat(payload, query, headers)

                # Update chat history with assistant's response
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.chat_message("assistant").write(response)


if __name__ == '__main__':
    # Set the base directory for the app
    base_dir = Path(__file__).resolve().parent
    os.chdir(base_dir)
    load_dotenv(dotenv_path=r".env")

    # Run the main function
    main()

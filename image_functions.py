import os
import base64
import requests

# function in order to initialize chat, it will need an image and some text
def initialize_chat(image_bytes, starting_text):

    GPT4_KEY = os.environ.get('OPENAI_API_KEY')
    GPT4_ENDPOINT = os.environ.get('OPENAI_API_BASE')
    GPT4_NAME = os.environ.get('LLM4_NAME')
    GPT4_VERSION = os.environ.get('OPENAI_API_VERSION')

    headers = {
        "Content-Type": "application/json",
        "api-key": GPT4_KEY,
    }

    # Encode image as base64
    encoded_image = base64.b64encode(image_bytes.getvalue()).decode('ascii')

    # Payload for the request
    payload = {
        "messages": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "You are an AI assistant that helps people find information when they provide you a meaningful image"
                    }
                ]
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": starting_text
                    }
                ]
            },
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 800
    }

    GPT4V_ENDPOINT = f"{GPT4_ENDPOINT}openai/deployments/{GPT4_NAME}/chat/completions?api-version={GPT4_VERSION}"

    # Send request
    try:
        response = requests.post(GPT4V_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    return response, payload, headers


# ask for new information about the image
def new_question(payload, question, headers):

    GPT4_KEY = os.environ.get('LLM4_NAME')
    GPT4_ENDPOINT = os.environ.get('OPENAI_API_BASE')

    # Append user's message to the conversation
    user_message = {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": question
            }
        ]
    }
    payload["messages"].append(user_message)

    # Send another request with appended message
    try:
        response = requests.post(GPT4_ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    return response, payload
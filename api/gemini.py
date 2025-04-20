import requests
import json

from utils import load_env_vars
config = load_env_vars()

# The URL for the Gemini API (API_KEY should be set externally or passed as an argument)
API_KEY = config.GEMINI_API_KEY
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

def generate_content(model="gemini-1.5-flash", prompt="Explain how AI works"):
    """
    Sends a request to the Gemini API to generate content.

    Args:
        model: The name of the Gemini model to use (default: gemini-1.5-flash).
        prompt: The prompt to send to the model.

    Returns:
        The generated text, or None if an error occurs.
    """

    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(data))
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        try:
            response_json = response.json()  # Parse the JSON response
            generated_text = response_json['candidates'][0]['content']['parts'][0]['text']
            return generated_text  # Return the text

        except (KeyError, IndexError, TypeError) as e:  # Handle JSON structure errors
            print(f"Error extracting text from JSON: {e}")
            print(f"Response data: {response.text}") # Print the raw response for debugging
            return None  # Indicate failure

        except json.JSONDecodeError as e:  # Handle JSON decoding errors
            print(f"Invalid JSON response: {e}")
            print(f"Response text: {response.text}")  # Print the raw response for debugging
            return None

    except requests.exceptions.RequestException as e:  # Handle request errors
        print(f"Error communicating with Gemini API: {e}")
        if response.status_code != 200:
            print(f"Status Code: {response.status_code}")
        try:
            print(f"Response text: {response.text}")  # Print raw response if possible
        except:
            pass
        return None



# Example usage:
generated_text = generate_content(prompt="Que sabes de mi?")  # Or generate_content(prompt="Your prompt here")

if generated_text:
    print(generated_text)  # Now you can use the generated text
else:
    print("Failed to get a valid response from the Gemini API.")
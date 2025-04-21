import os, sys
import datetime
import logging
from dotenv import load_dotenv
from colorama import Fore, Style
import requests

def get_request(url: str, params: dict = None) -> None:
    try:
        response = requests.get(url, params=params)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print_with_format(f"Error: {response.status_code} - {response.text}", type="error")
            return None
    except requests.exceptions.RequestException as e:
        print_with_format(f"Request failed: {e}", type="error")
        return None
    
def post_request(url: str, data: dict = None) -> None:
    try:
        response = requests.post(url, json=data)
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print_with_format(f"Error: {response.status_code} - {response.text}", type="error")
            return None
    except requests.exceptions.RequestException as e:
        print_with_format(f"Request failed: {e}", type="error")
        return None


def print_with_format(text: str, type: str = "message") -> None:
    _print_formatted(text, type)
    if os.getenv("LOGGING_ENABLED") and os.getenv("LOGGING_ENABLED").lower() == "true":
        _log_message(text)

        
def _print_formatted(text: str, type: str = "message") -> None: # Función interna para imprimir
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    color = {
        "message": Fore.GREEN,
        "warning": Fore.YELLOW,
        "error": Fore.RED,
    }.get(type, Fore.RED)  # Color por defecto: rojo

    formatted_text = f"[{color}{date}{Style.RESET_ALL}] | {text}"
    print(formatted_text)


def _log_message(text: str) -> None: # Función interna para logging
    logging.info(text)     

def create_env_file(file_path=".env"):
    """Creates a .env file with environment variables."""
    try:
        variables = {
                "FRONTEND_PORT" : "8000",
                "API_URL" : "http://localhost:8000",
                "VERSION" : "2.0.1",
                }
        
        with open(file_path, "w") as f:
            for key, value in variables.items():
                f.write(f"{key}={value}\n")

        return True
    
    except Exception as e:
            return False

# Load environment variables
def load_env_vars():
    """Loads environment variables from .env file."""
    if not os.path.exists('.env'):
        print_with_format("[MAIN] The .env file does not exist. Creating...", type="error")
        if create_env_file():
            print_with_format("[MAIN] .env file created. Please fill it with the required variables.")
        else:
            print_with_format("[MAIN] Error creating .env file. Exiting...", type="error")
        sys.exit()
    else:
        print_with_format("[MAIN] The .env file exists. Loading variables...")
        load_dotenv()
        return Config()
    
    
class Config:

    def __init__(self):
        self.FRONTEND_PORT = os.environ.get('FRONTEND_PORT')
        self.API_URL = os.getenv("API_URL")          
        self.VERSION = os.getenv("VERSION")          
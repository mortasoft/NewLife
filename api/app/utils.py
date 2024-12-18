import sys,os,json
import datetime
from colorama import Fore,Style
import uuid
import hashlib
import logging
from dotenv import load_dotenv
load_dotenv()

class Response:
  def __init__(self, result, message, status_code):
    self.result = result
    self.message = message
    self.status_code = status_code


def read_config_file(dir):
    try:
        f = open(dir+"/config.json")
        data = json.load(f)
        print_with_format("[Utils.read_config_file] JSON Configuration file loaded successfully.")
        return data
    except Exception as e:
        print(f"[Utils.read_config_file] Error opening configuration file {e}")
        sys.exit()


def print_with_format(text, type="message"):
    """
    Prints a message with a specific format.
    type can be:
        - m: message
        - w: warning
        - e: error
    """
    
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if os.getenv("API_DEBUG") and os.getenv("API_DEBUG").lower() == "true":
        if type=="message":
            formatted_text = f"[{Fore.GREEN}{date}{Style.RESET_ALL}] | {text}"
        elif type=="warning":
            formatted_text = f"[{Fore.YELLOW}{date}{Style.RESET_ALL}] | {text}"
        elif type=="error":
            formatted_text = f"[{Fore.RED}{date}{Style.RESET_ALL}] | {text}"
        print(formatted_text)
    else:
        formatted_text = f"[{Fore.RED}{date}{Style.RESET_ALL}] | {text}"
        print(formatted_text)

    # Configure logging
    if os.getenv("LOGGING_ENABLED") and os.getenv("LOGGING_ENABLED").lower() == "true":
        logging.basicConfig(filename='app.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
        logging.info(formatted_text)  # Guarda el mensaje formateado en el log
    
        
def generate_uuid():
    """
    Generates a UUID.

    Returns:
        str: UUID generated.
    """
    return str(uuid.uuid4())


def generate_hash(text):
    """
    Generates a hash from a text.

    Args:
        text (str): Text to hash.

    Returns:
        str: Hash generated.
    """
    return hashlib.sha1(text.encode()).hexdigest()


def create_env_file(file_path=".env"):
    """Creates a .env file with environment variables."""
    try:
        variables = {
                "ENVIRONMENT_TYPE": "development", # development or production
                "API_DEBUG": "true", # true or false
                "API_HOST": "domain.com", # domain or IP 
                "API_PORT": "5000", # The default port is 5000
                "API_TITLE": "NewLife API",
                "API_FAVICON": "", # favicon.ico
                "DB_USER": "username",
                "DB_PASS": "password",
                "DB_HOST": "mydomain.com",
                "DB_PORT": "3306", # MySQL default port
                "DB_NAME": "newlife",    
                "DEV_DB_HOST": "localhost",
                "DEV_DB_USER": "username",
                "DEV_DB_PASS": "password",
                "DEV_DB_PORT": "3306",
                "DEV_DB_NAME": "newlife",
                "LOGGING_ENABLED": "True"
                }
        
        with open(file_path, "w") as f:
            for key, value in variables.items():
                f.write(f"{key}={value}\n")

        return True
    
    except Exception as e:
            return False



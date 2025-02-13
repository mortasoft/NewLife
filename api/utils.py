import sys,os,json
import datetime
from colorama import Fore,Style
import uuid
import hashlib
import logging
from apiflask.fields import String, Integer, Field
from apiflask import Schema
from typing import Dict, Any, Optional
from dotenv import load_dotenv
load_dotenv()

@staticmethod
def create_response(result: Dict[str, Any]) -> tuple[Dict[str, Any], int]:
    """Create a standardized response format."""
    return {
        'message': result['message'],
        'status_code': result['status_code'],
        'result': result['result'],
        'data': result['data']
    }, result['status_code']


class BaseResponse(Schema):
    result = String()
    message = String()
    status_code = Integer()
    data = Field()
    


def generate_message(obj: Optional[Any], type: str) -> str:
    if obj is None:
        messages = {
            "get": "Data retrieved successfully.",
            "error": "Error processing the request.",
            "id_not_found": "The data with the specified ID does not exist."
        }
        return messages.get(type, "Invalid operation.")
    else:
        messages = {
            "create": f"[{obj}] created successfully.",
            "update": f"[{obj}] updated successfully.",
            "delete": f"[{obj}] deleted successfully.",
            "get": f"[{obj}] retrieved successfully.",
            "error": f"Error processing the request for [{obj}]."
        }
        return messages.get(type, "Invalid operation.")

def read_config_file(dir):
    try:
        f = open(dir+"/config.json")
        data = json.load(f)
        print_with_format("[Utils.read_config_file] JSON Configuration file loaded successfully.")
        return data
    except Exception as e:
        print(f"[Utils.read_config_file] Error opening configuration file {e}")
        sys.exit()


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

def print_with_format(text: str, type: str = "message") -> None:
    _print_formatted(text, type)
    if os.getenv("LOGGING_ENABLED") and os.getenv("LOGGING_ENABLED").lower() == "true":
        _log_message(text)
    
        
def generate_uuid() -> str:
    """
    Generates a UUID.

    Returns:
        str: UUID generated.
    """
    return str(uuid.uuid4())


def generate_hash(text: str) -> str:
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


def get_db_config():
    """Returns database configuration based on environment type."""
    env_type = os.getenv("ENVIRONMENT_TYPE")
    print_with_format(f"[MAIN] Environment type: {env_type}")

    db_configs = {
        "development": {
            "DB_NAME": os.getenv("DB_HOST_DEV"),
            "DB_USER": os.getenv("DEV_DB_USER"),
            "DB_PASS": os.getenv("DEV_DB_PASS"),
            "DB_HOST": os.getenv("DEV_DB_HOST"),
            "DB_PORT": os.getenv("DEV_DB_PORT")
        },
        "production": {
            "DB_NAME": os.getenv("DB_NAME"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASS": os.getenv("DB_PASS"),
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": os.getenv("DB_PORT")
        }
    }

    try:
        return db_configs[env_type]
    except KeyError:
        print_with_format("[MAIN] Invalid environment type. Exiting...", type="error")
        sys.exit()
        

class Config:

    def __init__(self):
        self.SECRET_KEY = os.environ.get('SECRET_KEY')
        self.API_HOST = os.getenv("API_HOST")
        self.API_PORT = os.getenv("API_PORT")
        self.API_DEBUG = os.getenv("API_DEBUG")
        self.API_TITLE = os.getenv("API_TITLE")
        self.BASE_DIRECTORY = os.path.dirname(__file__)
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASS = os.getenv("DB_PASS")
        self.VERSION = os.getenv("VERSION")
        self.ENVIRONMENT_TYPE = os.getenv("ENVIRONMENT_TYPE")
        self.DEV_DB_HOST = os.getenv("DEV_DB_HOST")
        self.DEV_DB_USER = os.getenv("DEV_DB_USER")     
        self.DEV_DB_PASS = os.getenv("DEV_DB_PASS")
        self.DEV_DB_PORT = os.getenv("DEV_DB_PORT")
        self.DEV_DB_NAME = os.getenv("DB_HOST_DEV")
        
        if self.ENVIRONMENT_TYPE == "development":
            self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{self.DEV_DB_USER}:{self.DEV_DB_PASS}@{self.DEV_DB_HOST}:{self.DEV_DB_PORT}/{self.DEV_DB_NAME}"
        if self.ENVIRONMENT_TYPE == "production":
            self.SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        else: 
            print_with_format("[MAIN] Invalid environment type. Exiting...", type="error")
            sys.exit()
            
            
        
        

        
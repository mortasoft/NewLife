import sys
import json
import datetime
from colorama import Fore,Style
import uuid
import hashlib


def make_resp(message, data,status_code):
    return {'message': message, 'data': data,'status_code': status_code}


def read_config_file(dir):
    try:
        f = open(dir+"/config.json")
        data = json.load(f)
        print_with_format("[Utils.read_config_file] JSON Configuration file loaded successfully.")
        return data
    except Exception as e:
        print(f"[Utils.read_config_file] Error opening configuration file {e}")
        sys.exit()


def print_with_format(texto, debug=True):
    if debug:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{Fore.GREEN}{date}{Style.RESET_ALL}] | {texto}")
        

def print_with_format_error(texto, debug=True):
    if debug:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{Fore.RED}{date}{Style.RESET_ALL}] | {texto}")
        
        
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






import os,sys
import json
import datetime
from colorama import Fore,Style

def make_resp(message, data,status_code):
    return {'message': message, 'data': data,'status_code': status_code}


def read_config_file(dir):
    try:
        f = open(dir+"/config.json")
        data = json.load(f)
        print_with_format("JSON Configuration file loaded successfully.")
        return data
    except Exception as e:
        print(f"Error opening configuration file {e}")
        sys.exit()


def print_with_format(texto, debug=True):
    if debug:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{Fore.GREEN}{date}{Style.RESET_ALL}] | {texto}")
        

def print_with_format_error(texto, debug=True):
    if debug:
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{Fore.RED}{date}{Style.RESET_ALL}] | {texto}")
        
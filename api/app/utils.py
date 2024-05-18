import os
import json
import datetime
from colorama import Fore,Style

def make_resp(message, data,status_code):
    return {'message': message, 'data': data,'status_code': status_code}


def read_config_file(dir):
    try:
        f = open(dir+"/config.json")
        data = json.load(f)
        imprimir("Archivo de configuración cargado correctamente")
        #imprimir(json.dumps(data,indent=4,sort_keys=True))
        return data
    except Exception as e:
        print(e)
        exit()


def imprimir(texto, debug=True):
    if debug:
        date = datetime.datetime.now().strftime("%x %X")
        salida = f"[{Fore.GREEN}{date}{Style.RESET_ALL}] {texto}"
        print(salida)


def print_with_format(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{timestamp} | {text}")

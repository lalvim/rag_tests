import requests
import simplejson

import unicodedata
import re
import codecs 

import os
from dotenv import dotenv_values

def normalize(text):

    clean_text = text.encode('raw_unicode_escape').decode('unicode-escape')
    clean_text = unicodedata.normalize("NFKD", clean_text)
    clean_text = re.sub(r'<[^>]*>', '', clean_text)
    clean_text = re.sub(r'http[s]?://\S+', '', clean_text)
    clean_text = clean_text.replace("'", "\"")

    return clean_text


def do_request(url,data,headers):
    try:
        response = requests.post(url,json=data,headers=headers)
        print("Status code:", response.status_code)
        if response.status_code == 200:
            return response
        else:
            print("Request error:", response.status_code)
            return None
    except Exception as e:
        print("Error:", e)
        return None


if __name__ == '__main__':

    env_vars = dotenv_values(".env")
    
    token  = env_vars["PYTHIA_TOKEN"]
    uuid   = env_vars["PYTHIA_DIALOG_UUID"]
 
    print('Entre com a pergunta : ')
    data = {'query': normalize(input())}
    url = f"http://127.0.0.1:3333/api/chat/{uuid}/ask"
    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
    }
    response = do_request(url,data,headers)
    if response:
        caminho_arquivo = "dados.json"
        data = response.json()
        with open(caminho_arquivo, "w") as arquivo:
            simplejson.dump(data, arquivo)

        print("JSON salvo com sucesso em", caminho_arquivo)
    
    
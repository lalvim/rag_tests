import requests
import simplejson

import unicodedata
import re
import codecs 

def normalize(text):

    clean_text = text.encode('raw_unicode_escape').decode('unicode-escape')
    clean_text = unicodedata.normalize("NFKD", clean_text)
    clean_text = re.sub(r'<[^>]*>', '', clean_text)
    clean_text = re.sub(r'http[s]?://\S+', '', clean_text)
    clean_text = clean_text.replace("'", "\"")

    return clean_text


def do_request(url,data):
    try:
        response = requests.post(url,json=data)
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

    print('Entre com a pergunta : ')
    data = {'query': normalize(input())}
    url = "http://127.0.0.1:3333/chat/api/bc00edf6-e3f7-4e61-b2b7-93119fa7e669/ask"
  
    response = do_request(url,data)
    if response:
        caminho_arquivo = "dados.json"
        data = response.json()
        with open(caminho_arquivo, "w") as arquivo:
            simplejson.dump(data, arquivo)

        print("JSON salvo com sucesso em", caminho_arquivo)
    
    
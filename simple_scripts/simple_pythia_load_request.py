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


if __name__ == '__main__':

    print('Entre com a pergunta : ')
    data = {'query': normalize(input())}
    url = "http://127.0.0.1:3333/chat/"
  
    response = requests.post(url,json=data)
    pattern = r"[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"

    match = re.search(pattern, response.url)
    if match:
        uuid = match.group(0)
        print("UUID encontrado:", uuid)
    else:
        print("Nenhum UUID encontrado na URL")    

    url = f'http://127.0.0.1:3333/chat/api/{uuid}/load'
    response = requests.get(url)
    if response:
        caminho_arquivo = "dados.json"
        data = response.json()
        with open(caminho_arquivo, "w") as arquivo:
            simplejson.dump(data, arquivo)

        print("JSON salvo com sucesso em", caminho_arquivo)
    
    
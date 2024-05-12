import requests
import simplejson

def json_parser(data):

    textos = []
    for item in data:
        print(item)
        """
        if 'webPageFragment' in item and item['webPageFragment'] and 'content' in item['webPageFragment']:
            textos.append(item['webPageFragment']['content'])
        if 'answer' in item:
            textos.append(item['answer'])
        if 'textFragment' in item and item['textFragment']:
            textos.append(item['textFragment'])
        """

    return textos    


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
    data = {'query': input()}
    url = "http://127.0.0.1:3333/chat/api/bc00edf6-e3f7-4e61-b2b7-93119fa7e669/ask"
  
    response = do_request(url,data)
    if response:
        caminho_arquivo = "dados.json"
        data = response.json()
        with open(caminho_arquivo, "w") as arquivo:
            simplejson.dump(data, arquivo)

        print("JSON salvo com sucesso em", caminho_arquivo)
        #question = response.json()[0]['text']
        #answer = response.json()[1]['text']
        #print(response.json())
        #print(json_parser(data))
        
        #json_str = simplejson.dumps(response.json(), indent=4, sort_keys=True)
        #print(json_str)

        #print(question)
        #print(answer)

    
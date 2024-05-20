import simplejson
import unicodedata

import re

def normalize(text):
    
    clean_text = re.sub(r'<[^>]*>', '', text)
    clean_text = unicodedata.normalize("NFKD", clean_text)
    clean_text = re.sub(r'http[s]?://\S+', '', clean_text)

    return clean_text


def json_parser(data):

    textos = {}
    chunks = []
    for item in data:
        if 'sources' in item:
            for source_dict in item['sources']: # lista com cada elemento um dict que tem id, questão
                s_id = int(source_dict['id'])
                textos[s_id] = {}
                if source_dict['question'] is not None:
                    textos[s_id]['answer'] = normalize(source_dict['question']['answer'])
                    textos[s_id]['title'] = normalize(source_dict['question']['title'])
                    #chunks.append(textos[s_id]['answer'])
                
                content = None
                if source_dict['webPageFragment'] is not None:    
                    content = normalize(source_dict['webPageFragment']['content'])
                    chunks.append(content)

                textos[s_id]['webpage_fragment'] = content
                content = None
                if source_dict['textFragment'] is not None:    
                    content = normalize(source_dict['textFragment']['content'])
                    chunks.append(content)
                    
                textos[s_id]['text_fragment'] = content

                
    return textos,chunks    


if __name__ == '__main__':

    caminho_arquivo = "dados.json"
    with open(caminho_arquivo, "r") as arquivo:
        json_data = simplejson.load(arquivo)

    json_parsed,chunks = json_parser(json_data)

    #json_str = simplejson.dumps(json_parsed, indent=4, sort_keys=True)
    #print(json_parsed)
    print(chunks)


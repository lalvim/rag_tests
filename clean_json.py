
import json

# Função para corrigir caracteres problemáticos durante o carregamento do JSON
def fix_json_object(obj):
    if isinstance(obj, str):
        return obj.encode('raw_unicode_escape').decode('unicode-escape')
    elif isinstance(obj, list):
        return [fix_json_object(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: fix_json_object(value) for key, value in obj.items()}
    else:
        return obj

# Carregando o JSON e corrigindo os caracteres problemáticos durante o carregamento
def load_fixed_json(input_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f, object_hook=fix_json_object)
    return data

# Caminho para o arquivo JSON de entrada e o arquivo de saída corrigido
input_file = input()

output_file = './synthetic_data/dados_corrigidos.json'

# Chamando a função para corrigir o JSON
fixed_data = load_fixed_json('./synthetic_data/'+input_file)

with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=4)



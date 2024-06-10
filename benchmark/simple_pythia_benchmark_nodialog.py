import sys
import os
import pytest
from dotenv import dotenv_values

from deepeval.test_case import LLMTestCase
from deepeval.metrics import ToxicityMetric, BiasMetric, FaithfulnessMetric, AnswerRelevancyMetric, ContextualRelevancyMetric, HallucinationMetric, ContextualPrecisionMetric, ContextualRecallMetric
from deepeval import evaluate
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset
from benchmark.json_pythia_parser import json_parser
import simplejson
import unicodedata
import re
import requests 
from tqdm import tqdm

def normalize(text):
    clean_text = text.encode('raw_unicode_escape').decode('unicode-escape')
    clean_text = unicodedata.normalize("NFKD", clean_text)
    clean_text = re.sub(r'<[^>]*>', '', clean_text)
    clean_text = re.sub(r'http[s]?://\S+', '', clean_text)
    clean_text = clean_text.replace("'", "\"")

    return clean_text

def get_text_of_answer_question(dictionaries):
    text = []
    for dictionary in dictionaries:
        if dictionary.get("type") == "ANSWER_QUESTION":
            return  dictionary.get("text"),dictionary.get("uuid")
    return None, None


MODEL   = "gpt-3.5-turbo"
#MODEL   = "gpt-4o"
TH = 0.5

if __name__=='__main__':

    input_filename = sys.argv[1]
    env_vars = dotenv_values(".env")
    
    os.environ["OPENAI_API_KEY"] = env_vars["OPENAI_API_KEY"]
    token  = env_vars["PYTHIA_TOKEN"]
    headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
    }
    create_url = 'http://127.0.0.1:3333/api/dialogs'

    dataset = EvaluationDataset()
    dataset.add_test_cases_from_json_file(
        file_path=f"./synthetic_data/{input_filename}",
        input_key_name="input",
        actual_output_key_name="actual_output",
        expected_output_key_name="expected_output",
        context_key_name="context",
        retrieval_context_key_name="retrieval_context",
    )
    
    for test_case in tqdm(dataset):
                
        response = requests.post(create_url,json=None,headers=headers)
        dialog_uuid = response.json()['uuid']
        
        parsed_input = normalize(test_case.input)
        if len(parsed_input) > 300:
           parsed_input = parsed_input[:300]
           print("out of limit") 
        
        llm_question = {'query': parsed_input}
        ask_url = f"http://127.0.0.1:3333/api/chat/{dialog_uuid}/ask"

        print(parsed_input)
        response = requests.post(ask_url,json=llm_question,headers=headers)
        #if response:
        answer = response.json()
        #print(answer)
        
        r,answer_uuid = get_text_of_answer_question(answer)
        if r:
            sources_url = f"http://127.0.0.1:3333/api/messages/{answer_uuid}/sources"
            src_response = requests.get(sources_url,headers=headers)
            #if src_response:
            sources = src_response.json()
            chunks = json_parser(sources)
        else:
            print("Exceção: resposta vazia")
            r = "Não tenho resposta para a pergunta."
            chunks = ["Sem contetxo."]
        test_case.actual_output = r
        test_case.retrieval_context = chunks

    c_relevancy = ContextualRelevancyMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True)

    a_relevancy = AnswerRelevancyMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True)

    h_metric = HallucinationMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True)

    f_metric = FaithfulnessMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True)

    c_precision = ContextualPrecisionMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True
    )

    c_recall = ContextualRecallMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True
    )
    """
    b_metric = BiasMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True 
    )

    t_metric = ToxicityMetric(
        threshold=TH,
        model=MODEL,
        include_reason=True 
    )
    """
    #x = evaluate(dataset.test_cases, [a_relevancy, c_relevancy, h_metric, f_metric, c_precision, c_recall])    
    x = evaluate(dataset.test_cases, [a_relevancy, h_metric, f_metric, c_relevancy, c_precision, c_recall ])    

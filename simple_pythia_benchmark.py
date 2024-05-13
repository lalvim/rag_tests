import os
import pytest
from dotenv import dotenv_values

from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, ContextualRelevancyMetric
from deepeval import evaluate
from deepeval import assert_test
from deepeval.dataset import EvaluationDataset
from simple_pythia_request import do_request
from json_pythia_parser import json_parser
import simplejson
import unicodedata
import re


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
            return  dictionary.get("text")
    return None

if __name__=='__main__':

    env_vars = dotenv_values(".env")
    url = "http://127.0.0.1:3333/chat/api/bc00edf6-e3f7-4e61-b2b7-93119fa7e669/ask"

    os.environ["OPENAI_API_KEY"] = env_vars["OPENAI_API_KEY"]
 
    dataset = EvaluationDataset()
    dataset.add_test_cases_from_json_file(
        file_path="./synthetic_data/dados_corrigidos.json",
        input_key_name="input",
        actual_output_key_name="actual_output",
        expected_output_key_name="expected_output",
        context_key_name="context",
        retrieval_context_key_name="retrieval_context",
    )
    
    for test_case in dataset:
        parsed_input = normalize(test_case.input)
        print(parsed_input)
        llm_question = {'query': parsed_input}
        response = do_request(url,llm_question)
        if response:
           data = response.json()
           r = get_text_of_answer_question(data)
           _,chunks = json_parser(data)
            
           test_case.actual_output = r
           test_case.retrieval_context = chunks
    
    c_relevancy = ContextualRelevancyMetric(
        threshold=0.7,
        model="gpt-3.5-turbo",
        include_reason=True)

    a_relevancy = AnswerRelevancyMetric(
        threshold=0.7,
        model="gpt-3.5-turbo",
        include_reason=True)


    x = evaluate(dataset.test_cases, [a_relevancy, c_relevancy])    

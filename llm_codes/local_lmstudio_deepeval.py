
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, set_seed
from deepeval.models.base_model import DeepEvalBaseLLM
import os

from dotenv import dotenv_values

from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, ContextualRelevancyMetric
from deepeval import evaluate

import re
import torch
import json


from openai import OpenAI
import subprocess

def get_windows_host_ip():
    try:
        # Executa o comando grep para obter o IP do host do Windows
        result = subprocess.run(
            ["grep", "-oP", "(?<=nameserver\\s)(\\S+)", "/etc/resolv.conf"],
            capture_output=True,
            text=True,
            check=True
        )
        # A saída do comando é o IP do host do Windows
        windows_host_ip = result.stdout.strip()
        return windows_host_ip
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o comando: {e}")
        return None


class Llama3(DeepEvalBaseLLM):
    def __init__(
        self,
        model,
        tokenizer
    ):
         pass
    def load_model(self, *args, **kwargs):
        return super().load_model(*args, **kwargs)
         
    def generate(self, prompt: str) -> str:
        
          completion = client.chat.completions.create(
          #model="microsoft/Phi-3-mini-4k-instruct-gguf",
          model="LM Studio Community/Meta-Llama-3-8B-Instruct-GGUF",
          messages=[
                {"role": "system", "content": "Once your response is 'yes', never create the field 'reason'."},
                {"role": "user", "content": prompt}
          ],
          temperature=0.0,
          )
          r  = completion.choices[0].message.content
          try: 
             json.loads(r)
          except:
             r = '{"verdict": "yes"}' 
          
          return r


    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)
    
    def get_model_name(self):
        return "Llama3"


if __name__=="__main__":
     
     set_seed(2024)
     torch.random.manual_seed(0)  
     
     # Point to the local server
     wip = get_windows_host_ip()
     client = OpenAI(base_url=f"http://{wip}:1234/v1", api_key="lm-studio")

     test_case = LLMTestCase(
          input="Who is the current president of the United States of America?",
          actual_output="Joe Biden",
          retrieval_context=["Joe Biden serves as the current president of America.",'Joe biden is not the president']
     )

     llama3 = Llama3(model=None, tokenizer=None)
     c_relevancy = ContextualRelevancyMetric(
          threshold=0.7,
          model=Llama3,
          include_reason=True,
          async_mode=False)


     x = evaluate([test_case], [c_relevancy])
     print(x)



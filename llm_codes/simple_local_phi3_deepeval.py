
from transformers import AutoModelForCausalLM, AutoTokenizer
from deepeval.models.base_model import DeepEvalBaseLLM

from dotenv import dotenv_values




class Phi3(DeepEvalBaseLLM):
    def __init__(
        self,
        model,
        tokenizer
    ):
        self.model = model
        self.tokenizer = tokenizer

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        model = self.load_model()

        device = "cuda" # the device to load the model onto
        
        inputs = tokenizer(prompt, return_tensors="pt").to(device)
        outputs = model.generate(**inputs, do_sample=True, max_new_tokens=120)
        response= tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    
        #model_inputs = self.tokenizer([prompt], return_tensors="pt").to(device)
        #model.to(device)

        #generated_ids = model.generate(**model_inputs, max_new_tokens=100, do_sample=True)
        #return self.tokenizer.batch_decode(generated_ids)[0]

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return "Phi3"

import os

current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, '..', '.env')
env_vars = dotenv_values(env_path)

access_token = env_vars["HUG_TOKEN"]

MODEL_PATH = "microsoft/Phi-3-mini-4k-instruct"
#MODEL_PATH = "mistralai/Mistral-7B-v0.1"


model = AutoModelForCausalLM.from_pretrained(MODEL_PATH,token=access_token)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH,token=access_token)

mistral_7b = Phi3(model=model, tokenizer=tokenizer)

print("Entre com a pergunta: ")
prompt = input()
prompt = f"<|user|>\n{prompt}<|end|>\n<|assistant|>"

print(mistral_7b.generate(prompt))

"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed
set_seed(2024)  

prompt = "Africa is an emerging economy because"

model_checkpoint = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint,
                                             trust_remote_code=True,
                                             torch_dtype="auto",
                                             device_map="cuda")

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, do_sample=True, max_new_tokens=120)
response= tokenizer.decode(outputs[0], skip_special_tokens=True)

print(response)

"""



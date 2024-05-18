
from transformers import AutoModelForCausalLM, AutoTokenizer
from deepeval.models.base_model import DeepEvalBaseLLM
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, set_seed
set_seed(2024)  

from dotenv import dotenv_values
import os
import time

current_dir = os.path.dirname(__file__)
env_path = os.path.join(current_dir, '..', '.env')
env_vars = dotenv_values(env_path)

access_token = env_vars["HUG_TOKEN"]

MODEL_PATH = "microsoft/Phi-3-mini-4k-instruct"
model_checkpoint = "microsoft/Phi-3-mini-4k-instruct"

tokenizer = AutoTokenizer.from_pretrained(model_checkpoint,trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_checkpoint,
                                             trust_remote_code=True,
                                             torch_dtype="auto",
                                             device_map="cuda")

prompt = " "
while len(prompt) > 0:

    prompt = input()
    prompt = f"<|user|>\n{prompt}<|end|>\n<|assistant|>"

    start_time = time.time()

    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(**inputs, do_sample=True, max_new_tokens=120)
    response= tokenizer.decode(outputs[0], skip_special_tokens=True)

    end_time = time.time()
    response_time = end_time - start_time
    
    print(response)
    print(f"Tempo de resposta: {response_time} segundos")
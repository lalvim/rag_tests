
from transformers import AutoModelForCausalLM, AutoTokenizer, set_seed
from deepeval.models.base_model import DeepEvalBaseLLM
import os

from dotenv import dotenv_values

from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, ContextualRelevancyMetric
from deepeval import evaluate


set_seed(2024)  


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

    def generate(self, prompt: str, device = "cuda") -> str:
        
        prompt = f"<|user|>\n{prompt}<|end|>\n<|assistant|>"

        model    = self.load_model()
        inputs   = tokenizer(prompt, return_tensors="pt").to(device)
        outputs  = model.generate(**inputs, do_sample=True, max_new_tokens=120)
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return response

    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)

    def get_model_name(self):
        return "Phi3"


if __name__=="__main__":


    current_dir = os.path.dirname(__file__)
    env_path = os.path.join(current_dir, '..', '.env')
    env_vars = dotenv_values(env_path)
    device = "cuda"

    access_token = env_vars["HUG_TOKEN"]

    MODEL_PATH = "microsoft/Phi-3-mini-4k-instruct"

    model = AutoModelForCausalLM.from_pretrained(MODEL_PATH,token=access_token,trust_remote_code=True,
                                                torch_dtype="auto",
                                                device_map=device)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH,token=access_token)

    phi3 = Phi3(model=model, tokenizer=tokenizer)


    

    test_case = LLMTestCase(
      input="Who is the current president of the United States of America?",
      actual_output="Joe Biden",
      retrieval_context=["Joe Biden serves as the current president of America.",'Joe biden is not the president']
    )

    c_relevancy = ContextualRelevancyMetric(
        threshold=0.7,
        model=phi3,
        include_reason=True)

    a_relevancy = AnswerRelevancyMetric(
        threshold=0.7,
        model=phi3,
        include_reason=True)


    x = evaluate([test_case], [a_relevancy, c_relevancy])
    print(x)




#    for i in [1,2]:
#        print("Entre com a pergunta: ")
#        prompt = input()
#        print(phi3.generate(prompt))



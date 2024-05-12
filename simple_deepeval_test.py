import os
import pytest
from dotenv import dotenv_values

from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric, AnswerRelevancyMetric, ContextualRelevancyMetric
from deepeval import evaluate
from deepeval import assert_test


if __name__=='__main__':
    

    env_vars = dotenv_values(".env")

    os.environ["OPENAI_API_KEY"] = env_vars["OPENAI_API_KEY"]

    test_case = LLMTestCase(
      input="Who is the current president of the United States of America?",
      actual_output="Joe Biden",
      retrieval_context=["Joe Biden serves as the current president of America.",'Joe biden is not the president']
    )


    c_relevancy = ContextualRelevancyMetric(
        threshold=0.7,
        model="gpt-4",
        include_reason=True)

    a_relevancy = AnswerRelevancyMetric(
        threshold=0.7,
        model="gpt-4",
        include_reason=True)


    x = evaluate([test_case], [a_relevancy, c_relevancy])
    print(x)


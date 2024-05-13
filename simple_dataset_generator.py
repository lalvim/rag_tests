from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import dotenv_values

from deepeval.synthesizer import Synthesizer
from deepeval.dataset import EvaluationDataset

import unicodedata
import re
import os

def normalize(text):
    
    return text.encode('raw_unicode_escape').decode('unicode-escape')
    
if __name__=='__main__':


    env_vars = dotenv_values(".env")

    db_host = env_vars["PG_HOST"]
    db_user = env_vars["PG_USER"]
    db_port = env_vars["PG_PORT"]
    db_password = env_vars["PG_PASSWORD"]
    db_name     = env_vars["PG_DB_NAME"]

    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(SQLALCHEMY_DATABASE_URI)

    synthesizer = Synthesizer(model="gpt-3.5-turbo")

    n_pages  = 2
    contexts = []
    with engine.connect() as connection:
        query = text(f"SELECT * FROM public.pages ORDER BY id ASC LIMIT {n_pages}")
        result = connection.execute(query)
        for row in result:
            c = [normalize(row[2])]
            contexts.append(c)    

    #dataset = EvaluationDataset()
    synthesizer.generate_goldens(
        contexts=contexts,
        include_expected_output = True
    )

    synthesizer.save_as(
    file_type='json', # or 'csv'
    directory="./synthetic_data"
    )


    """
    dataset = EvaluationDataset()
    dataset.generate_goldens(
        synthesizer=synthesizer,
        contexts=contexts
    )

    dataset.save_as(
    file_type='json', # or 'csv'
    directory="./synthetic_data"
    )
    """


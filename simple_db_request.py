from sqlalchemy import text
from sqlalchemy import create_engine
from dotenv import dotenv_values

import os


if __name__=='__main__':


    env_vars = dotenv_values(".env")

    db_host = env_vars["PG_HOST"]
    db_user = env_vars["PG_USER"]
    db_port = env_vars["PG_PORT"]
    db_password = env_vars["PG_PASSWORD"]
    db_name     = env_vars["PG_DB_NAME"]

    SQLALCHEMY_DATABASE_URI = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    engine = create_engine(SQLALCHEMY_DATABASE_URI)


    with engine.connect() as connection:
        query = text("SELECT * FROM public.text_fragments ORDER BY id ASC LIMIT 1")
        result = connection.execute(query)
        for row in result:
            print(row[1])




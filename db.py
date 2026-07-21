import os
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from logging_config import logger

def database_conn():
    try:
        
        logger.info("Database Connection Start:")
        return psycopg2.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            database=os.getenv("DB_NAME"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
    
    except Exception as e:
        logger.info("Databse Connection Failed %s",e)
        

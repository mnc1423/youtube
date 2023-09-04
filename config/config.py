import os
from dotenv import load_dotenv
load_dotenv()

def get_api_key() -> str:
    return os.getenv("API_KEY")

def get_es_server() -> str:
    return os.getenv("ES_SERVER")
def get_es_port() -> int:
    return os.getenv("ES_PORT")
def get_es_index() -> str:
    return os.getenv("ES_INDEX")
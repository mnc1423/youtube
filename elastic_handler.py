from elasticsearch import Elasticsearch, helpers
from config import config

class esHandler:
    def __init__(self):
        es_host=config.get_es_server()
        es_port=config.get_es_port()
        self.es_client = Elasticsearch(
            "localhost",
            port=es_port
        )
        self.es_index = config.get_es_index()
    
    def create_doc(self, data):
        doc = {
            "_op_type": "create",
            "_index": self.es_index,
            "_id": data['_id'] 
        }

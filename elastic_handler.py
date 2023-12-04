from elasticsearch import Elasticsearch, helpers
from config import config


class esHandler:
    def __init__(self):
        es_host = config.get_es_server()
        es_port = config.get_es_port()
        es_user = config.get_es_user()
        es_password = config.get_es_password()
        self.es_client = Elasticsearch(
            hosts=[{"host": "172.18.0.2", "port": 9200, "scheme": "https"}],
            http_auth=(es_user, es_password),
            verify_certs=False,
        )

        self.es_index = config.get_es_index()

    def create_doc(self, data):
        doc = {
            "_op_type": "create",
            "_index": self.es_index,
            "_id": data["_id"],
            "url_list": data["url_list"],
            "vid_title": data["vid_title"],
            "publishedAt": data["publishedAt"],
            "channelTitle": data["channelTitle"],
            "channelId": data["channelId"],
        }
        return doc

    def createInputData(self, _list):
        inputList = []
        for docs in _list:
            doc = self.create_doc(docs)
            inputList.append(doc)
            return inputList

    def generate_documents(self, _list):
        for doc in _list:
            yield doc

    def esInput(self, _list):
        success, failed = 0, 0
        for ok, result in helpers.streaming_bulk(
            client=self.es_client, actions=self.generate_documents(_list)
        ):
            if not ok:
                failed += 1
            else:
                success += 1
        print(success, failed)

    def testDummyData(self):
        doc = {
            "url_list": "test_url",
            "vid_title": "test_title",
            "publishedAt": "test_date",
            "channelTitle": "test_title",
            "channelId": "test_channel",
        }
        result = self.es_client.index(index="test", id=1, body=doc)
        # res = self.es_client.get(index="test", id="1")
        print(result)


if __name__ == "__main__":
    a = esHandler()
    a.testDummyData()

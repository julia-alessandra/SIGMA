from pymongo import MongoClient

class ConexaoMongo:
    def __init__(self, uri="mongodb://localhost:27017/", database_nome="faculdade"):
        self.client = MongoClient(uri)
        self.db = self.client[database_nome]

    def get_colecao(self, nome_colecao):
        return self.db[nome_colecao]
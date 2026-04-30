from models.materia import Materia

class MateriaRepository:
    def __init__(self, conexao):
        self.colecao = conexao.get_colecao("materias")

    def salvar_ou_atualizar(self, materia):

        self.colecao.update_one(
            {"codigo": materia.codigo},
            {"$set": materia.to_dict()},
            upsert=True
        )

    def salvar_todas(self, lista_materias):
        for materia in lista_materias:
            self.salvar_ou_atualizar(materia)

    def listar_todas(self):
        cursor = self.colecao.find()
        return [Materia.from_dict(doc) for doc in cursor]

    def atualizar_status_conclusao(self, codigo, status):
        self.colecao.update_one(
            {"codigo": codigo},
            {"$set": {"concluida": status}}
        )

    def listar_todas(self):
        cursor = self.colecao.find()
        return [Materia.from_dict(doc) for doc in cursor]

    def limpar_banco(self):
        resultado = self.colecao.delete_many({})
        return resultado.deleted_count

    def remover_por_codigo(self, codigo):
        """Remove uma matéria específica do MongoDB"""
        resultado = self.colecao.delete_one({"codigo": codigo})
        return resultado.deleted_count > 0
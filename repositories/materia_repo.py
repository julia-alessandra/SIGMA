class MateriaRepository:
    def __init__(self, conexao):
        self.colecao = conexao.get_colecao("materias")

    def salvar_varias(self, lista_materias):
        documentos = [materia.to_dict() for materia in lista_materias]
        if documentos:
            self.colecao.insert_many(documentos)
            print(f"{len(documentos)} matérias salvas no MongoDB com sucesso!")
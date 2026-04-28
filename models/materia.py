class Materia:
    def __init__(self, codigo, nome, natureza, creditos, carga_horaria, 
                 pre_requisitos, periodo_sugerido, concluida=False):
        self.codigo = codigo
        self.nome = nome
        self.natureza = natureza
        self.creditos = creditos
        self.carga_horaria = carga_horaria
        self.pre_requisitos = pre_requisitos
        self.periodo_sugerido = periodo_sugerido
        self.concluida = concluida

    def to_dict(self):
        # Retorna todos os atributos como um dicionário para o JSON
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "natureza": self.natureza,
            "creditos": self.creditos,
            "carga_horaria": self.carga_horaria,
            "pre_requisitos": self.pre_requisitos,
            "periodo_sugerido": self.periodo_sugerido,
            "concluida": self.concluida
        }

    @staticmethod
    def from_dict(dados):
        # Método auxiliar para reconstruir o objeto a partir de dados do banco
        return Materia(
            codigo=dados.get("codigo"),
            nome=dados.get("nome"),
            natureza=dados.get("natureza"),
            creditos=dados.get("creditos"),
            carga_horaria=dados.get("carga_horaria"),
            pre_requisitos=dados.get("pre_requisitos"),
            periodo_sugerido=dados.get("periodo_sugerido"),
            concluida=dados.get("concluida", False)
        )
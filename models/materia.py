class Materia:
    def __init__(self, codigo, nome, natureza, creditos, carga_horaria, pre_requisitos, periodo_sugerido):
        self.codigo = codigo
        self.nome = nome
        self.natureza = natureza
        self.creditos = creditos
        self.carga_horaria = carga_horaria
        self.pre_requisitos = pre_requisitos
        self.periodo_sugerido = periodo_sugerido

    def to_dict(self):
        # Facilita na hora de salvar no MongoDB ou gerar o JSON
        return {
            "codigo": self.codigo,
            "nome": self.nome,
            "natureza": self.natureza,
            "creditos": self.creditos,
            "carga_horaria": self.carga_horaria,
            "pre_requisitos": self.pre_requisitos,
            "periodo_sugerido": self.periodo_sugerido
        }
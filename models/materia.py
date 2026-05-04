from .falta import Falta

class Materia:
    def __init__(self, codigo, nome, natureza, creditos, carga_horaria, 
                 pre_requisitos, periodo_sugerido, concluida=False, faltas=None):
        self.codigo = codigo
        self.nome = nome
        self.natureza = natureza
        self.creditos = creditos
        self.carga_horaria = carga_horaria
        self.pre_requisitos = pre_requisitos
        self.periodo_sugerido = periodo_sugerido
        self.concluida = concluida
        
        self.faltas = [Falta.from_dict(f) if isinstance(f, dict) else f for f in (faltas or [])]

    def adicionar_falta(self, horas):
        nova_falta = Falta(horas)
        self.faltas.append(nova_falta)
        return nova_falta

    def calcular_limite_faltas(self):
        return int((self.creditos * 15) * 0.25)

    def faltas_gastas(self):
        return sum(f.horas for f in self.faltas)

    def faltas_disponiveis(self):
        return self.calcular_limite_faltas() - self.faltas_gastas()

    def to_dict(self):
        dados = {
            "codigo": self.codigo,
            "nome": self.nome,
            "natureza": self.natureza,
            "creditos": self.creditos,
            "carga_horaria": self.carga_horaria,
            "pre_requisitos": self.pre_requisitos,
            "periodo_sugerido": self.periodo_sugerido,
            "concluida": self.concluida,
            "faltas": [f.to_dict() for f in self.faltas]
        }
        return dados
    
    @staticmethod
    def from_dict(dados):
        return Materia(
            codigo=dados.get("codigo"),
            nome=dados.get("nome"),
            natureza=dados.get("natureza"),
            creditos=dados.get("creditos"),
            carga_horaria=dados.get("carga_horaria"),
            pre_requisitos=dados.get("pre_requisitos"),
            periodo_sugerido=dados.get("periodo_sugerido"),
            concluida=dados.get("concluida", False),
            faltas=dados.get("faltas", [])
        )
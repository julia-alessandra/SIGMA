from datetime import datetime

class Falta:
    def __init__(self, horas, data=None):
        self.data = data if data else datetime.now().strftime("%d/%m/%Y")
        self.horas = float(horas)

    def to_dict(self):
        return {
            "data": self.data,
            "horas": self.horas
        }

    @staticmethod
    def from_dict(dados):
        return Falta(horas=dados["horas"], data=dados["data"])
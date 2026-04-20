import pdfplumber
import re
from models.materia import Materia

class ExtratorCurriculo:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.re_disciplina = re.compile(r'(?:DIG-?)?\s*([A-Z]{3}\d{3})[\s\-]+(.*?)(?=(?:DIG-?\s*[A-Z]{3}\d{3})|$)')
        self.re_periodo = re.compile(r'(\d+)º\s+PERÍODO')

    def extrair_materias(self):
        materias_extraidas = []
        periodo_atual = 0

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                texto_pagina = page.extract_text() or ""
                busca_periodo = self.re_periodo.search(texto_pagina)
                if busca_periodo:
                    periodo_atual = int(busca_periodo.group(1))

                tabelas = page.extract_tables()
                for tabela in tabelas:
                    for row in tabela:
                        if not row or not row[0] or "Atividade" in str(row[0]):
                            continue

                        texto_coluna_0 = str(row[0]).replace('\n', ' ')
                        
                        encontradas = list(self.re_disciplina.finditer(texto_coluna_0))
                        
                        if encontradas:
                            creditos_raw = str(row[1]) if len(row) > 1 else ""
                            lista_creditos = re.findall(r'\d+', creditos_raw)
                            
                            for i, match in enumerate(encontradas):
                                codigo = match.group(1).strip()
                                nome = match.group(2).strip()
                                
                                creditos = 0
                                if i < len(lista_creditos):
                                    creditos = int(lista_creditos[i])
                                    
                                try:
                                    materia = Materia(
                                        codigo=codigo,
                                        nome=nome,
                                        natureza="OB",      # Preenchimento padrão
                                        creditos=creditos,
                                        carga_horaria=0,    # Preenchimento padrão para não quebrar a classe
                                        pre_requisitos=[],  # Preenchimento padrão
                                        periodo_sugerido=periodo_atual
                                    )
                                    materias_extraidas.append(materia)
                                except Exception as e:
                                    print(f"Erro ao instanciar matéria {codigo}: {e}")

        return materias_extraidas
import pdfplumber
import re
from models.materia import Materia

class ExtratorCurriculo:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.re_disciplina = re.compile(r'(?:DIG-?)?\s*([A-Z]{3}\d{3})[\s\-]+(.*?)(?=(?:DIG-?\s*[A-Z]{3}\d{3})|$)')
        self.re_codigo = re.compile(r'[A-Z]{3}\d{3}')
        self.re_periodo = re.compile(r'(\d+)º\s*PERÍODO', re.IGNORECASE)

    def _identificar_indices(self, row):
        headers = [str(cell).lower() if cell else "" for cell in row]
        indices = {'materia': 0, 'creditos': 1, 'grupo': -1, 'pre_requisitos': -1}
        
        for i, h in enumerate(headers):
            if 'grupo' in h and 'natureza' not in h:
                indices['grupo'] = i
            if any(term in h for term in ['pré', 'pre', 'req']):
                indices['pre_requisitos'] = i
        return indices

    def extrair_materias(self):
        materias_extraidas = []
        secao_optativa = False 
        periodo_atual = None 

        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                texto_pagina = page.extract_text() or ""
                
                match_periodo = self.re_periodo.search(texto_pagina)
                if match_periodo:
                    periodo_atual = int(match_periodo.group(1))

                if "optativas no percurso" in texto_pagina.lower():
                    secao_optativa = True
                    periodo_atual = None

                tabelas = page.extract_tables()
                for tabela in tabelas:
                    if not tabela or len(tabela) < 2: continue
                    
                    indices = self._identificar_indices(tabela[0])
                    
                    for row in tabela:
                        # Pula linhas vazias ou que sejam apenas cabeçalhos
                        if not row or not row[0] or any(x in str(row[0]) for x in ["Atividade", "Código", "Natureza"]):
                            continue

                        texto_coluna_materia = str(row[indices['materia']]).replace('\n', ' ')
                        encontradas = list(self.re_disciplina.finditer(texto_coluna_materia))
                        
                        if encontradas:
                            grupo_val = str(row[indices['grupo']]).strip() if indices['grupo'] != -1 else ""
                            if grupo_val == "1":
                                natureza = "OB"
                            elif grupo_val == "2":
                                natureza = "EC" # Estágio
                            elif secao_optativa or grupo_val in ["3", "4", "5", "7"]:
                                natureza = "OP"
                            else:
                                natureza = "OB"

                            creditos_raw = str(row[indices['creditos']])
                            lista_creditos = re.findall(r'\d+', creditos_raw)

                            # Pre requisitos
                            texto_requisitos = ""
                            if indices['pre_requisitos'] != -1:
                                texto_requisitos = str(row[indices['pre_requisitos']])
                            
                            if not self.re_codigo.search(texto_requisitos):
                                texto_requisitos = " ".join([str(c) for c in row[2:] if c])

                            for i, match in enumerate(encontradas):
                                codigo = match.group(1).strip()
                                nome = match.group(2).strip()
                                creditos = int(lista_creditos[i]) if i < len(lista_creditos) else 0
                                
                                pre_reqs = [c for c in self.re_codigo.findall(texto_requisitos) if c != codigo]
                                
                                try:
                                    materia = Materia(
                                        codigo=codigo,
                                        nome=nome,
                                        natureza=natureza,
                                        creditos=creditos,
                                        carga_horaria=creditos * 15,
                                        pre_requisitos=list(dict.fromkeys(pre_reqs)),
                                        periodo_sugerido=periodo_atual
                                    )
                                    materias_extraidas.append(materia)
                                except Exception as e:
                                    print(f"Erro ao criar objeto Materia {codigo}: {e}")

        return materias_extraidas
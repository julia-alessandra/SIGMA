import tkinter as tk
from database.conexao import ConexaoMongo
from repositories.materia_repo import MateriaRepository
from services.extrator_pdf import ExtratorCurriculo
from view.gui import AplicativoMaterias

class ControladorPrincipal:
    def __init__(self):
        self.conexao = ConexaoMongo()
        self.repo = MateriaRepository(self.conexao)

        self.root = tk.Tk()      
        self.app = AplicativoMaterias(
            self.root, 
            self.processar_pdf, 
            self.buscar_do_banco,
            self.excluir_materia 
        )
        self.app.repo = self.repo 
        self.carregar_dados_iniciais()

    def buscar_do_banco(self):
        return self.repo.listar_todas()

    def excluir_materia(self, codigo):
        return self.repo.remover_por_codigo(codigo)

    def carregar_dados_iniciais(self):
        materias_existentes = self.buscar_do_banco()
        if materias_existentes:
            print(f"Carregando {len(materias_existentes)} matérias do banco...")
            self.app.materias_objetos = materias_existentes
            self.app.atualizar_interface()

    def processar_pdf(self, caminho_pdf):
        extrator = ExtratorCurriculo(caminho_pdf)
        materias_novas = extrator.extrair_materias()
      
        self.repo.salvar_todas(materias_novas)
      
        return materias_novas

    def iniciar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app_controlador = ControladorPrincipal()
    app_controlador.iniciar()
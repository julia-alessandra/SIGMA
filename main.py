import tkinter as tk
from database.conexao import ConexaoMongo
from repositories.materia_repo import MateriaRepository
from services.extrator_pdf import ExtratorCurriculo
from view.gui import AplicativoMaterias, TelaInicial, TelaFaltas
from datetime import datetime

class ControladorPrincipal:
    def __init__(self):
        self.conexao = ConexaoMongo()
        self.repo = MateriaRepository(self.conexao)

        self.root = tk.Tk()      
        self.root.title("SIGMA - Gestão Acadêmica UFMG")
        self.root.geometry("1100x700")
        
        self.tela_atual = None
        self.navegar_para_inicial()

    def destruir_tela_atual(self):
        if self.tela_atual:
            self.tela_atual.destroy()

    def navegar_para_inicial(self):
        self.destruir_tela_atual()
        self.tela_atual = TelaInicial(self.root, self.navegar_para_materias, self.navegar_para_faltas)

    def navegar_para_materias(self):
        self.destruir_tela_atual()
        self.tela_atual = AplicativoMaterias(
            self.root, 
            self.processar_pdf, 
            self.buscar_do_banco,
            self.excluir_materia
        )
        self.tela_atual.repo = self.repo
        self.tela_atual.pack(expand=True, fill="both")
        
        tk.Button(self.tela_atual.toolbar, text="Voltar ao Menu", command=self.navegar_para_inicial).pack(side="right", padx=10)

    def navegar_para_faltas(self):
        self.destruir_tela_atual()
        materias_do_banco = self.buscar_do_banco()
        
        self.tela_atual = TelaFaltas(
            self.root, 
            materias_do_banco, 
            self.navegar_para_inicial, 
            self.registrar_falta
        )
        self.tela_atual.pack(expand=True, fill="both")

    def registrar_falta(self, codigo, horas):
        nova_falta = {"data": datetime.now().strftime("%d/%m/%Y"), "horas": horas}
        return self.repo.registrar_falta(codigo, nova_falta)

    def buscar_do_banco(self):
        return self.repo.listar_todas()

    def excluir_materia(self, codigo):
        return self.repo.remover_por_codigo(codigo)

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
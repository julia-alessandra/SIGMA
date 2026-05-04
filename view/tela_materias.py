import tkinter as tk
from tkinter import filedialog, messagebox
from view.components import Toolbar, TabelaMaterias

class AplicativoMaterias(tk.Frame):
    def __init__(self, parent, extrator_callback, recarregar_callback, excluir_callback):
        super().__init__(parent)
        self.extrator_callback = extrator_callback
        self.recarregar_callback = recarregar_callback
        self.excluir_callback = excluir_callback
        self.materias_objetos = []
        self.repo = None

        self.toolbar = Toolbar(self, self.selecionar_arquivo, self.solicitar_recarga, self.confirmar_exclusao)
        self.tabela = TabelaMaterias(self, self.alternar_status_materia)

    def solicitar_recarga(self):
        novas = self.recarregar_callback()
        if not novas:
            messagebox.showinfo("SIGMA", "O banco de dados está vazio")
        self.materias_objetos = novas
        self.atualizar_interface()

    def confirmar_exclusao(self):
        item_id = self.tabela.focus()
        if not item_id:
            messagebox.showwarning("Aviso", "Selecione uma matéria")
            return

        codigo = self.tabela.item(item_id, 'values')[1]
        if messagebox.askyesno("Confirmar", f"Excluir a matéria {codigo}?"):
            if self.excluir_callback(codigo):
                self.solicitar_recarga()
            else:
                messagebox.showerror("Erro", "Falha ao excluir.")

    def alternar_status_materia(self, event):
        item_id = self.tabela.focus()
        if not item_id: return
        codigo = self.tabela.item(item_id, 'values')[1]
        for m in self.materias_objetos:
            if m.codigo == codigo:
                m.concluida = not m.concluida
                self.repo.atualizar_status_conclusao(m.codigo, m.concluida)
                break
        self.atualizar_interface()

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho:
            self.materias_objetos = self.extrator_callback(caminho)
            self.atualizar_interface()

    def calcular_status(self, materia, codigos_concluidos):
        if materia.concluida: return "Concluida"
        if not materia.pre_requisitos: return "Pendente"
        todos_concluidos = all(req in codigos_concluidos for req in materia.pre_requisitos)
        return "Pendente" if todos_concluidos else "Bloqueada"

    def atualizar_interface(self):
        self.tabela.limpar()
        creditos_totais = 0
        codigos_concluidos = {m.codigo for m in self.materias_objetos if m.concluida}
        for m in self.materias_objetos:
            status = self.calcular_status(m, codigos_concluidos)
            self.tabela.inserir_materia(m, status)
            if m.concluida: creditos_totais += m.creditos
        self.toolbar.atualizar_resumo(creditos_totais)
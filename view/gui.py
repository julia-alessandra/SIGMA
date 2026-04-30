import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class AplicativoMaterias:
    def __init__(self, root, extrator_callback, recarregar_callback, excluir_callback):
        self.root = root
        self.root.title("SIGMA - Gestão Acadêmica UFMG")
        self.root.geometry("1100x700")
        
        self.extrator_callback = extrator_callback
        self.recarregar_callback = recarregar_callback
        self.excluir_callback = excluir_callback
        
        self.materias_objetos = []

        frame_topo = tk.Frame(root)
        frame_topo.pack(fill="x", padx=10, pady=10)

        tk.Button(frame_topo, text="Importar PDF", command=self.selecionar_arquivo).pack(side="left", padx=5)
        tk.Button(frame_topo, text="Recarregar do Banco", command=self.solicitar_recarga).pack(side="left", padx=5)
        
        self.btn_excluir = tk.Button(frame_topo, text="Excluir Selecionada", command=self.confirmar_exclusao, fg="red")
        self.btn_excluir.pack(side="left", padx=5)

        self.lbl_resumo = tk.Label(frame_topo, text="Créditos Concluídos: 0", font=("Arial", 10, "bold"))
        self.lbl_resumo.pack(side="right")

        self.colunas = ("status", "codigo", "nome", "natureza", "creditos", "pre_requisitos")
        self.tabela = ttk.Treeview(root, columns=self.colunas, show="headings")
        
        self.tabela.heading("status", text="Status")
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("natureza", text="Nat.")
        self.tabela.heading("creditos", text="Créd.")
        self.tabela.heading("pre_requisitos", text="Pré-requisitos")

        self.tabela.bind("<Double-1>", self.alternar_status_materia)
        self.tabela.pack(expand=True, fill="both", padx=10, pady=5)

    def solicitar_recarga(self):
        self.materias_objetos = self.recarregar_callback()
        self.atualizar_interface()

    def confirmar_exclusao(self):
        item_id = self.tabela.focus()
        if not item_id:
            messagebox.showwarning("Aviso", "Selecione uma matéria!")
            return

        valores = self.tabela.item(item_id, 'values')
        codigo = valores[1]
        
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

    def atualizar_interface(self):
        for i in self.tabela.get_children():
            self.tabela.delete(i)
        creditos_totais = 0
        for m in self.materias_objetos:
            status = "Concluida" if m.concluida else "Pendente"
            self.tabela.insert("", "end", values=(status, m.codigo, m.nome, m.natureza, m.creditos, m.pre_requisitos))
            if m.concluida: creditos_totais += m.creditos
        self.lbl_resumo.config(text=f"Créditos Concluídos: {creditos_totais}")
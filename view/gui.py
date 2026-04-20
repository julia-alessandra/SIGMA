import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class AplicativoMaterias:
    def __init__(self, root, extrator_callback):
        self.root = root
        self.root.title("Extrator de Currículo - POO")
        self.root.geometry("800x500")
        
        self.extrator_callback = extrator_callback

        self.btn_carregar = tk.Button(root, text="Selecionar PDF", command=self.selecionar_arquivo)
        self.btn_carregar.pack(pady=10)

        self.colunas = ("codigo", "nome", "periodo", "creditos")
        self.tabela = ttk.Treeview(root, columns=self.colunas, show="headings")
        
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome da Disciplina")
        self.tabela.heading("periodo", text="Período")
        self.tabela.heading("creditos", text="Créditos")
        
        self.tabela.column("codigo", width=80)
        self.tabela.column("nome", width=400)
        self.tabela.column("periodo", width=80)
        self.tabela.column("creditos", width=80)
        
        self.tabela.pack(expand=True, fill="both", padx=10, pady=10)

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho:
            try:
                materias = self.extrator_callback(caminho)
                self.atualizar_lista(materias)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível ler o arquivo: {e}")

    def atualizar_lista(self, materias):
        for i in self.tabela.get_children():
            self.tabela.delete(i)
            
        for m in materias:
            self.tabela.insert("", "end", values=(
                m.codigo, 
                m.nome, 
                f"{m.periodo_sugerido}º", 
                m.creditos
            ))
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class AplicativoMaterias:
    def __init__(self, root, extrator_callback):
        self.root = root
        self.root.title("Extrator de Currículo")
        self.root.geometry("1000x600")
        
        self.extrator_callback = extrator_callback

        self.btn_carregar = tk.Button(root, text="Selecionar PDF", command=self.selecionar_arquivo)
        self.btn_carregar.pack(pady=10)

        self.colunas = ("codigo", "nome", "natureza", "creditos", "pre_requisitos")
        self.tabela = ttk.Treeview(root, columns=self.colunas, show="headings")
        
        # Configuração de cabeçalhos
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome da Disciplina")
        self.tabela.heading("natureza", text="Nat.")
        self.tabela.heading("creditos", text="Créd.")
        self.tabela.heading("pre_requisitos", text="Pré-requisitos")
        
        # Dimensionamento das colunas (widths)
        self.tabela.column("codigo", width=80, anchor="center")
        self.tabela.column("nome", width=350, anchor="w")
        self.tabela.column("natureza", width=50, anchor="center")
        self.tabela.column("creditos", width=50, anchor="center")
        self.tabela.column("pre_requisitos", width=250, anchor="w")
        
        # Scroll lateral
        scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tabela.yview)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        
        self.tabela.pack(side="left", expand=True, fill="both", padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", pady=10, padx=(0, 10))

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho:
            try:
                materias = self.extrator_callback(caminho)
                self.atualizar_lista(materias)
            except Exception as e:
                messagebox.showerror("Erro", f"Falha na extração: {e}")

    def atualizar_lista(self, materias):
        for i in self.tabela.get_children():
            self.tabela.delete(i)
            
        for m in materias:
            pre_req_str = ", ".join(m.pre_requisitos) if m.pre_requisitos else "-"
            
            self.tabela.insert("", "end", values=(
                m.codigo, 
                m.nome, 
                m.natureza, 
                m.creditos,
                pre_req_str
            ))
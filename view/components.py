import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class Toolbar(tk.Frame):
    def __init__(self, parent, on_import, on_reload, on_delete):
        super().__init__(parent)
        self.pack(fill="x", padx=10, pady=10)

        tk.Button(self, text="Importar PDF", command=on_import).pack(side="left", padx=5)
        tk.Button(self, text="Recarregar do Banco", command=on_reload).pack(side="left", padx=5)
        
        self.btn_excluir = tk.Button(self, text="Excluir Selecionada", command=on_delete, fg="red")
        self.btn_excluir.pack(side="left", padx=5)

        self.lbl_resumo = tk.Label(self, text="Créditos Concluídos: 0", font=("Arial", 10, "bold"))
        self.lbl_resumo.pack(side="right")

    def atualizar_resumo(self, total):
        self.lbl_resumo.config(text=f"Créditos Concluídos: {total}")


class TabelaMaterias(ttk.Treeview):
    def __init__(self, parent, on_double_click):
        colunas = ("status", "codigo", "nome", "natureza", "creditos", "pre_requisitos")
        super().__init__(parent, columns=colunas, show="headings")
        
        cabecalhos = {
            "status": "Status", "codigo": "Código", "nome": "Nome",
            "natureza": "Nat.", "creditos": "Créd.", "pre_requisitos": "Pré-requisitos"
        }
        for col, texto in cabecalhos.items():
            self.heading(col, text=texto)
            self.column(col, width=100 if col != "nome" else 350)

        self.bind("<Double-1>", on_double_click)
        self.pack(expand=True, fill="both", padx=10, pady=5)

        self.tag_configure('bloqueada', foreground='red')
        self.tag_configure('pendente', foreground='black')
        self.tag_configure('concluida', foreground='green')

    def limpar(self):
        for i in self.get_children():
            self.delete(i)

    def inserir_materia(self, m, status_calculado):
        tag = status_calculado.lower()
        self.insert("", "end", values=(
            status_calculado, m.codigo, m.nome, m.natureza, m.creditos, m.pre_requisitos
        ), tags=(tag,))
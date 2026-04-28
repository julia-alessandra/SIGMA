import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class AplicativoMaterias:
    def __init__(self, root, extrator_callback):
        self.root = root
        self.root.title("SIGMA - Gestão Acadêmica UFMG")
        self.root.geometry("1100x700")
        
        self.extrator_callback = extrator_callback
        self.materias_objetos = [] # Lista para guardar os objetos Materia em memória

        # --- Frame Superior (Controles e Resumo) ---
        frame_topo = tk.Frame(root)
        frame_topo.pack(fill="x", padx=10, pady=10)

        self.btn_carregar = tk.Button(frame_topo, text="Importar PDF", command=self.selecionar_arquivo)
        self.btn_carregar.pack(side="left")

        self.lbl_resumo = tk.Label(frame_topo, text="Créditos Concluídos: 0", font=("Arial", 12, "bold"))
        self.lbl_resumo.pack(side="right")

        # --- Tabela ---
        # Adicionamos a coluna "status"
        self.colunas = ("status", "codigo", "nome", "natureza", "creditos", "pre_requisitos")
        self.tabela = ttk.Treeview(root, columns=self.colunas, show="headings")
        
        self.tabela.heading("status", text="Status")
        self.tabela.heading("codigo", text="Código")
        self.tabela.heading("nome", text="Nome")
        self.tabela.heading("natureza", text="Nat.")
        self.tabela.heading("creditos", text="Créd.")
        self.tabela.heading("pre_requisitos", text="Pré-requisitos")

        self.tabela.column("status", width=100, anchor="center")
        self.tabela.column("codigo", width=80, anchor="center")
        self.tabela.column("nome", width=350)
        self.tabela.column("natureza", width=50, anchor="center")
        self.tabela.column("creditos", width=50, anchor="center")
        
        # Evento de clique duplo para alternar status
        self.tabela.bind("<Double-1>", self.alternar_status_materia)
        
        self.tabela.pack(expand=True, fill="both", padx=10, pady=5)
        
        tk.Label(root, text="Dica: Clique duplo em uma matéria para marcar como concluída", fg="gray").pack()

    def selecionar_arquivo(self):
        caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
        if caminho:
            try:
                # O extrator retorna a lista de objetos Materia
                self.materias_objetos = self.extrator_callback(caminho)
                self.atualizar_interface()
            except Exception as e:
                messagebox.showerror("Erro", f"Falha na extração: {e}")

    def alternar_status_materia(self, event):
        item_id = self.tabela.focus()
        if not item_id: return
        
        valores = self.tabela.item(item_id, 'values')
        codigo_materia = valores[1] # O código está na segunda coluna (índice 1)

        # Localiza o objeto na lista e inverte o status
        for m in self.materias_objetos:
            if m.codigo == codigo_materia:
                m.concluida = not m.concluida
                break
        
        self.atualizar_interface()

    def atualizar_interface(self):
        # Limpa tabela
        for i in self.tabela.get_children():
            self.tabela.delete(i)
            
        total_creditos = 0
        
        for m in self.materias_objetos:
            status_texto = "Concluída" if m.concluida else "Pendente"
            pre_req_str = ", ".join(m.pre_requisitos) if m.pre_requisitos else "-"
            
            # Adiciona na tabela
            self.tabela.insert("", "end", values=(
                status_texto,
                m.codigo, 
                m.nome, 
                m.natureza, 
                m.creditos,
                pre_req_str
            ))
            
            if m.concluida:
                total_creditos += m.creditos

        # Atualiza o contador de créditos no topo
        self.lbl_resumo.config(text=f"Créditos Concluídos: {total_creditos}")
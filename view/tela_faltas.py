import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TelaFaltas(tk.Frame):
    def __init__(self, parent, materias, on_voltar, on_salvar_falta):
        super().__init__(parent)
        self.materias = materias
        self.on_salvar_falta = on_salvar_falta
        self.materia_selecionada = None

        topbar = tk.Frame(self, bg="#e1e1e1", pady=5, padx=10)
        topbar.pack(fill="x")
        tk.Button(topbar, text="Voltar ao Menu", command=on_voltar).pack(side="left")

        container = tk.Frame(self)
        container.pack(expand=True, fill="both", padx=20, pady=20)

        frame_lista = tk.Frame(container)
        frame_lista.pack(side="left", fill="y", padx=(0, 20))
        tk.Label(frame_lista, text="Selecione a Matéria:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.listbox = tk.Listbox(frame_lista, width=40, font=("Arial", 11))
        self.listbox.pack(expand=True, fill="y")
        self.listbox.bind("<<ListboxSelect>>", self.ao_selecionar_materia)

        for m in self.materias:
            if not m.concluida:
                self.listbox.insert("end", f"{m.codigo} - {m.nome}")

        self.frame_detalhe = tk.Frame(container)
        self.frame_detalhe.pack(side="left", expand=True, fill="both")
        
        self.lbl_nome = tk.Label(self.frame_detalhe, text="Nenhuma matéria selecionada", font=("Arial", 14, "bold"))
        self.lbl_nome.pack(anchor="w", pady=(0, 20))

        self.lbl_info = tk.Label(self.frame_detalhe, text="", font=("Arial", 12), justify="left")
        self.lbl_info.pack(anchor="w", pady=(0, 20))

        self.frame_form = tk.Frame(self.frame_detalhe)
        tk.Label(self.frame_form, text="Horas de aula que faltou:").pack(anchor="w")
        self.ent_horas = tk.Entry(self.frame_form)
        self.ent_horas.pack(anchor="w", pady=5)
        
        tk.Button(self.frame_form, text="Registrar Falta", bg="red", fg="white", 
                  command=self.salvar_falta).pack(anchor="w", pady=10)


    def ao_selecionar_materia(self, event):
        selecao = self.listbox.curselection()
        if not selecao: return
        codigo = self.listbox.get(selecao[0]).split(" - ")[0]
        self.materia_selecionada = next((m for m in self.materias if m.codigo == codigo), None)
        self.atualizar_painel_detalhes()

    def atualizar_painel_detalhes(self):
        m = self.materia_selecionada
        self.lbl_nome.config(text=f"{m.codigo} - {m.nome}")
        
        texto_info = (
            f"Créditos: {m.creditos}\n"
            f"Carga Horária Total: {m.creditos * 15}h\n\n"
            f"Limite de Faltas (25%): {m.calcular_limite_faltas()}h\n"
            f"Faltas já utilizadas: {m.faltas_gastas()}h\n"
            f"Você tem {m.faltas_disponiveis()} horas de faltas disponíveis."
        )
        self.lbl_info.config(text=texto_info)
        self.frame_form.pack(anchor="w", fill="x")

    def salvar_falta(self):
        if not self.materia_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma matéria")
            return

        try:
            horas = float(self.ent_horas.get())
            
            self.on_salvar_falta(self.materia_selecionada.codigo, horas)
            self.materia_selecionada.adicionar_falta(horas)
            
            self.atualizar_painel_detalhes()
            self.ent_horas.delete(0, 'end')
            
            messagebox.showinfo("Sucesso", "Falta registrada")
        except ValueError:
            messagebox.showerror("Erro", "Insira um valor numérico válido.")
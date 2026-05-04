import tkinter as tk

class TelaInicial(tk.Frame):
    def __init__(self, parent, on_acessar_materias, on_acessar_faltas):
        super().__init__(parent)
        self.pack(expand=True, fill="both")
        
        frame_central = tk.Frame(self)
        frame_central.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame_central, text="SIGMA", font=("Arial", 40, "bold"), fg="#1a73e8").pack(pady=(0, 10))

        tk.Button(frame_central, text="Acessar Matérias", font=("Arial", 14), command=on_acessar_materias, 
                  bg="#4CAF50", fg="white", width=20, pady=10).pack(pady=10)
                  
        tk.Button(frame_central, text="Lançar Faltas", font=("Arial", 14), command=on_acessar_faltas, 
                  bg="#4CAF50", fg="white", width=20, pady=10).pack(pady=10)
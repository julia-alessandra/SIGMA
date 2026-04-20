import tkinter as tk
from services.extrator_pdf import ExtratorCurriculo
from view.gui import AplicativoMaterias

def acao_extrair(caminho_pdf):
    extrator = ExtratorCurriculo(caminho_pdf)
    return extrator.extrair_materias()

def main():
    root = tk.Tk()
    app = AplicativoMaterias(root, acao_extrair)
    root.mainloop()

if __name__ == "__main__":
    main()
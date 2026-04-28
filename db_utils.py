from database.conexao import ConexaoMongo
from repositories.materia_repo import MateriaRepository

def menu_utilitario():
    conexao = ConexaoMongo()
    repo = MateriaRepository(conexao)

    print("1. Listar matérias no banco")
    print("2. Limpar todo o banco")
    print("3. Sair")
    
    opcao = input("\nEscolha:")

    if opcao == "1":
        materias = repo.listar_todas()
        if not materias:
            print("O banco está vazio.")
        for m in materias:
            status = "[X]" if m.concluida else "[ ]"
            print(f"{status} {m.codigo} - {m.nome} ({m.creditos} créditos)")
            
    elif opcao == "2":
        confirmar = input("Apagar TUDO? (s/n): ")
        if confirmar.lower() == 's':
            qtd = repo.limpar_banco()
            print(f"{qtd} registros removidos.")
            
    elif opcao == "3":
        exit()

if __name__ == "__main__":
    menu_utilitario()
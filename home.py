from ultils import limpar_terminal, CriarArquivos
CriarArquivos()

from usuarios import ModuloClientes
from estoque import ModuloEstoque
from vendas import ModuloVendas


def Home():
    while True:
        limpar_terminal()
        print("""
    ============================
                HOME
    ============================
        1 - Gerir Clientes
        2 - Gerir Estoque
        3 - Gerir Vendas
        4 - Sair do Sistema
    ============================
        """)

        modulo = input("qual modulo você deseja acessar ? :")

        if modulo == '1':
            limpar_terminal(0.2)
            ModuloClientes()
            

        elif modulo == '2':
            limpar_terminal(0.2)
            ModuloEstoque()

        elif modulo == '3':
            limpar_terminal(0.2)
            ModuloVendas() 

        elif modulo == '4':
            limpar_terminal()
            print("Saindo do Sistema...")
            limpar_terminal(1)
            break           

        else:
            limpar_terminal()
            print("Escolha um modulo ja existente!")
            limpar_terminal(1)

Home()
            
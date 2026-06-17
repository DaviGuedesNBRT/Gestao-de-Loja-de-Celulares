from usuarios import ModuloClientes
from ultils import limpar_terminal
from estoque import ModuloEstoque
from vendas import ModuloVendas
from time import sleep


def Home():
    while True:
        limpar_terminal()
        print("""
    =========-HOME-=========
        1 - Gerir Clientes
        2 - Gerir Estoque
        3 - Gerir Vendas
    ========================
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

        else:
            limpar_terminal()
            print("Escolha um modulo ja existente!")
            limpar_terminal(1)

Home()
            
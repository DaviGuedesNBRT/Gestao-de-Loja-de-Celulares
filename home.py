import os
import usuarios


def limpar_terminal():
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para Linux ou Mac
    else:
        os.system("clear")


def Home():
    while True:
        print("""
        ======================
        1 - Gerir Clientes
        2 - Gerir Estoque
        3 - Gerir Vendas
        =======================
        """)

        modulo = input("qual modulo você deseja acessar ? :")

        if modulo == '1':
            limpar_terminal()
            usuarios.ModuloClientes()
            

        elif modulo == '2':
            pass

        elif modulo == '3':
            pass

        else:
            limpar_terminal()
            print("Escolha um modulo ja existente!")
            
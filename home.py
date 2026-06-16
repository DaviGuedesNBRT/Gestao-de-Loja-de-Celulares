import os
import usuarios
from estoque import ModuloEstoque
from time import sleep


def limpar_terminal():
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para Linux ou Mac
    else:
        os.system("clear")


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
            limpar_terminal()
            usuarios.ModuloClientes()
            

        elif modulo == '2':
            limpar_terminal()
            ModuloEstoque()

        elif modulo == '3':
            limpar_terminal()
            print("Ops! O Modulo Ainda Não Está Fancionando, Mas Em Breve Estará Disponivel!!!")
            sleep(2)
            

        else:
            limpar_terminal()
            print("Escolha um modulo ja existente!")

Home()
            
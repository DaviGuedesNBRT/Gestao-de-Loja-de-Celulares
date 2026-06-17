import json
import os
from time import sleep

def limpar_terminal(tempo=0):
    # Para Windows
    if os.name == "nt":
        sleep(tempo)
        os.system("cls")
    # Para Linux ou Mac
    else:
        sleep(tempo)
        os.system("clear")


def atualizar_arquivos(produtos = None, clientes = None, vendas = None):
    if produtos is not None:
        with open("estoque.json", "w", encoding="utf-8") as arquivo:
            json.dump(produtos, arquivo, indent=4, ensure_ascii=False)

    else:
        pass
    
    if clientes is not None:
        with open("clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

    else:
        pass

    if vendas is not None:
        with open("vendas.json", "w", encoding="utf-8") as arquivo:
            json.dump(vendas, arquivo, indent=4, ensure_ascii=False)

    else:
        pass


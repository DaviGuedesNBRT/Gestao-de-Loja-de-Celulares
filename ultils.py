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

import json

def atualizar_arquivos(produtos=None, clientes=None, vendas=None, contador=None):
    if produtos is not None:
        with open("banco/estoque.json", "w", encoding="utf-8") as arquivo:
            json.dump(produtos, arquivo, indent=4, ensure_ascii=False)

    if clientes is not None:
        with open("banco/clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

    if vendas is not None:
        with open("banco/vendas.json", "w", encoding="utf-8") as arquivo:
            json.dump(vendas, arquivo, indent=4, ensure_ascii=False)

    if contador is not None:
        with open("banco/contador.json", "w", encoding="utf-8") as arquivo:
            json.dump(contador, arquivo, indent=4, ensure_ascii=False)

def CriarArquivos():
        
    if not os.path.exists("banco"):
        os.makedirs("banco")

    if not os.path.exists("banco/clientes.json") and not os.path.exists("banco/contador.json") and not os.path.exists("banco/estoque.json") and os.path.exists("banco/vendas.json"):
        with open("banco/clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False) 

        with open("banco/vendas.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False)

        with open("banco/estoque.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False) 

        with open("banco/contador.json", "w", encoding="utf-8") as arquivo:
            json.dump({"cont_clientes": 0, "cont_estoque": 0, "cont_vendas" :0}, arquivo, indent=4, ensure_ascii=False)

    if not os.path.exists("banco/clientes.json"):
        with open("banco/clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False) 

    if not os.path.exists("banco/vendas.json"):
        with open("banco/vendas.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False)

    if not os.path.exists("banco/estoque.json"):
        with open("banco/estoque.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False)


    elif not os.path.exists("banco/contador.json"):
        if os.path.exists("banco/clientes.json"):
            os.remove("banco/clientes.json")

        if os.path.exists("banco/vendas.json"):
            os.remove("banco/vendas.json")

        if os.path.exists("banco/estoque.json"):
            os.remove("banco/estoque.json")
        
        with open("banco/clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False)

        with open("banco/vendas.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False)

        with open("banco/estoque.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False) 

        with open("banco/contador.json", "w", encoding="utf-8") as arquivo:
            json.dump({"cont_clientes": 0, "cont_estoque": 0, "cont_vendas" :0}, arquivo, indent=4, ensure_ascii=False)


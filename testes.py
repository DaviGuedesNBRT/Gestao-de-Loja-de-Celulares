import json


def salvarClientes(clientes):
    with open("clientes.json", "w", encoding="utf-8") as arquivo:
        json.dump(clientes, arquivo, indent=4, ensure_ascii=False)


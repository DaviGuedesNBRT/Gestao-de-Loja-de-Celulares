import json
import os
from time import sleep
from datetime import date

def limpar_terminal(tempo=0):
    # Para Windows
    if os.name == "nt":
        sleep(tempo)
        os.system("cls")
    # Para Linux ou Mac
    else:
        sleep(tempo)
        os.system("clear")

def atualizar_arquivos(produtos=None, clientes=None, vendas=None):
    if produtos is not None:
        with open("banco/estoque.json", "w", encoding="utf-8") as arquivo:
            json.dump(produtos, arquivo, indent=4, ensure_ascii=False)

    if clientes is not None:
        with open("banco/clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

    if vendas is not None:
        with open("banco/vendas.json", "w", encoding="utf-8") as arquivo:
            json.dump(vendas, arquivo, indent=4, ensure_ascii=False)

def CriarArquivos():
        
    if not os.path.exists("banco"):
        os.makedirs("banco")

    if not os.path.exists("banco/clientes.json"):
        with open("banco/clientes.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False) 

    if not os.path.exists("banco/vendas.json"):
        with open("banco/vendas.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False)

    if not os.path.exists("banco/estoque.json"):
        with open("banco/estoque.json", "w", encoding="utf-8") as arquivo:
            json.dump({}, arquivo, indent=4, ensure_ascii=False)

def adicionar_produto_carrinho(venda_id, produtos, produtos_vendidos):
    if venda_id in produtos:
        quantidade = int(input("Informe a quantidade de produtos: "))

        while produtos[venda_id]["quantidade"] < quantidade:
            print(f"\nA quantidade excedeu o estoque! Estoque máximo atual: {produtos[venda_id]['quantidade']}")
            quantidade = int(input("Informe uma quantidade válida: "))

        produtos[venda_id]["quantidade"] -= quantidade
        produto_comprado = {
            "id": venda_id,
            "quantidade": quantidade,
            "preco_unitario": produtos[venda_id]["preco"]
        }
        produtos_vendidos.append(produto_comprado)

        print("\nProduto adicionado ao carrinho!")
        sleep(1)
        limpar_terminal()

        return produtos[venda_id]["preco"] * quantidade
    else:
        print("ID selecionado inválido.")
        sleep(1.5)
        limpar_terminal()
        return 0 
    
def RealizarVenda(venda_realizada=False, pagamento=0.0, cpf_cliente='', vendas={}, produtos={}, clientes={}, prazo=True, produtos_vendidos=None):    
    if produtos_vendidos is None:
        produtos_vendidos = []

    while not venda_realizada:               
        print(f"""
    ====-FORMAS DE PAGAMENTO-====
    Valor Total: R${pagamento:.2f}
    -----------------------------
        1 - Pix
        2 - A Vista (Espécie)
        3 - A Vista (Cartão)
        4 - Parcelado
        {"5 - A Prazo" if prazo else ""}
    =============================
            """)
        
        forma_pagamento = input("Informe o método de pagamento: ").strip()   
        hoje = date.today().isoformat()
        nome_metodo = ""

        if forma_pagamento == '1':
            nome_metodo = "Pix"
        elif forma_pagamento == '2':
            nome_metodo = "A Vista (Espécie)"
        elif forma_pagamento == '3':
            nome_metodo = "A Vista (Cartão)"
        elif forma_pagamento == '4':
            nome_metodo = "Parcelado"
        elif forma_pagamento == '5' and prazo: # Corrigido: aceita se prazo for True
            nome_metodo = "A Prazo"
        else:
            print("Opção inválida!")
            sleep(1)
            limpar_terminal()
            continue 
        
        # Se for "A Prazo", aumenta a dívida do cliente
        if nome_metodo == "A Prazo":
            tipo_venda = "Venda a Prazo (Dívida)"
            for id_cli, dados_cli in clientes.items():
                if dados_cli["cpf"] == cpf_cliente:
                    clientes[id_cli]["saldo_devedor"] += float(pagamento)
                    print(f"Saldo devedor de {dados_cli['nome']} atualizado para: R${clientes[id_cli]['saldo_devedor']:.2f}")
                    sleep(2)
                    break
        else:
            tipo_venda = "Venda de produto"

        venda_atual = {
            "cpf_cliente": cpf_cliente, 
            "valor_venda": pagamento,
            "forma_pagamento": nome_metodo, 
            "tipo_venda": tipo_venda,
            "data": hoje,
            "ID_produtos_vendidos": produtos_vendidos
        }
        id_venda = len(vendas)
        id_venda += 1 

        vendas[str(id_venda)] = venda_atual
        atualizar_arquivos(produtos=produtos, vendas=vendas, clientes=clientes)
        
        print("\nVenda registrada com sucesso!")
        sleep(1.5)
        limpar_terminal()
        venda_realizada = True
        

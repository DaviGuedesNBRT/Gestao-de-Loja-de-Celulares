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

        if produtos[venda_id]["quantidade"] > 0:
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
            print("quantidade do produto zerada no estoque")
            limpar_terminal(1.5)
            return 0

    else:
        print("ID selecionado inválido.")
        limpar_terminal(1.5)
        return 0 

def RealizarVenda(venda_realizada=False, pagamento=0.0, cpf_cliente='', vendas={}, produtos={}, clientes={}, prazo=False, produtos_vendidos=None):    
    with open("banco/clientes.json", "r", encoding="utf-8") as arquivo:
        clientes = json.load(arquivo)
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
        tipo_venda = ""

        if forma_pagamento == '1':
            nome_metodo = "Pix"
            tipo_venda = "Venda de produto"
        elif forma_pagamento == '2':
            nome_metodo = "A Vista (Espécie)"
            tipo_venda = "Venda de produto"
        elif forma_pagamento == '3':
            nome_metodo = "A Vista (Cartão)"
            tipo_venda = "Venda de produto"
        elif forma_pagamento == '4':
            nome_metodo = "Parcelado"
            tipo_venda = "Venda de produto"
        elif forma_pagamento == '5' and prazo:
            nome_metodo = "A Prazo"
            tipo_venda = "Venda a Prazo (Dívida)"
            if cpf_cliente in clientes:
                clientes[cpf_cliente]["saldo_devedor"] += float(pagamento)
                print(f"Saldo devedor de {clientes[cpf_cliente]['nome']} atualizado para: R${clientes[cpf_cliente]['saldo_devedor']:.2f}")
                sleep(2)
        else:
            print("Opção inválida!")
            sleep(1)
            limpar_terminal()
            continue 

        # Pagamento de dívida (quando não é venda a prazo)
        if nome_metodo != "A Prazo":
            if cpf_cliente in clientes and clientes[cpf_cliente]["saldo_devedor"] > 0:
                tipo_venda = "Pagamento de Dívida"
                print(f"Saldo devedor de {clientes[cpf_cliente]['nome']} foi atualizado de R${clientes[cpf_cliente]['saldo_devedor']:.2f}")
                clientes[cpf_cliente]["saldo_devedor"] -= float(pagamento)
                print(f"Para: R${clientes[cpf_cliente]['saldo_devedor']:.2f}")
                limpar_terminal(2)

        # Registrar venda
        venda_atual = {
            "cpf_cliente": cpf_cliente, 
            "valor_venda": pagamento,
            "forma_pagamento": nome_metodo, 
            "tipo_venda": tipo_venda,
            "data": hoje,
            "ID_produtos_vendidos": produtos_vendidos
        }
        id_venda = len(vendas) + 1
        vendas[str(id_venda)] = venda_atual
        atualizar_arquivos(produtos=produtos, vendas=vendas, clientes=clientes)
        
        print("\nVenda registrada com sucesso!")
        sleep(1.5)
        limpar_terminal()
        return True

def mostrar_vendas(vendas_filtradas,clientes):
    if not vendas_filtradas:
        print("Nenhuma venda encontrada.")
        sleep(2)
        limpar_terminal()
        return

    print(f"{'ID':<5}| {'CPF Cliente':<15}| {'Nome Cliente':<20}| {'Valor (R$)':>10}| {'Forma':<15}| {'Data':<12}| {'Tipo':<20}")
    print("-" * 120)

    for id_venda, dados in vendas_filtradas.items():
        cpf = dados['cpf_cliente']
        nome_cliente = clientes.get(cpf, {}).get("nome", "N/D")  # busca no dicionário de clientes
        print(f"{id_venda:<5}| {cpf:<15}| {nome_cliente:<20}| "
            f"{dados['valor_venda']:>10.2f}| {dados['forma_pagamento']:<15}| {dados['data']:<12}| {dados['tipo_venda']:<20}")

    print("-" * 120)
    input("\nPressione ENTER para continuar...")
    limpar_terminal()

def validar_formatar_cpf(cpf: str) -> str:
    """
    Valida se o CPF tem 11 dígitos numéricos e retorna formatado: XXX.XXX.XXX-XX
    """
    cpf = ''.join(filter(str.isdigit, cpf))  # remove tudo que não for número
    if len(cpf) != 11:
        raise ValueError("CPF inválido. Deve conter 11 dígitos numéricos.")
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def validar_formatar_telefone(telefone: str) -> str:
    """
    Valida se o telefone tem entre 10 e 11 dígitos e retorna formatado: (XX) XXXXX-XXXX
    """
    telefone = ''.join(filter(str.isdigit, telefone))
    if len(telefone) not in (10, 11):
        raise ValueError("Telefone inválido. Deve conter 10 ou 11 dígitos numéricos.")

    ddd = telefone[:2]
    if len(telefone) == 10:
        return f"({ddd}) {telefone[2:6]}-{telefone[6:]}"
    else:  # 11 dígitos → celular
        return f"({ddd}) {telefone[2:7]}-{telefone[7:]}"

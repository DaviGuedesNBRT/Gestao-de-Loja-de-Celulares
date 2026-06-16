import json 
from time import sleep
import os
import usuarios
from datetime import datetime

vendas = []
clientes = []
produtos = []

def limpar_terminal():
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para Linux ou Mac
    else:
        os.system("clear")



if os.path.exists("estoque.json"):
    with open("estoque.json", "r", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)

else:
    with open("estoque.json", "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, indent=4, ensure_ascii=False)  


if os.path.exists("clientes.json"):
    with open("clientes.json", "r", encoding="utf-8") as arquivo:
        clientes = json.load(arquivo)

else:
    with open("clientes.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, indent=4, ensure_ascii=False)  


if os.path.exists("vendas.json"):
    with open("vendas.json", "r", encoding="utf-8") as arquivo:
        vendas = json.load(arquivo)

else:
    with open("vendas.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, indent=4, ensure_ascii=False)  



def ModuloVendas():
    while True:
        print('''
            ====================
            1 - Efetuar Venda
            2 - Visualizar vendas
            3 - Voltar Para Home
            =====================
            ''')
            
        opcao = input("Qual Opção Você Deseja acessar ? : ")

        if opcao == '1':
            pass

        elif opcao == '2':
            pass

        elif opcao == '3':
            sleep(1)
            limpar_terminal()
            break
        
        else:
            print('opção invalida!!')


def efetuarVenda():
    while True:
        cpf_venda = input('CPF Do Comprador :')
        cpf_encontrado = False

        for i,clientes in enumerate(clientes):
            if cpf_venda == clientes[i]["cpf"]:
                cpf_encontrado = True
        
        if not cpf_venda:
            print('CPF não encontrado, por favor cadastre-o!')
            sleep(2)
            limpar_terminal()
            usuarios.CadastrarCliente()

        produtos_vendidos = []
        valor_venda = 0

        while True:
            limpar_terminal()
            print("deixe o campo vazil para sair")
            nome_produto = input("informe o nome do produto :")

            if nome_produto == '':
                limpar_terminal()
                break

            encontrado = False
            for i, produto in enumerate(produtos):
                if produtos[i]["nome"] == nome_produto:
                    print(f"""
                        ID: {i+1}, Nome: {produto['nome']},
                        Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
                        Cor: {produto['cor']}
                    """)
                    print("================================================================")
                    print()
                    encontrado = True

                    venda = int(input("infome o ID do produto a ser vendido"))
                    quantidade = int(input("informe a quantidade de produtos : "))

                    while produtos[i][quantidade] < quantidade:
                        print("a quantidade de produtos da venda execeu o estoque!")
                        sleep(0.3)
                        print(f"por favor, efetue uma venda com no maximo {produtos[i][quantidade]}")

                        quantidade = int(input("informe a quantidade de produtos : "))

                    produtos[venda]["quantidade" - quantidade ]
                    produtos_vendidos.append(produtos[venda-1])
                    valor_venda += produtos[venda]["valor"]*quantidade
                    sleep(0.3)
                    limpar_terminal()

                    break

            if not encontrado:
                print("Produto Não Encontrado!")
                sleep(1)
                limpar_terminal()

        while True:
                
            print("""
                ====-FORMAS DE PAGAMENTO-====
                1 - pix
                2 - A vista(Éspecie)
                3 - A Vista(Cartão)
                4 - Parcelado
                5 - A prazo
                =============================
    """)
            forma_pagamento = input("Infome o metodo de pagamento : ")   
            if forma_pagamento == '1':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "Pix",
                         "produtos_vendidos": produtos_vendidos
                         }
                
                vendas.append(venda)
                with open("vendas.json", "r", encoding="utf-8") as arquivo:
                    vendas = json.load(arquivo)


            elif forma_pagamento == '2':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "A Vista(Éspecie)",
                         "produtos_vendidos": produtos_vendidos
                         }
                
                vendas.append(venda)
                with open("vendas.json", "r", encoding="utf-8") as arquivo:
                    vendas = json.load(arquivo)


            elif forma_pagamento == '3':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "A Vista(cartão)",
                         "produtos_vendidos": produtos_vendidos
                         }
                
                vendas.append(venda)
                with open("vendas.json", "r", encoding="utf-8") as arquivo:
                    vendas = json.load(arquivo)


            elif forma_pagamento == '4':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "Parcelado",
                         "produtos_vendidos": produtos_vendidos
                         }
                
                vendas.append(venda)
                with open("vendas.json", "r", encoding="utf-8") as arquivo:
                    vendas = json.load(arquivo)


            elif forma_pagamento == '5':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "A Prazo",
                         "produtos_vendidos": produtos_vendidos
                         }
                
                for i in enumerate(clientes):
                    if cpf_venda == clientes[i]["cpf"]:
                        pass

                vendas.append(venda)
                with open("vendas.json", "r", encoding="utf-8") as arquivo:
                    vendas = json.load(arquivo)

            else :
                print("opção invalida!")
                sleep(0.3)
                limpar_terminal()
        pass

def visualizarVendas():
    pass
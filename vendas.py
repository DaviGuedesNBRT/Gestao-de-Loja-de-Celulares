import json 
from ultils import limpar_terminal, atualizar_arquivos
from time import sleep
import os
import usuarios
from datetime import date

vendas = []
clientes = []
produtos = []


with open("estoque.json", "r", encoding="utf-8") as arquivo:
    produtos = json.load(arquivo)

with open("clientes.json", "r", encoding="utf-8") as arquivo:
    clientes = json.load(arquivo)

if not os.path.exists("vendas.json"):
    with open("vendas.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, indent=4, ensure_ascii=False)  
else:
    with open("vendas.json", "r", encoding="utf-8") as arquivo:
        vendas = json.load(arquivo)


def ModuloVendas():
    while True:
        print('''
    ============================
        1 - Efetuar Venda
        2 - Visualizar vendas
        3 - Voltar Para Home
    ============================
            ''')
            
        opcao = input("Qual Opção Você Deseja acessar ? : ")
        limpar_terminal(0.1)

        if opcao == '1':
            efetuarVenda()

        elif opcao == '2':
            pass

        elif opcao == '3':
            break
        
        else:
            print('opção invalida!!')
            limpar_terminal(1)


def efetuarVenda():
    global clientes
    global produtos
    global vendas

    venda_realizada = False
    while not venda_realizada:
        cpf_venda = input('CPF Do Comprador :').strip()
        cpf_encontrado = False
        

        for i,cliente in enumerate(clientes):
            if cpf_venda == str(clientes[i]["cpf"]).strip():
                cpf_encontrado = True
        
        if not cpf_encontrado:
            print('CPF não encontrado, por favor cadastre-o!')
            limpar_terminal(2)
            cpf_venda = usuarios.CadastrarCliente()

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
                if nome_produto in produtos[i]["nome"]:
                    print(f"""
            ID: {i+1}, Nome: {produto['nome']},
            Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
            Cor: {produto['cor']}, Quantidade: {produto["quantidade"]}
            ================================================================
                    """)
                    print()
                    encontrado = True

            if encontrado:
                venda_id = int(input("infome o ID do produto a ser vendido"))
                quantidade = int(input("informe a quantidade de produtos : "))

                while produto["quantidade"] < quantidade:
                    limpar_terminal(0.25)
                    print("a quantidade de produtos da venda execeu o estoque!")
                    limpar_terminal(0.5)
                    print(f"por favor, efetue uma venda com no maximo {produtos[venda_id-1]["quantidade"]}")

                    quantidade = int(input("informe a quantidade de produtos : "))
                    limpar_terminal(0.25)

                produtos[venda_id-1]["quantidade"] - quantidade

                produtos_comprados = produtos[venda_id-1].copy()
                produtos_comprados["quantidade"] = quantidade

                produtos_vendidos.append(produtos_comprados)
                valor_venda += produtos[venda_id-1]["preco"]*quantidade

                limpar_terminal(0.3)

                atualizar_arquivos(produtos=produtos)

            else:
                print("Produto Não Encontrado!")
                limpar_terminal(1)

        while not venda_realizada:               
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
            hoje = date.today().isoformat()

            if forma_pagamento == '1':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "Pix", "data" : hoje,
                         "produtos_vendidos": produtos_vendidos
                         }
                
                vendas.append(venda)
                venda_realizada = True

            elif forma_pagamento == '2':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "A Vista(Éspecie)", "data" : hoje,
                         "produtos_vendidos": produtos_vendidos
                         }
                
                vendas.append(venda)
                venda_realizada = True

            elif forma_pagamento == '3':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "A Vista(cartão)", "data" : hoje,
                         "produtos_vendidos": produtos_vendidos
                         }                
                vendas.append(venda)
                venda_realizada = True

            elif forma_pagamento == '4':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "Parcelado", "data" : hoje,
                         "produtos_vendidos": produtos_vendidos
                         }                
                vendas.append(venda)
                venda_realizada = True

            elif forma_pagamento == '5':
                venda = {"cpf_cliente":cpf_venda, "valor_venda": valor_venda,
                         "forma_pagamento" : "A Prazo", "data" : hoje,
                         "produtos_vendidos": produtos_vendidos
                         }
                
                for i ,cliente in enumerate(clientes):
                    if cpf_venda == clientes[i]["cpf"]:
                        clientes[i]["saldo_devedor"] += float(valor_venda)
                        atualizar_arquivos(clientes=clientes)

                        print(f"Saldo devedor do cliente :{clientes[i]["nome"]} foi atualizado para : {clientes[i]["saldo_devedor"]}")
                        limpar_terminal(1)

                vendas.append(venda)
                venda_realizada = True
            else :
                print("opção invalida!")
                sleep(0.3)
                limpar_terminal()

            #atualiza todos os arquivos de uma vez
            atualizar_arquivos(produtos=produtos, vendas=vendas, clientes=clientes)
            
            print("venda realizada com sucesso!")
            sleep(10)
            sair = input("pressione enter para sair")



def visualizarVendas():
    pass
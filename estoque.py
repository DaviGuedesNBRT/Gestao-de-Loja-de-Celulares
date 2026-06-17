from time import sleep
from ultils import limpar_terminal, atualizar_arquivos
import os
import json

produtos = []

if not os.path.exists("estoque.json"):
    with open("estoque.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, indent=4, ensure_ascii=False)  
else:
    with open("estoque.json", "r", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)


def ModuloEstoque():
    while True:
        limpar_terminal()
        print("""
        ======================
        1 - Cadastrar Produto
        2 - Atualizar Produto
        3 - Excluir Produto
        4 - Visualizar Produto
        5 - Visualizar Produtos
        6 - Voltar para o Menu Principal
        =======================
        """)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            sleep(0.25)
            limpar_terminal()
            salvarProdutos()

        elif opcao == '2':
            sleep(0.25)
            limpar_terminal()
            processarProduto(atualizar=True)

        elif opcao == '3':
            sleep(0.25)
            limpar_terminal()
            processarProduto(excluir=True)

        elif opcao == '4':
            sleep(0.25)
            limpar_terminal()
            processarProduto()

        elif opcao == '5':
            sleep(0.25)
            limpar_terminal()
            carregarProdutos()

        elif opcao == '6':
            limpar_terminal()
            break

        else:
            limpar_terminal()
            print("Opção inválida. Por favor, escolha uma opção válida.")
            sleep(1)
            limpar_terminal()


def salvarProdutos():
    print("Cadastrar Produto, Se Não houver Informação Para o Campo, deixe em branco!")
    print()

    nome_produto = input("Digite o nome do produto: ")
    marca_produto = input("Digite a marca do produto: ")
    preco_produto = float(input("Digite o preço do produto: "))
    cor_produto = input("Digite a cor do produto: ")
    quantidade_produto = int(input("Digite a quantidade do produto: "))

    produto = {
        "nome": nome_produto,
        "marca": marca_produto,
        "preco": preco_produto,
        "cor": cor_produto,
        "quantidade": quantidade_produto
    }

    produtos.append(produto)
    with open("estoque.json", "w", encoding="utf-8") as arquivo:
        json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
    
    print("Produto cadastrado com sucesso!")
    sleep(1)
    limpar_terminal()

def carregarProdutos():
    while True:
        print("""
            ======================
            1 - Visualizar Todos os Produtos
            2 - visualizar produtos Disponiveis
            3 - visualizar produtos Indisponiveis
            4 - Voltar Para o Menu Anterior
            ======================
            """)
        
        opcao = input("Escolha uma opção: ")
        print()
        limpar_terminal()

        if opcao == '1':
            encontrado = False
            for i, produto in enumerate(produtos):
                print(f"""
                    ID: {i+1}, Nome: {produto['nome']},
                    Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
                    Cor: {produto['cor']}, Quantidade: {produto['quantidade']}
                """)
                print("================================================================")
                print()
                encontrado = True
            
            if not encontrado:
                print("Nenhum Resultado Encontrado Para a Busca!")

            sair = input("\nPrecione Enter Para Voltar ao Menu...")
            limpar_terminal()
        
        elif opcao == '2':
            encontrado = False
            for i, produto in enumerate(produtos):
                if produto["quantidade"] > 0:
                    print(f"""
                    ID: {i+1}, Nome: {produto['nome']},
                    Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
                    Cor: {produto['cor']}, Quantidade: {produto['quantidade']}
                """)
                print("================================================================")
                print()
                encontrado = True
            
            if not encontrado:
                print("Nenhum Resultado Encontrado Para a Busca!")

            sair = input("\nPrecione Enter Para Voltar ao Menu...")
            limpar_terminal()


        elif opcao == '3':
            encontrado = False
            for i, produto in enumerate(produtos):
                if produto["quantidade"] <= 0:
                    print(f"""
                    ID: {i+1}, Nome: {produto['nome']},
                    Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
                    Cor: {produto['cor']}, Quantidade: {produto['quantidade']}
                """)
                print("================================================================")
                print()
                encontrado = True

            if not encontrado:
                print("Nenhum Resultado Encontrado Para a Busca!")
            
            sair = input("\nPrecione Enter Para Voltar ao Menu...")
            limpar_terminal()

        
        elif opcao == '4':
            break
        

def processarProduto(excluir=False, atualizar=False):
    while True:
        if excluir:
            prompt = "Digite o Nome do Produto para Exclusão: "
        elif atualizar:
            prompt = "Digite o Nome do Produto para Atualização: "
        else:
            prompt = "Digite o Nome do Produto para Visualizar: "

        nome_produto = input(prompt)

        if not excluir and not atualizar:
            encontrado = False
            for i, produto in enumerate(produtos):
                if produtos[i]["nome"] == nome_produto:
                    print(f"""
                        ID: {i+1}, Nome: {produto['nome']},
                        Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
                        Cor: {produto['cor']}, Quantidade: {produto['quantidade']}
                    """)
                    print("================================================================")
                    print()
                    encontrado = True

            if not encontrado:
                print("Produto Não Encontrado!")
                sleep(2)
                limpar_terminal()
                break

            break

        elif excluir:
            encontrado = False
            for i, produto in enumerate(produtos):
                if produtos[i]["nome"] == nome_produto:
                    print(f"""
                        ID: {i+1}, Nome: {produto['nome']},
                        Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
                        Cor: {produto['cor']}, Quantidade: {produto['quantidade']}
                    """)
                    print("================================================================")
                    print()
                    encontrado = True

            if not encontrado:
                print("Produto Não Encontrado!")
                sleep(2)
                limpar_terminal()
                break

            else:
                excluir_produto = int(input("Digite o ID do Produto a Ser excluido :"))
                produtos.pop(excluir_produto-1)

                with open("estoque.json", "w", encoding="utf-8") as arquivo:
                    json.dump(produtos, arquivo, indent=4, ensure_ascii=False)  
                break

        elif atualizar:
            encontrado = False
            for i, produto in enumerate(produtos):
                if produtos[i]["nome"] == nome_produto:
                    print(f"""
                        ID: {i+1}, Nome: {produto['nome']},
                        Marca: {produto['marca']}, Preço: R${produto['preco']:.2f},
                        Cor: {produto['cor']}, Quantidade: {produto['quantidade']}
                    """)
                    print("================================================================")
                    print()
                    encontrado = True

            if not encontrado:
                print("Produto Não Encontrado!")
                sleep(2)
                limpar_terminal()
                break

            else:
                atualizar_produto= int(input("Digite o ID do Produto a Ser Atualizado :"))-1
                sleep(0.25)
                limpar_terminal()
                print(atualizar_produto)

                if 0<= atualizar_produto < len(produtos):

                    print("Atualizar Produto, se não houver informação para o campo, deixe em branco!\n")

                    produto = produtos[atualizar_produto]

                    nome_produto = input(f"Digite o nome do produto ({produto['nome']}): ") or produto['nome']
                    marca_produto = input(f"Digite a marca do produto ({produto['marca']}): ") or produto['marca']

                    preco_input = input(f"Digite o preço do produto ({produto['preco']}): ")
                    preco_produto = float(preco_input) if preco_input else produto['preco']

                    cor_produto = input(f"Digite a cor do produto ({produto['cor']}): ") or produto['cor']

                    quantidade_input = input(f"Digite a quantidade do produto ({produto['quantidade']}): ")
                    quantidade_produto = int(quantidade_input) if quantidade_input else produto['quantidade']

                    produto = {
                        "nome": nome_produto,
                        "marca": marca_produto,
                        "preco": preco_produto,
                        "cor": cor_produto,
                        "quantidade": quantidade_produto
                    }

                    produtos[atualizar_produto] = produto
                    with open("estoque.json", "w", encoding="utf-8") as arquivo:
                        json.dump(produtos, arquivo, indent=4, ensure_ascii=False)
                
                print("Produto Atualizado Com Sucesso!")
                sleep(1)
                limpar_terminal()
                break



            

                


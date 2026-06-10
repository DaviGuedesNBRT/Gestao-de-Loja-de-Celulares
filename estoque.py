from home import limpar_terminal
from time import sleep
import os
import json

produtos = []

if os.path.exists("estoque.json"):
    with open("estoque.json", "r", encoding="utf-8") as arquivo:
        produtos = json.load(arquivo)
else:
    with open("estoque.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, indent=4, ensure_ascii=False)  
        produtos = json.load(arquivo)


def ModuloEstoque():
    while True:
        print("""
        ======================
        1 - Cadastrar Produto
        2 - Atualizar Produto
        3 - Excluir Produto
        4 - Visualizar Produtos
        5 - Voltar para o Menu Principal
        =======================
        """)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            pass

        elif opcao == '2':
            pass

        elif opcao == '3':
            pass

        elif opcao == '4':
            pass

        elif opcao == '5':
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

            input = ("\nPrecione Enter Para Voltar ao Menu...")
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

            input = ("\nPrecione Enter Para Voltar ao Menu...")
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
            
            input = ("\nPrecione Enter Para Voltar ao Menu...")
            limpar_terminal()

        
        elif opcao == '4':
            break
        

def preocessarProduto(excluir = False, atualizar = False):
    while True:
        nome_produto = input(f"Digite o Nome do Produto Para {
            'para Exclusão : ' if excluir else 'para Atualização : ' if atualizar else 'Visualizar : '
        })

        
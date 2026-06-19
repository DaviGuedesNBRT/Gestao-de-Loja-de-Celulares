from ultils import limpar_terminal, atualizar_arquivos
import json

produtos = []
id_produto = 0

with open("banco/estoque.json", "r", encoding="utf-8") as arquivo:
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
            limpar_terminal(0.2)
            salvarProdutos()

        elif opcao == '2':
            limpar_terminal(0.2)
            processarProduto(atualizar=True)

        elif opcao == '3':
            limpar_terminal(0.2)
            processarProduto(excluir=True)

        elif opcao == '4':
            limpar_terminal(0.2)
            processarProduto()

        elif opcao == '5':
            limpar_terminal(0.2)
            carregarProdutos()

        elif opcao == '6':
            limpar_terminal(0.1)
            break

        else:
            limpar_terminal()
            print("Opção inválida. Por favor, escolha uma opção válida.")
            limpar_terminal(1)

def salvarProdutos():
    global id_produto, produtos
    
    print("Cadastrar Produto, Se Não houver Informação Para o Campo, deixe em branco!")
    print()

    nome_produto = input("Digite o nome do produto: ")
    marca_produto = input("Digite a marca do produto: ")
    armazenamento = input("Digite a quantidade de armazenamento (deixe em branco se nao tiver):") or " "
    preco_produto = float(input("Digite o preço do produto: "))
    cor_produto = input("Digite a cor do produto: ")
    quantidade_produto = int(input("Digite a quantidade do produto: "))

    id_produto += len(produtos)

    dados = {
        "nome": nome_produto,
        "marca": marca_produto,
        "armazenamento": armazenamento,
        "preco": preco_produto,
        "cor": cor_produto,
        "quantidade": quantidade_produto,
        "habilitado": True
    }

    produtos[str(id_produto)] = dados
    atualizar_arquivos(produtos=produtos)

    print("Produto cadastrado com sucesso!")
    limpar_terminal(1)

def carregarProdutos():
    while True:
        print("""
            ======================
            1 - Visualizar Todos os Produtos
            2 - Visualizar Produtos Disponíveis
            3 - Visualizar Produtos Indisponíveis
            4 - Voltar Para o Menu Anterior
            ======================
            """)
        
        opcao = input("Escolha uma opção: ")
        print()
        limpar_terminal()

        if opcao == '4':
            break

        if opcao not in ['1', '2', '3']:
            print("Opção inválida! Por favor, escolha uma opção válida.")
            limpar_terminal(1)
            continue

        # Define cabeçalho da tabela
        print("=" * 120)
        print(f"{'ID':<5} {'Nome':<20} {'Marca':<15} {'Armazenamento':<15} {'Preço':<12} {'Cor':<12} {'Quantidade':<10}")
        print("-" * 120)

        encontrado = False
        for id_produto, dados in produtos.items():
            # Filtro conforme opção
            if opcao == '1':
                incluir = True
            elif opcao == '2':
                incluir = dados["quantidade"] > 0
            else:  # opcao == '3'
                incluir = dados["quantidade"] <= 0

            if incluir:
                # Exibe uma linha da tabela
                print(f"{id_produto:<5} {dados['nome']:<20} {dados['marca']:<15} {dados['armazenamento']:<15} R$ {dados['preco']:<10.2f} {dados['cor']:<12} {dados['quantidade']:<10}")
                encontrado = True

        if not encontrado:
            limpar_terminal()
            print("Nenhum resultado encontrado para a busca!")

        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

def processarProduto(excluir=False, atualizar=False, rehabilitar=False):
    global produtos 
    
    while True:
        if excluir:
            prompt = "Digite o Nome do Produto para Exclusão: "
        elif atualizar:
            prompt = "Digite o Nome do Produto para Atualização: "
        elif rehabilitar:
            prompt = "Digite o Nome do Produto para Rehabilitar: "
        else:
            prompt = "Digite o Nome do Produto para Visualizar: "

        nome_busca = input(prompt).strip()
        if not nome_busca:
            print("O nome não pode ser vazio!")
            limpar_terminal(1)
            continue

        produtos_encontrados = {}

        for id_estoque, dados in produtos.items():
            if dados["nome"].lower() == nome_busca.lower() and dados.get("habilitado", True):
                produtos_encontrados[id_estoque] = dados

        if not produtos_encontrados:
            print("Produto Não Encontrado!")
            limpar_terminal(1)
            break

        print(f"\nForam encontrados {len(produtos_encontrados)} resultados:")

        print("-" * 100)
        print(f"{'ID':<5} {'Nome':<15} {'Marca':<12} {'Armazenamento':<15} {'Preço (R$)':>10} {'Cor':<10} {'Qtd':>5}")
        print("-" * 100)

        for id_estoque, dados in produtos_encontrados.items():
            print(f"{id_estoque:<5} {dados['nome']:<15} {dados['marca']:<12} {dados['armazenamento']:<15} {dados['preco']:>10.2f} {dados['cor']:<10} {dados['quantidade']:>5}")

        print("-" * 100)

        if not excluir and not atualizar:
            input("\nPressione Enter para continuar...")
            limpar_terminal()
            break
            
        if excluir:
            id_escolhido = input("\nDigite o ID do Produto desejado: ").strip()
            if id_escolhido in produtos_encontrados:
                produtos[id_escolhido]["habilitado"] = False
                atualizar_arquivos(produtos=produtos)   

                print("Produto Excluído Com Sucesso!")
                limpar_terminal(1)
                break

            else:
                print("ID inválido ou não correspondente à busca.")
                limpar_terminal(1) 

        elif atualizar:
            id_escolhido = input("\nDigite o ID do Produto desejado: ").strip()
            if id_escolhido in produtos_encontrados:                    
                print("Atualizar Produto, se não houver informação para o campo, deixe em branco!\n")
                produto_atualizar = produtos[id_escolhido]

                nome_produto = input(f"Digite o nome do produto ({produto_atualizar['nome']}): ") or produto_atualizar['nome']
                marca_produto = input(f"Digite a marca do produto ({produto_atualizar['marca']}): ") or produto_atualizar['marca']
                armazenamento = input(f"Digite o armazenamento ({produto_atualizar['armazenamento']}): ") or produto_atualizar['armazenamento']

                preco_input = input(f"Digite o preço do produto ({produto_atualizar['preco']}): ")
                preco_produto = float(preco_input) if preco_input else produto_atualizar['preco']

                cor_produto = input(f"Digite a cor do produto ({produto_atualizar['cor']}): ") or produto_atualizar['cor']

                quantidade_input = input(f"Digite a quantidade do produto ({produto_atualizar['quantidade']}): ")
                quantidade_produto = int(quantidade_input) if quantidade_input else produto_atualizar['quantidade']

                produtos[id_escolhido] = {
                    "nome": nome_produto,
                    "marca": marca_produto,
                    "armazenamento": armazenamento,
                    "preco": preco_produto,
                    "cor": cor_produto,
                    "quantidade": quantidade_produto
                }

                atualizar_arquivos(produtos=produtos)                
                print("Produto Atualizado Com Sucesso!")
                limpar_terminal(1)
                break
            else:
                print("ID inválido ou não correspondente à busca.")
                limpar_terminal(1)                


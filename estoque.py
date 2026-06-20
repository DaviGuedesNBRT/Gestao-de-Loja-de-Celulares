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
        ========================================
                        ESTOQUE
        ========================================
            1 - Cadastrar Produto
            2 - Atualizar Produto
            3 - Excluir Produto
            4 - Rehabilitar Produto
            5 - Visualizar Produto
            6 - Visualizar Produtos
            7 - Voltar para o Menu Principal
        ========================================
        """)

        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            limpar_terminal(0.2)
            salvarProdutos()

        elif opcao == '2':
            limpar_terminal(0.2)
            ProcessarProduto(atualizar=True)

        elif opcao == '3':
            limpar_terminal(0.2)
            ProcessarProduto(excluir=True)
        
        elif opcao == '4':
            limpar_terminal(0.2)
            ProcessarProduto(rehabilitar=True)

        elif opcao == '5':
            limpar_terminal(0.2)
            ProcessarProduto()

        elif opcao == '6':
            limpar_terminal(0.2)
            carregarProdutos()

        elif opcao == '7':
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
            ============================================
                        VISUALIZAR PRODUTOS
            ============================================
                1 - Visualizar Todos os Produtos
                2 - Visualizar Produtos Disponíveis
                3 - Visualizar Produtos Indisponíveis
                4 - Visualizar Produtos Desabilitados
                5 - Voltar Para o Menu Anterior
            ============================================
            """)
        
        opcao = input("Escolha uma opção: ").strip()
        print()
        limpar_terminal()

        if opcao == '5':
            break

        if opcao not in ['1', '2', '3', '4']:
            print("Opção inválida! Por favor, escolha uma opção válida.")
            limpar_terminal(1)
            continue

        # CORREÇÃO: Define se mostra a coluna "Status" (Opção 1 ou 4)
        mostrar_status = opcao in ['1', '4']
        coluna_status = f"| {'Status':<10}" if mostrar_status else ""

        # Cabeçalho da tabela adaptável
        print("=" * 120)
        print(f"{'ID':<5}| {'Nome':<20}| {'Marca':<15}| {'Armazenamento':<15}| {'Preço':>12}| {'Cor':<12}| {'Quantidade':<10}{coluna_status}")
        print("-" * 120)

        encontrado = False
        for id_produto, dados in produtos.items():
            incluir = False
            
            # Filtros ajustados
            if opcao == '1':
                incluir = True
            elif opcao == '2':
                incluir = dados["quantidade"] > 0 and dados.get("habilitado", True) != False
            elif opcao == '3':
                incluir = dados['quantidade'] <= 0 and dados.get("habilitado", True) != False
            elif opcao == '4':
                incluir = dados.get("habilitado") == False

            if incluir:
                # Tratando o texto do status (Ativo/Inativo) para ficar bonito na tabela
                status_texto = "Inativo" if dados.get("habilitado") == False else "Ativo"
                campo_status = f"| {status_texto:<10}" if mostrar_status else ""
                
                # Exibe a linha formatada (Preço alinhado à direita com '>')
                print(f"{id_produto:<5}| {dados['nome']:<20}| {dados['marca']:<15}| {dados['armazenamento']:<15}| R$ {dados['preco']:>9.2f}| {dados['cor']:<12}| {dados['quantidade']:^10}{campo_status}")
                encontrado = True

        if not encontrado:
            limpar_terminal()
            print("Nenhum resultado encontrado para a busca!")

        print("-" * 120)
        input("\nPressione Enter para voltar ao menu...")
        limpar_terminal()

def ProcessarProduto(excluir=False, atualizar=False, rehabilitar=False):
    global produtos 
    
    while True:
        if excluir:
            prompt = "Digite O Nome Do Produto Para Exclusão: "
        elif atualizar:
            prompt = "Digite O Nome Do Produto Para Atualização: "
        elif rehabilitar:
            prompt = "Digite O Nome Do Produto Para Reabilitar: "
        else:
            prompt = "Digite O Nome Do Produto Para Visualizar: "

        nome_busca = input(prompt).strip()
        if not nome_busca:
            print("O Nome Não Pode Ser Vazio!")
            limpar_terminal(1)
            continue

        produtos_encontrados = {}

        for id_estoque, dados in produtos.items():
            if nome_busca.lower() in dados["nome"].lower():
                # Se for reabilitar, pega só os inativos
                if rehabilitar and not dados.get("habilitado", True):
                    produtos_encontrados[id_estoque] = dados
                # Se não for reabilitar, pega só os ativos
                elif not rehabilitar and dados.get("habilitado", True):
                    produtos_encontrados[id_estoque] = dados

        if not produtos_encontrados:
            print("Produto Não Encontrado!")
            limpar_terminal(1)
            break

        print(f"\nForam Encontrados {len(produtos_encontrados)} Resultados:")

        print("-" * 110)
        print(f"{'ID':<5}| {'Nome':<25}| {'Marca':<17}| {'Armazenamento':<15}| {'Preço (R$)':>10}| {'Cor':<12}| {'Qtd':>5}")
        print("-" * 110)
        
        for id_estoque, dados in produtos_encontrados.items():
            print(f"{id_estoque:<5}| {dados['nome']:<25}| {dados['marca']:<17}| {dados['armazenamento']:<15}| "
                  f"{dados['preco']:>10.2f}| {dados['cor']:<12}| {dados['quantidade']:>5}")
        print("-" * 110)

        if not excluir and not atualizar and not rehabilitar:
            input("\nPressione Enter Para Continuar...")
            limpar_terminal()
            break
            
        if excluir:
            id_escolhido = input("\nDigite O ID Do Produto Desejado: ").strip()
            if id_escolhido in produtos_encontrados:
                limpar_terminal(0.5)
                produtos[id_escolhido]["habilitado"] = False
                atualizar_arquivos(produtos=produtos)   
                print("Produto Excluído Com Sucesso!")
                limpar_terminal(1)
                break
            else:
                limpar_terminal(0.5)
                print("ID Inválido Ou Não Correspondente À Busca.")
                limpar_terminal(1) 

        elif rehabilitar:
            id_escolhido = input("\nDigite O ID Do Produto Desejado: ").strip()
            if id_escolhido in produtos_encontrados:
                limpar_terminal(0.5)
                produtos[id_escolhido]["habilitado"] = True
                atualizar_arquivos(produtos=produtos)   
                print("Produto Reabilitado Com Sucesso!")
                limpar_terminal(1)
                break
            else:
                limpar_terminal(0.5)
                print("ID Inválido Ou Não Correspondente À Busca.")
                limpar_terminal(1)

        elif atualizar:
            id_escolhido = input("\nDigite O ID Do Produto Desejado: ").strip()
            if id_escolhido in produtos_encontrados:
                limpar_terminal(0.5)                    
                print("Atualizar Produto, Se Não Houver Informação Para O Campo, Deixe Em Branco!\n")
                produto_atualizar = produtos[id_escolhido]

                nome_produto = input(f"Digite O Nome Do Produto ({produto_atualizar['nome']}): ") or produto_atualizar['nome']
                marca_produto = input(f"Digite A Marca Do Produto ({produto_atualizar['marca']}): ") or produto_atualizar['marca']
                armazenamento = input(f"Digite O Armazenamento ({produto_atualizar['armazenamento']}): ") or produto_atualizar['armazenamento']

                preco_input = input(f"Digite O Preço Do Produto ({produto_atualizar['preco']}): ")
                preco_produto = float(preco_input) if preco_input else produto_atualizar['preco']

                cor_produto = input(f"Digite A Cor Do Produto ({produto_atualizar['cor']}): ") or produto_atualizar['cor']

                quantidade_input = input(f"Digite A Quantidade Do Produto ({produto_atualizar['quantidade']}): ")
                quantidade_produto = int(quantidade_input) if quantidade_input else produto_atualizar['quantidade']

                produtos[id_escolhido] = {
                    "nome": nome_produto,
                    "marca": marca_produto,
                    "armazenamento": armazenamento,
                    "preco": preco_produto,
                    "cor": cor_produto,
                    "quantidade": quantidade_produto,
                    "habilitado": True
                }

                atualizar_arquivos(produtos=produtos)
                limpar_terminal(0.5)                
                print("Produto Atualizado Com Sucesso!")
                limpar_terminal(1)
                break
            else:
                print("ID Inválido Ou Não Correspondente À Busca.")
                limpar_terminal(1)

                


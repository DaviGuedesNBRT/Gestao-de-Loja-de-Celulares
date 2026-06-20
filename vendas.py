import json 
from ultils import limpar_terminal, adicionar_produto_carrinho, RealizarVenda, mostrar_vendas
from time import sleep
from usuarios import CadastrarCliente
from datetime import date, datetime, timedelta

vendas = {}
clientes = {}
produtos = {}
id_venda = 0


with open("banco/estoque.json", "r", encoding="utf-8") as arquivo:
    produtos = json.load(arquivo)

with open("banco/clientes.json", "r", encoding="utf-8") as arquivo:
    clientes = json.load(arquivo)

with open("banco/vendas.json", "r", encoding="utf-8") as arquivo:
    vendas = json.load(arquivo)

def ModuloVendas():
    while True:
        print('''
    ============================
              VENDAS
    ============================
        1 - Efetuar Venda
        2 - Visualizar Vendas
        3 - Pagar Divida
        4 - Relatorio Financeiro
        5 - Voltar Para Home
    ============================
            ''')
            
        opcao = input("Qual Opção Você Deseja acessar ? : ")
        limpar_terminal(0.1)

        if opcao == '1':
            limpar_terminal()
            EfetuarVenda()

        elif opcao == '2':
            limpar_terminal()
            VisualizarVendas()

        elif opcao == '3':
            limpar_terminal()
            PagarPrazo()

        elif opcao == '4':
            limpar_terminal()
            RelatorioFinanceiro()

        elif opcao == '5':
            break
        
        else:
            print('opção invalida!!')
            limpar_terminal(1)

def EfetuarVenda():
    global clientes, produtos, vendas

    venda_realizada = False
    while not venda_realizada:
        cpf_venda = input("CPF Do Comprador: ").strip()

        # Verifica se o CPF existe diretamente como chave
        if cpf_venda not in clientes:
            print("CPF Não Encontrado, Por Favor Cadastre-O!")
            sleep(2)
            limpar_terminal()
            cpf_venda = CadastrarCliente() 

        produtos_vendidos = []
        valor_venda = 0

        # Loop de compras
        while True:
            print("""
        ===============================================
                        Formas De Busca     
        ================================================
            1 - Buscar Por ID Do Produto
            2 - Buscar Por Nome Do Produto
            3 - Finalizar Compra (Ir Para Pagamento)
        ================================================
            """)
            busca = input("Qual A Forma De Busca? : ")

            if busca == '3':
                limpar_terminal()
                break  # Sai do loop de busca e vai para o pagamento

            elif busca == '1':
                while True:
                    limpar_terminal()
                    print("Deixe O Campo Vazio Para Voltar Ao Menu De Busca")
                    venda_id = input("Informe O ID Do Produto A Ser Vendido: ").strip()

                    if venda_id == "":
                        limpar_terminal()
                        break

                    valor_venda += adicionar_produto_carrinho(venda_id, produtos, produtos_vendidos)

            elif busca == '2':
                while True:
                    limpar_terminal()
                    print("Deixe O Campo Vazio Para Voltar Ao Menu De Busca")
                    nome_produto = input("Informe O Nome Do Produto: ").strip()

                    if nome_produto == "":
                        limpar_terminal()
                        break

                    produtos_encontrados = {}
                    for id_prod, dados_prod in produtos.items():
                        if nome_produto.lower() in dados_prod["nome"].lower() and dados_prod["quantidade"] > 0:
                            produtos_encontrados[id_prod] = dados_prod

                    if produtos_encontrados:
                        print(f"\nForam Encontrados {len(produtos_encontrados)} Resultados:")
                        print("-" * 90)
                        print(f"{'ID':<5}| {'Nome':<20}| {'Marca':<12}| {'Preço (R$)':>10}| {'Cor':<10}| {'Estoque':>8}")
                        print("-" * 90)
                        
                        for id_prod, dados_prod in produtos_encontrados.items():
                            print(f"{id_prod:<5}| {dados_prod['nome']:<20}| {dados_prod['marca']:<12}| "
                                  f"{dados_prod['preco']:>10.2f}| {dados_prod['cor']:<10}| {dados_prod['quantidade']:>8}")
                        
                        print("-" * 90)

                        venda_id = input("Informe O ID Do Produto A Ser Vendido: ").strip()
                        
                        if venda_id not in produtos_encontrados:
                            print("ID Inválido, Tente Novamente")
                            sleep(1)
                            continue

                        valor_venda += adicionar_produto_carrinho(venda_id, produtos, produtos_vendidos)

            else:
                limpar_terminal()
                print("Opção Inválida!")
                sleep(1)
                limpar_terminal()

        # Se o carrinho estiver vazio, cancela a venda
        if not produtos_vendidos:
            print("Nenhum Produto Foi Adicionado. Venda Cancelada.")
            sleep(2)
            limpar_terminal()
            continue
        
        # Chama a função de realizar venda
        venda_realizada = RealizarVenda(
                    cpf_cliente=cpf_venda,
                    pagamento=valor_venda,
                    produtos_vendidos=produtos_vendidos,
                    prazo=True,
                    vendas=vendas,
                    produtos=produtos,
                    clientes=clientes        
                )
          
def VisualizarVendas():
    global vendas

    while True:
        print("""
        ===============================================
                    Visualização de Vendas
        ===============================================
            1 - Todas as vendas
            2 - Vendas do último mês
            3 - Vendas da última semana
            4 - Voltar
        ===============================================
        """)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            limpar_terminal()
            mostrar_vendas(vendas_filtradas)

        elif opcao == "2":
            hoje = datetime.today().date()
            ultimo_mes = hoje - timedelta(days=30)
            vendas_filtradas = {
                id_venda: dados for id_venda, dados in vendas.items()
                if datetime.fromisoformat(dados["data"]).date() >= ultimo_mes
            }

            limpar_terminal()
            mostrar_vendas(vendas_filtradas)

        elif opcao == "3":
            hoje = datetime.today().date()
            ultima_semana = hoje - timedelta(days=7)
            vendas_filtradas = {
                id_venda: dados for id_venda, dados in vendas.items()
                if datetime.fromisoformat(dados["data"]).date() >= ultima_semana
            }
            limpar_terminal()
            mostrar_vendas(vendas_filtradas)

        elif opcao == "4":
            break
        else:
            print("Opção inválida, tente novamente.")
            sleep(1)
            limpar_terminal()


def PagarPrazo():
    global clientes, produtos, vendas
    cpf_cliente = input("Informe O CPF Do Cliente Para Pagamento: ").strip()

    if cpf_cliente in clientes:
        cliente = clientes[cpf_cliente]
        print("Cliente Encontrado!")
        sleep(1)
        print(f"\nCPF: {cpf_cliente} - Nome: {cliente['nome']} - Saldo Devedor: R${cliente['saldo_devedor']:.2f}")

        pagamento = float(input("Qual A Quantia Do Pagamento? : "))

        RealizarVenda(cpf_cliente=cpf_cliente,pagamento=pagamento,produtos=produtos,
                        vendas=vendas,clientes=clientes,prazo=False)
        
        limpar_terminal(1)
    else:
        print("CPF Não Encontrado, Por Favor Cadastre-O!")
        sleep(2)
        limpar_terminal()


def RelatorioFinanceiro():
    global vendas, clientes

    while True:
        print("""
        ===============================================
                  Relatórios Financeiros
        ===============================================
            1 - Faturamento
            2 - Vendas a Prazo / Dívidas
            3 - Voltar
        ===============================================
        """)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            relatorio_faturamento()
        elif opcao == "2":
            relatorio_dividas()
        elif opcao == "3":
            break
        else:
            print("Opção inválida!")
            limpar_terminal(1)


def relatorio_faturamento():
    global vendas
    hoje = datetime.today().date()
    limpar_terminal()

    print("""
    ===============================================
                Faturamento por Período
    ===============================================
        1 - Últimos 2 anos
        2 - Último ano
        3 - Últimos 6 meses
        4 - Último mês
        5 - Última semana
        6 - Voltar
    ===============================================
    """)
    opcao = input("Escolha uma opção: ").strip()
    limpar_terminal()

    if opcao == "6":
        return

    # Definir intervalo
    if opcao == "1":
        inicio = hoje - timedelta(days=730)
    elif opcao == "2":
        inicio = hoje - timedelta(days=365)
    elif opcao == "3":
        inicio = hoje - timedelta(days=180)
    elif opcao == "4":
        inicio = hoje - timedelta(days=30)
    elif opcao == "5":
        inicio = hoje - timedelta(days=7)
    else:
        print("Opção inválida!")
        return

    # Filtrar vendas
    vendas_filtradas = [
        dados for dados in vendas.values()
        if datetime.fromisoformat(dados["data"]).date() >= inicio
    ]

    faturamento = sum(v["valor_venda"] for v in vendas_filtradas)
    print(f"\nFaturamento no período: R${faturamento:.2f}")
    print(f"Total de vendas: {len(vendas_filtradas)}")
    input("\nPressione ENTER para continuar...")
    limpar_terminal()


def relatorio_dividas():
    global clientes
    limpar_terminal()
    print("""
    ===============================================
                Relatório de Dívidas
    ===============================================
        1 - Ordenar por valor (crescente)
        2 - Ordenar por valor (decrescente)
        3 - Ordenar por data (mais antigas)
        4 - Ordenar por data (mais novas)
        5 - Voltar
    ===============================================
    """)
    opcao = input("Escolha uma opção: ").strip()
    limpar_terminal()

    # Filtrar clientes com dívida
    clientes_endividados = {
        cpf: dados for cpf, dados in clientes.items()
        if dados["saldo_devedor"] > 0
    }

    if not clientes_endividados:
        print("Nenhum cliente com dívida encontrado.")
        limpar_terminal(2)
        return

    # Ordenações
    if opcao == "1":
        ordenados = sorted(clientes_endividados.items(), key=lambda x: x[1]["saldo_devedor"])
    elif opcao == "2":
        ordenados = sorted(clientes_endividados.items(), key=lambda x: x[1]["saldo_devedor"], reverse=True)
    elif opcao == "3":
        ordenados = sorted(clientes_endividados.items(), key=lambda x: datetime.fromisoformat(x[1].get("data_divida", datetime.today().isoformat())))
    elif opcao == "4":
        ordenados = sorted(clientes_endividados.items(), key=lambda x: datetime.fromisoformat(x[1].get("data_divida", datetime.today().isoformat())), reverse=True)
    elif opcao == "5":
        return
    else:
        print("Opção inválida!")
        return

    # Mostrar relatório
    print("\nClientes com dívida:\n")
    print("-" * 70)
    print(f"{'CPF':<15}| {'Nome':<20}| {'Saldo Devedor (R$)':>15}")
    print("-" * 70)
    for cpf, dados in ordenados:
        print(f"{cpf:<15}| {dados['nome']:<20}| {dados['saldo_devedor']:>15.2f}")
    print("-" * 70)

    input("\nPressione ENTER para continuar...")
    limpar_terminal()


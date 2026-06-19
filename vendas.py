import json 
from ultils import limpar_terminal, atualizar_arquivos, adicionar_produto_carrinho, RealizarVenda
from time import sleep
from usuarios import CadastrarCliente
import os
from datetime import date

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
    global clientes, produtos, vendas, id_venda

    venda_realizada = False
    while not venda_realizada:
        cpf_venda = input('CPF Do Comprador: ').strip()
        cpf_encontrado = False
        
        for id_cli, dados_cli in clientes.items():
            if dados_cli["cpf"] == cpf_venda:
                cpf_encontrado = True
                break
        
        if not cpf_encontrado:
            print('CPF não encontrado, por favor cadastre-o!')
            sleep(2)
            limpar_terminal()
            cpf_venda = CadastrarCliente() 

        produtos_vendidos = []
        valor_venda = 0

        # LOOP DE COMPRAS
        while True:
            print("""
                Formas de Busca     
        ==============================
        1- Buscar Por ID do Produto
        2- Buscar Por Nome do Produto
        3- Finalizar Compra (Ir p/ Pagamento)L
        ===============================    """)
            busca = input("Qual a forma de busca ? : ")

            if busca == '3':
                limpar_terminal()
                break # Sai do loop de busca e vai para o pagamento

            elif busca == '1':
                while True:
                    limpar_terminal()
                    print("deixe o campo vazio para voltar ao menu de busca")
                    venda_id = input("Informe o ID do produto a ser vendido: ").strip()

                    if venda_id == "":
                        limpar_terminal()
                        break

                    # Somando o retorno da função ao valor total da venda
                    valor_venda += adicionar_produto_carrinho(venda_id, produtos, produtos_vendidos)

            elif busca == '2':
                while True:
                    limpar_terminal()
                    print("Deixe o campo vazio para voltar ao menu de busca")
                    nome_produto = input("Informe o nome do produto: ").strip()

                    if nome_produto == '':
                        limpar_terminal()
                        break

                    produtos_encontrados = {}
                    for id_prod, dados_prod in produtos.items():
                        if nome_produto.lower() in dados_prod["nome"].lower() and dados_prod["quantidade"] > 0:
                            produtos_encontrados[id_prod] = dados_prod

                    if produtos_encontrados:
                        print(f"\nForam encontrados {len(produtos_encontrados)} resultados:")
                        print("-" * 90)
                        print(f"{'ID':<5}| {'Nome':<20}| {'Marca':<12}| {'Preço (R$)':>10}| {'Cor':<10}| {'Estoque':>8}")
                        print("-" * 90)
                        
                        for id_prod, dados_prod in produtos_encontrados.items():
                            print(f"{id_prod:<5}| {dados_prod['nome']:<20}| {dados_prod['marca']:<12}| {dados_prod['preco']:>10.2f}| {dados_prod['cor']:<10}| {dados_prod['quantidade']:>8}")
                        
                        print("-" * 90)
                        print("")

                        venda_id = input("Informe o ID do produto a ser vendido: ").strip()
                        
                        if venda_id not in produtos_encontrados:
                            print("ID invalido, tente novamente")
                            sleep(1)
                            continue

                        # Somando o retorno da função ao valor total da venda
                        valor_venda += adicionar_produto_carrinho(venda_id, produtos, produtos_vendidos)

            else:
                limpar_terminal()
                print("Opção invalida !")
                sleep(1)
                limpar_terminal()

        # Se o carrinho estiver vazio, não faz sentido ir para o pagamento
        if not produtos_vendidos:
            print("Nenhum produto foi adicionado. Venda cancelada.")
            sleep(2)
            limpar_terminal()
            continue
        
        RealizarVenda(cpf_cliente=cpf_venda,pagamento=valor_venda, produtos=produtos, vendas=vendas, 
                  clientes=clientes, produtos_vendidos=produtos_vendidos, prazo=False)
        # LOOP DE PAGAMENTO
        '''while not venda_realizada:               
            print(f"""
        ====-FORMAS DE PAGAMENTO-====
        Valor Total: R${valor_venda:.2f}
        -----------------------------
            1 - Pix
            2 - A Vista (Espécie)
            3 - A Vista (Cartão)
            4 - Parcelado
            5 - A Prazo
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
            elif forma_pagamento == '5':
                nome_metodo = "A Prazo"
                
                for id_cli, dados_cli in clientes.items():
                    if dados_cli["cpf"] == cpf_venda:
                        clientes[id_cli]["saldo_devedor"] += float(valor_venda)
                        print(f"Saldo devedor de {dados_cli['nome']} atualizado para: R${clientes[id_cli]['saldo_devedor']:.2f}")
                        sleep(2)
                        break
            else:
                print("Opção inválida!")
                sleep(1)
                limpar_terminal()
                continue 

            venda_atual = {
                "cpf_cliente": cpf_venda, 
                "valor_venda": valor_venda,
                "forma_pagamento": nome_metodo,
                "tipo_venda": "Venda de produto",
                "data": hoje,
                "ID_produtos_vendidos": produtos_vendidos
            }
            
            id_venda += 1 # Incrementa de 1 em 1 para novos IDs

            vendas[str(id_venda)] = venda_atual
            atualizar_arquivos(produtos=produtos, vendas=vendas, clientes=clientes)
            
            print("\nVenda realizada com sucesso!")
            venda_realizada = True
            input("\nPressione Enter para sair...")
            limpar_terminal()'''
            
def VisualizarVendas():
    pass

def PagarPrazo():
    venda_realizada = False
    cpf_cliente = input("informe o cpf do cliente para pagamento: ").strip()
    for i, cliente in clientes.items():
        if cliente["cpf"].strip() == cpf_cliente:
            print("cliente encontrado ! ")
            sleep(1)
            print(f"\nID: {i} - Nome: {cliente['nome']} - CPF: {cliente['cpf']} - Saldo Devedor: R${cliente['saldo_devedor']:.2f}")

            pagamento = float(input("qual a quantia do do pagamento ? : "))
            while not venda_realizada:               
                print(f"""
            ====-FORMAS DE PAGAMENTO-====
            Valor Total: R${pagamento:.2f}
            -----------------------------
                1 - Pix
                2 - A Vista (Espécie)
                3 - A Vista (Cartão)
                4 - Parcelado
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
                else:
                    print("Opção inválida!")
                    sleep(1)
                    limpar_terminal()
                    continue 

                venda_atual = {
                    "cpf_cliente": cpf_cliente, 
                    "valor_venda": pagamento,
                    "forma_pagamento": nome_metodo, 
                    "tipo_venda": "Pagamento de divida",
                    "data": hoje,
                    "ID_produtos_vendidos": None
                }
                
                id_venda += 1 # Incrementa de 1 em 1 para novos IDs

                vendas[str(id_venda)] = venda_atual
                atualizar_arquivos(produtos=produtos, vendas=vendas, clientes=clientes)

                for id_cli, dados_cli in clientes.items():
                    if dados_cli["cpf"] == cpf_cliente:
                        print(f"Saldo devedor de {dados_cli['nome']} foi de R${clientes[id_cli]['saldo_devedor']:.2f}")
                        sleep(0.5)
                        clientes[id_cli]["saldo_devedor"] -= float(pagamento)
                        print(f"Para: R${clientes[id_cli]['saldo_devedor']:.2f}")
                        limpar_terminal(2)
                        break
                
                venda_realizada = True


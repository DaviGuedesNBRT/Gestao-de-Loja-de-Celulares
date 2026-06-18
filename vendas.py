import json 
from ultils import limpar_terminal, atualizar_arquivos
from time import sleep
from usuarios import CadastrarCliente
import os
from datetime import date

vendas = {}
clientes = {}
produtos = {}
contador_completo = {}
id_venda = 0


with open("banco/estoque.json", "r", encoding="utf-8") as arquivo:
    produtos = json.load(arquivo)

with open("banco/clientes.json", "r", encoding="utf-8") as arquivo:
    clientes = json.load(arquivo)

with open("banco/vendas.json", "r", encoding="utf-8") as arquivo:
    vendas = json.load(arquivo)

with open("banco/contador.json", "r", encoding="utf-8") as arquivo:
    contador_completo = json.load(arquivo)
    id_venda = contador_completo["cont_vendas"]


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


from datetime import date
from time import sleep

def efetuarVenda():
    global clientes, produtos, vendas, id_venda, contador_completo

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

        while True:
            print("Deixe o campo vazio para sair")
            nome_produto = input("Informe o nome do produto: ").strip()

            if nome_produto == '':
                limpar_terminal()
                break

            produtos_encontrados = {}
            
            for id_prod, dados_prod in produtos.items():
                if nome_produto.lower() in dados_prod["nome"].lower():
                    produtos_encontrados[id_prod] = dados_prod

            if produtos_encontrados:
                print(f"\nForam encontrados {len(produtos_encontrados)} resultados:")
                for id_prod, dados_prod in produtos_encontrados.items():
                    print(f"""
            ID: {id_prod} | Nome: {dados_prod['nome']}
            Marca: {dados_prod['marca']} | Preço: R${dados_prod['preco']:.2f}
            Cor: {dados_prod['cor']} | Estoque Atual: {dados_prod["quantidade"]}
            ================================================================
                    """)
                
                venda_id = input("Informe o ID do produto a ser vendido: ").strip()
                
                if venda_id in produtos_encontrados:
                    quantidade = int(input("Informe a quantidade de produtos: "))

                    while produtos[venda_id]["quantidade"] < quantidade:
                        print(f"\nA quantidade excedeu o estoque! Estoque máximo atual: {produtos[venda_id]['quantidade']}")
                        quantidade = int(input("Informe uma quantidade válida: "))

                    produtos[venda_id]["quantidade"] -= quantidade

                    produto_comprado = produtos[venda_id].copy()
                    produto_comprado["quantidade"] = quantidade 

                    produtos_vendidos.append(produto_comprado)
                    valor_venda += produtos[venda_id]["preco"] * quantidade

                    print("\nProduto adicionado ao carrinho!")
                    sleep(1)
                    limpar_terminal()
                else:
                    print("ID selecionado inválido.")
                    sleep(1.5)
                    limpar_terminal()
            else:
                print("Produto Não Encontrado!")
                sleep(1.5)
                limpar_terminal()

        if not produtos_vendidos:
            print("Nenhum produto foi selecionado. Venda cancelada.")
            sleep(2)
            limpar_terminal()
            break

        while not venda_realizada:               
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
                "data": hoje,
                "produtos_vendidos": produtos_vendidos
            }
            
            id_venda += 1
            vendas[str(id_venda)] = venda_atual
            contador_completo["cont_vendas"] = id_venda

            atualizar_arquivos(produtos=produtos, vendas=vendas, clientes=clientes, contador=contador_completo)
            
            print("\nVenda realizada com sucesso!")
            venda_realizada = True
            input("\nPressione Enter para sair...")
            limpar_terminal()

def visualizarVendas():
    pass
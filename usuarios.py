import os
import json
import time
from ultils import limpar_terminal, atualizar_arquivos

clientes = {}
contador_completo = {}
id_cliente = 0

with open("banco/clientes.json", "r", encoding="utf-8") as arquivo:
    clientes = json.load(arquivo)

with open("banco/contador.json", "r", encoding="utf-8") as arquivo:
    contador_completo = json.load(arquivo)
    id_cliente = contador_completo["cont_clientes"]


def ModuloClientes():
    while True:
        print("""
            =======================
            1 - Cadastrar Cliente
            2 - Editar Cliente
            3 - visualizar Cliente
            4 - Visualizar Clientes
            5 - Excluir Cliente
            6 - Voltar Para O Menu Principal
            =======================
            """)
        print()
        
        opcao = input("Qual opção você deseja ? :")    
        limpar_terminal()

        if opcao == '1':
            limpar_terminal()
            CadastrarCliente()

        elif opcao == '2':
            limpar_terminal()
            ProcessarCliente(atualizar=True)

        elif opcao == '3':
            limpar_terminal()
            ProcessarCliente()

        elif opcao == '4':
            limpar_terminal()
            VisualizarClientes()

        elif opcao == '5':
            limpar_terminal()
            ProcessarCliente(excluir=True)
        
        elif opcao == '6':
            limpar_terminal()
            break


def CadastrarCliente():
    global id_cliente, clientes, contador_completo 
    
    cpf = input("Digite o CPF do cliente: ")
    while True:
        cpf_existe = False
        for i, dados_cliente in clientes.items():
            if dados_cliente["cpf"] == cpf:
                cpf_existe = True
                break
        
        if cpf_existe:
            print("CPF já cadastrado. Por favor, insira um CPF diferente.")
            cpf = input("Digite o CPF do cliente: ")
        else:
            break

    nome = input("Digite o nome do cliente: ")
    email = input("Digite o email do cliente: ")
    telefone = input("Digite o telefone do cliente: ")        
    saldo_devedor = 0.0
    compras_feitas = 0
    
    id_cliente += 1 
    dados = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cpf": cpf,
        "compras": compras_feitas,
        "saldo_devedor": saldo_devedor,
        "habilitado": True,
        }

    clientes[str(id_cliente)] = dados
    contador_completo["cont_clientes"] = id_cliente

    atualizar_arquivos(clientes=clientes, contador=contador_completo)
    print("Cliente cadastrado com sucesso!")
    limpar_terminal(1)
    return cpf

def ProcessarCliente(excluir=False, atualizar=False):
    global clientes  
    
    while True:
        print(f"""
            =======================
            De Qual Forma Você Deseja Buscar O Cliente {
                'para Exclusão' if excluir else 'para Atualização' if atualizar else ''
            } ?
            1 - Buscar Por Nome
            2 - Buscar Por CPF
            3 - Buscar Por Telefone
            4 - Menu de Clientes
            =======================
        """)

        visualizar_cliente = input("Digite a opção desejada: ")
        limpar_terminal()

        if visualizar_cliente == '4':
            break

        if visualizar_cliente not in ['1', '2', '3']:
            print("Opção inválida! Por favor, escolha uma opção válida.")
            limpar_terminal(1)
            continue

        clientes_encontrados = {}

        if visualizar_cliente == '1':
            nome_cliente = input("Digite o nome do cliente: ").strip()
            limpar_terminal()
            for i, dados in clientes.items() and dados["habilitado"] == True:
                if dados["nome"].lower() == nome_cliente.lower():
                    clientes_encontrados[i] = dados

        elif visualizar_cliente == '2':
            cpf_cliente = input("Digite o CPF do cliente: ").strip()
            limpar_terminal()
            for i, dados in clientes.items() and dados["habilitado"] == True:
                if dados["cpf"] == cpf_cliente:
                    clientes_encontrados[i] = dados

        elif visualizar_cliente == '3':
            telefone_cliente = input("Digite o telefone do cliente: ").strip()
            limpar_terminal()
            for i, dados in clientes.items():
                if dados["telefone"] == telefone_cliente and dados["habilitado"] == True:
                    clientes_encontrados[i] = dados

        if clientes_encontrados:
            print(f"Foram encontrados {len(clientes_encontrados)} resultados de busca:")
            for i, dados in clientes_encontrados.items():
                print(f"\nID: {i} - Nome: {dados['nome']} - Email: {dados['email']} - Telefone: {dados['telefone']} - CPF: {dados['cpf']} - Saldo Devedor: R${dados['saldo_devedor']:.2f}")
            
            if not excluir and not atualizar:
                input("\nPressione Enter para continuar...")
                limpar_terminal()
                
            if excluir:
                id_escolhido = input("\nDigite o ID do cliente desejado: ").strip()
                if id_escolhido in clientes_encontrados:
                    clientes[id_escolhido]["habilitado"] = False
                    atualizar_arquivos(clientes=clientes)                    
                    
                    print("Cliente excluído com sucesso!")
                    limpar_terminal(1)

                else:
                    print("ID inválido ou não correspondente à busca.")
                    limpar_terminal(1)

            elif atualizar:
                id_escolhido = input("\nDigite o ID do cliente desejado: ").strip()
                if id_escolhido in clientes_encontrados:
                    cliente_atualizar = clientes[id_escolhido]

                    print("\nDigite os novos dados (deixe em branco para manter o atual):")
                    nome = input(f"Nome ({cliente_atualizar['nome']}): ") or cliente_atualizar['nome']
                    email = input(f"Email ({cliente_atualizar['email']}): ") or cliente_atualizar['email']
                    telefone = input(f"Telefone ({cliente_atualizar['telefone']}): ") or cliente_atualizar['telefone']
                    cpf = input(f"CPF ({cliente_atualizar['cpf']}): ") or cliente_atualizar['cpf']
                    
                    clientes[id_escolhido] = {
                        "nome": nome,
                        "email": email,
                        "telefone": telefone,
                        "cpf": cpf
                    }

                    atualizar_arquivos(clientes=clientes)
                    print("Cliente atualizado com sucesso!")
                    limpar_terminal(1)

                else:
                    print("ID inválido ou não correspondente à busca.")
                    limpar_terminal(1)

        else:
            print("Nenhum cliente encontrado.")
            limpar_terminal(1)

def VisualizarClientes():
    if not clientes:
        print("Nenhum cliente cadastrado no sistema.")
    else:
        print("========== LISTA DE CLIENTES ==========")
        for id_cliente, dados in clientes.items():
            if dados["habilitado"] == True:
                print(f"ID: {id_cliente} Nome: {dados['nome']}")
                print(f"Email: {dados['email']} ")
                print(f"Telefone: {dados['telefone']} CPF: {dados['cpf']}")
                print(f"Saldo Devedor: R${dados['saldo_devedor']:.2f}")
                print("-" * 40) 

    input("\nPressione Enter para voltar ao Menu...")
    limpar_terminal()


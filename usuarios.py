import os
import json
import time

clientes = []

if os.path.exists("clientes.json"):
    with open("clientes.json", "r", encoding="utf-8") as arquivo:
        clientes = json.load(arquivo)
else:
    with open("clientes.json", "w", encoding="utf-8") as arquivo:
        json.dump([], arquivo, indent=4, ensure_ascii=False)  

def limpar_terminal():
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para Linux ou Mac
    else:
        os.system("clear")


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
    nome = input("Digite o nome do cliente: ")
    email = input("Digite o email do cliente: ")
    telefone = input("Digite o telefone do cliente: ")
    cpf = input("Digite o CPF do cliente: ")

    for i, cliente in enumerate(clientes):
        if cliente["cpf"] == cpf:
            print("CPF já cadastrado. Por favor, insira um CPF diferente.")

            while cliente["cpf"] == cpf:
                cpf = input("Digite o CPF do cliente: ")
            
        
    saldo_devedor = float(input("Digite o saldo devedor do cliente: "))

    dicionario_cliente = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cpf": cpf,
                "saldo_devedor": saldo_devedor
            }

    clientes.append(dicionario_cliente)

    with open("clientes.json", "w", encoding="utf-8") as arquivo:
        json.dump(clientes, arquivo, indent=4, ensure_ascii=False)



def ProcessarCliente(excluir=False, atualizar=False):
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

        Visualizar_cliente = input("Digite a opção desejada: ")
        limpar_terminal()

        #busca por nome    
        if Visualizar_cliente == '1':
            clientes_encontrados = []
            nome_cliente = input("Digite o nome do cliente: ")
            limpar_terminal()

            for i, cliente in enumerate(clientes):
                if clientes[i]["nome"] == nome_cliente:
                    clientes_encontrados.append({"indice": i, "dados": cliente})

            if clientes_encontrados:
                print(f"Foram encontrados {len(clientes_encontrados)} Resultados da Buesca")
                for cliente in clientes_encontrados:
                    print()
                    print(f"ID: {cliente['indice']+1} - Nome: {cliente['dados']['nome']}- Email: {cliente['dados']['email']} -Telefone: {cliente['dados']['telefone']} -CPF: {cliente['dados']['cpf']} -Saldo Devedor: {cliente['dados']['saldo_devedor']}")
                                    
                if excluir:
                    print()
                    id_cliente = int(input("Digite o ID do cliente que deseja excluir: "))-1
                    if 0 <= id_cliente < len(clientes):
                        del clientes[id_cliente]

                        with open("clientes.json", "w", encoding="utf-8") as arquivo:
                            json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

                        print("Cliente excluído com sucesso!")
                        time.sleep(1)
                        limpar_terminal()

                    else:
                        print("ID inválido. Nenhum cliente foi excluído.")
                        time.sleep(1)
                        limpar_terminal()

                elif atualizar:
                    print()
                    id_cliente = int(input("Digite o ID do cliente que deseja atualizar: "))-1
                    if 0 <= id_cliente < len(clientes):
                        cliente_atualizar = clientes[id_cliente]

                        print("Digite os novos dados do cliente (deixe em branco para manter o valor atual):")
                        nome = input(f"Nome ({cliente_atualizar['nome']}): ") or cliente_atualizar['nome']
                        email = input(f"Email ({cliente_atualizar['email']}): ") or cliente_atualizar['email']
                        telefone = input(f"Telefone ({cliente_atualizar['telefone']}): ") or cliente_atualizar['telefone']
                        cpf = input(f"CPF ({cliente_atualizar['cpf']}): ") or cliente_atualizar['cpf']
                        saldo_devedor_input = input(f"Saldo Devedor ({cliente_atualizar['saldo_devedor']}): ")
                        saldo_devedor = float(saldo_devedor_input) if saldo_devedor_input else cliente_atualizar['saldo_devedor']

                        clientes[id_cliente] = {
                            "nome": nome,
                            "email": email,
                            "telefone": telefone,
                            "cpf": cpf,
                            "saldo_devedor": saldo_devedor
                        }

                        with open("clientes.json", "w", encoding="utf-8") as arquivo:
                            json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

                        print("Cliente atualizado com sucesso!")
                        time.sleep(1)
                        limpar_terminal()

            else:
                print("Cliente não encontrado.")
                time.sleep(1)
                limpar_terminal()
            

        elif Visualizar_cliente == '2':
            cpf_cliente = input("Digite o CPF do cliente: ")
            limpar_terminal()

            for i,cliente in enumerate(clientes):
                if cliente["cpf"] == cpf_cliente:
                    print(f"ID: {i+1} - Nome: {cliente['nome']}- Email: {cliente['email']} -Telefone: {cliente['telefone']} -CPF: {cliente['cpf']} -Saldo Devedor: {cliente['saldo_devedor']}")
            
                

            if excluir:
                    print()
                    id_cliente = int(input("Digite o ID do cliente que deseja excluir: "))-1
                    if 0 <= id_cliente < len(clientes):
                        del clientes[id_cliente]
                        print("Cliente excluído com sucesso!")

                        with open("clientes.json", "w", encoding="utf-8") as arquivo:
                            json.dump(clientes, arquivo, indent=4, ensure_ascii=False)
                        time.sleep(1)
                        limpar_terminal()

                    else:
                        print("ID inválido. Nenhum cliente foi excluído.")


            if atualizar:
                print()
                id_cliente = int(input("Digite o ID do cliente que deseja atualizar: "))-1
                if 0 <= id_cliente < len(clientes):
                    cliente_atualizar = clientes[id_cliente]

                    print("Digite os novos dados do cliente (deixe em branco para manter o valor atual):")
                    nome = input(f"Nome ({cliente_atualizar['nome']}): ") or cliente_atualizar['nome']
                    email = input(f"Email ({cliente_atualizar['email']}): ") or cliente_atualizar['email']
                    telefone = input(f"Telefone ({cliente_atualizar['telefone']}): ") or cliente_atualizar['telefone']
                    cpf = input(f"CPF ({cliente_atualizar['cpf']}): ") or cliente_atualizar['cpf']
                    saldo_devedor_input = input(f"Saldo Devedor ({cliente_atualizar['saldo_devedor']}): ")
                    saldo_devedor = float(saldo_devedor_input) if saldo_devedor_input else cliente_atualizar['saldo_devedor']

                    clientes[id_cliente] = {
                        "nome": nome,
                        "email": email,
                        "telefone": telefone,
                        "cpf": cpf,
                        "saldo_devedor": saldo_devedor
                    }

                    with open("clientes.json", "w", encoding="utf-8") as arquivo:
                        json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

                    time.sleep(1)
                    print("Cliente atualizado com sucesso!")

                else:
                    print("Cliente não encontrado.")
        

        elif Visualizar_cliente == '3':
            telefone_cliente = input("Digite o telefone do cliente: ")
            limpar_terminal()

            for i,cliente in enumerate(clientes):
                if cliente["telefone"] == telefone_cliente:
                    print(f"ID: {i+1} - Nome: {cliente['nome']}- Email: {cliente['email']} -Telefone: {cliente['telefone']} -CPF: {cliente['cpf']} -Saldo Devedor: {cliente['saldo_devedor']}")
            
            if excluir:
                    print()
                    id_cliente = int(input("Digite o ID do cliente que deseja excluir: "))-1
                    if 0 <= id_cliente < len(clientes):
                        del clientes[id_cliente]

                        with open("clientes.json", "w", encoding="utf-8") as arquivo:
                            json.dump(clientes, arquivo, indent=4, ensure_ascii=False)


                        print("Cliente excluído com sucesso!")
                        time.sleep(1)
                        limpar_terminal()

                    else:
                        print("ID inválido. Nenhum cliente foi excluído.")
                        time.sleep(1)
                        limpar_terminal()


            elif atualizar:
                print()
                id_cliente = int(input("Digite o ID do cliente que deseja atualizar: "))-1
                time.sleep(0.5)
                limpar_terminal()

                if 0 <= id_cliente < len(clientes):
                    cliente_atualizar = clientes[id_cliente]
                    print("Digite os novos dados do cliente (deixe em branco para manter o valor atual):")
                    nome = input(f"Nome ({cliente_atualizar['nome']}): ") or cliente_atualizar['nome']
                    email = input(f"Email ({cliente_atualizar['email']}): ") or cliente_atualizar['email']
                    telefone = input(f"Telefone ({cliente_atualizar['telefone']}): ") or cliente_atualizar['telefone']
                    cpf = input(f"CPF ({cliente_atualizar['cpf']}): ") or cliente_atualizar['cpf']
                    saldo_devedor_input = input(f"Saldo Devedor ({cliente_atualizar['saldo_devedor']}): ")
                    saldo_devedor = float(saldo_devedor_input) if saldo_devedor_input else cliente_atualizar['saldo_devedor']

                    clientes[id_cliente] = {
                        "nome": nome,
                        "email": email,
                        "telefone": telefone,
                        "cpf": cpf,
                        "saldo_devedor": saldo_devedor
                    }

                    with open("clientes.json", "w", encoding="utf-8") as arquivo:
                        json.dump(clientes, arquivo, indent=4, ensure_ascii=False)

                    print("Cliente atualizado com sucesso!")
                    time.sleep(1)
                    limpar_terminal()

                else:
                    print("Cliente não encontrado.")
                    limpar_terminal()

        elif Visualizar_cliente == '4':
            break

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")


def VisualizarClientes():
    for cliente in clientes:
        print(f"Nome: {cliente['nome']}- Email: {cliente['email']} -Telefone: {cliente['telefone']} -CPF: {cliente['cpf']} -Saldo Devedor: {cliente['saldo_devedor']}")
        print()
        
    input = ("\nPrecione Enter Para Voltar ao Menu...")
    limpar_terminal()


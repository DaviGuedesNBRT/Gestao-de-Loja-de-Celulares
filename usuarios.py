
import os




def limpar_terminal():
    # Para Windows
    if os.name == "nt":
        os.system("cls")
    # Para Linux ou Mac
    else:
        os.system("clear")

clientes = []
def ModuloClientes():
    while True:
        print("""
            =======================
            1 - Cadastrar Cliente
            2 - Editar Cliente
            3 - visualizar Cliente
            4 - Visualizar Clientes
            5 - Excluir Cliente
            6 - Atualizar Cliente
            =======================
            """)
        print()
        
        opcao = input("Qual opção você deseja ? :")    
        limpar_terminal()

        if opcao == '1':
            CadastrarCliente()

        elif opcao == '2':
            EditarCliente()

        elif opcao == '3':
            BuscarCliente()

        elif opcao == '4':
            VisualizarClientes()

        elif opcao == '5':
            ExcluirCliente()

        elif opcao == '6':
            AtualizarCliente()




def CadastrarCliente():
    dicionario_cliente = {}

    nome = input("Digite o nome do cliente: ")
    email = input("Digite o email do cliente: ")
    telefone = input("Digite o telefone do cliente: ")
    cpf = input("Digite o CPF do cliente: ")
    saldo_devedor = float(input("Digite o saldo devedor do cliente: "))

    for cliente in clientes:
        if cliente["cpf"] == cpf:
            print("Já existe um cliente cadastrado com esse CPF.")
        
        else:
            dicionario_cliente = {
                "nome": nome,
                "email": email,
                "telefone": telefone,
                "cpf": cpf,
                "saldo_devedor": saldo_devedor
            }

            clientes.append(dicionario_cliente)


def EditarCliente():
    pass

def BuscarCliente():
    while True:
        print("""
        =======================
        De Qual Forma Você Deseja Buscar O Cliente ?
        1 - Buscar Por Nome
        2 - Buscar Por CPF
        3 - Buscar Por Telefone
        =======================
        """)
        print()

        Visualizar_cliente = input("Digite a opção desejada: ")

        if Visualizar_cliente == '1':
            clientes_encontrados = []
            nome_cliente = input("Digite o nome do cliente: ")
            for i,cliente in clientes:
                if cliente["nome"] == nome_cliente:
                    clientes_encontrados.append({"indice": i, "dados": cliente})

            if clientes_encontrados:
                print(f"Foram encontrados {len(clientes_encontrados)} Resultados da Buesca")
                for cliente in clientes_encontrados:
                    print(f"Nome: {cliente['dados']['nome']}- Email: {cliente['dados']['email']} -Telefone: {cliente['dados']['telefone']} -CPF: {cliente['dados']['cpf']} -Saldo Devedor: {cliente['dados']['saldo_devedor']}")
                                    
            else:
                print("Cliente não encontrado.")
            

        elif Visualizar_cliente == '2':
            cpf_cliente = input("Digite o CPF do cliente: ")
            for cliente in clientes:
                if cliente["cpf"] == cpf_cliente:
                    print(f"Nome: {cliente['dados']['nome']}- Email: {cliente['dados']['email']} -Telefone: {cliente['dados']['telefone']} -CPF: {cliente['dados']['cpf']} -Saldo Devedor: {cliente['dados']['saldo_devedor']}")
                    
            else:
                print("Cliente não encontrado.")
            limpar_terminal()
        

        elif Visualizar_cliente == '3':
            telefone_cliente = input("Digite o telefone do cliente: ")
            for cliente in clientes:
                if cliente["telefone"] == telefone_cliente:
                    print(f"Nome: {cliente['dados']['nome']}- Email: {cliente['dados']['email']} -Telefone: {cliente['dados']['telefone']} -CPF: {cliente['dados']['cpf']} -Saldo Devedor: {cliente['dados']['saldo_devedor']}")
                
            else:
                print("Cliente não encontrado.")
            limpar_terminal()

        else:
            print("Opção inválida! Por favor, escolha uma opção válida.")

def VisualizarClientes():
    for cliente in clientes:
        print(f"Nome: {cliente['nome']}- Email: {cliente['email']} -Telefone: {cliente['telefone']} -CPF: {cliente['cpf']} -Saldo Devedor: {cliente['saldo_devedor']}")
        print("===============================================")

def ExcluirCliente():
    pass

def AtualizarCliente():
    pass

CadastrarCliente()
ExcluirCliente()
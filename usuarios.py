import os
import json
import time
from ultils import limpar_terminal, atualizar_arquivos, validar_formatar_cpf, validar_formatar_telefone

clientes = {}

with open("banco/clientes.json", "r", encoding="utf-8") as arquivo:
    clientes = json.load(arquivo)


def ModuloClientes():
    while True:
        print("""
            =========================================
                            CLIENTES
            =========================================
                1 - Cadastrar Cliente
                2 - Editar Cliente
                3 - visualizar Cliente
                4 - Visualizar Clientes
                5 - Excluir Cliente
                6 - Rehabilitar Cliente
                7 - Voltar Para O Menu Principal
            =========================================
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
            ProcessarCliente(rehabilitar= True)
        
        elif opcao == '7':
            limpar_terminal()
            break


def CadastrarCliente():
    global clientes 
    
    while True:
        try:
            cpf = validar_formatar_cpf(input("Digite O CPF Do Cliente: ").strip())
        except ValueError as e:
            print(e)
            continue

        if cpf in clientes:
            print("CPF Já Cadastrado. Por Favor, Insira Um CPF Diferente.")
            continue
        break

    nome = input("Digite O Nome Do Cliente: ").strip()
    email = input("Digite O Email Do Cliente: ").strip()

    while True:
        try:
            telefone = validar_formatar_telefone(input("Digite O Telefone Do Cliente: ").strip())
            break
        except ValueError as e:
            print(e)

    dados = {
        "nome": nome,
        "email": email,
        "telefone": telefone,
        "cpf": cpf,
        "compras": 0,
        "saldo_devedor": 0.0,
        "habilitado": True,
    }

    clientes[cpf] = dados
    atualizar_arquivos(clientes=clientes)
    print("Cliente Cadastrado Com Sucesso!")
    limpar_terminal(1)
    return cpf

def ProcessarCliente(excluir=False, atualizar=False, rehabilitar=False):
    global clientes  
    
    while True:
        print(f"""
            ================================
                De Qual Forma Você Deseja 
            Buscar O Cliente {
                'Para Exclusão' if excluir else 'Para Atualização' if atualizar else 'Para Reabilitar' if rehabilitar else ''
            } ?
            ================================
                1 - Buscar Por Nome
                2 - Buscar Por CPF
                3 - Buscar Por Telefone
                4 - Menu De Clientes
            ================================
        """)

        visualizar_cliente = input("Digite A Opção Desejada: ")
        limpar_terminal()

        if visualizar_cliente == '4':
            break

        if visualizar_cliente not in ['1', '2', '3']:
            print("Opção Inválida! Por Favor, Escolha Uma Opção Válida.")
            limpar_terminal(1)
            continue

        clientes_encontrados = {}

        if visualizar_cliente == '1':
            nome_cliente = input("Digite O Nome Do Cliente: ").strip()
            limpar_terminal()
            for cpf, dados in clientes.items():
                if nome_cliente.lower() in dados["nome"].lower():
                    if rehabilitar and not dados["habilitado"]:
                        clientes_encontrados[cpf] = dados
                    elif not rehabilitar and dados["habilitado"]:
                        clientes_encontrados[cpf] = dados

        elif visualizar_cliente == '2':
            cpf_cliente = input("Digite O CPF Do Cliente: ").strip()
            limpar_terminal()
            if cpf_cliente in clientes:
                dados = clientes[cpf_cliente]
                if rehabilitar and not dados["habilitado"]:
                    clientes_encontrados[cpf_cliente] = dados
                elif not rehabilitar and dados["habilitado"]:
                    clientes_encontrados[cpf_cliente] = dados

        elif visualizar_cliente == '3':
            telefone_cliente = input("Digite O Telefone Do Cliente: ").strip()
            limpar_terminal()
            for cpf, dados in clientes.items():
                if telefone_cliente == dados["telefone"]:
                    if rehabilitar and not dados["habilitado"]:
                        clientes_encontrados[cpf] = dados
                    elif not rehabilitar and dados["habilitado"]:
                        clientes_encontrados[cpf] = dados

        if clientes_encontrados:
            print(f"Foram Encontrados {len(clientes_encontrados)} Resultados De Busca:")
            print(f"\n{'CPF':<15} | {'Nome':<20} | {'Email':<25} | {'Telefone':<15} | {'Saldo Devedor (R$)':>18}")
            print("-" * 100)
            for cpf, dados in clientes_encontrados.items():
                print(f"{cpf:<15} | {dados['nome']:<20} | {dados['email']:<25} | {dados['telefone']:<15} | {dados['saldo_devedor']:>18.2f}")

                print(f"\nCPF: {cpf} - Nome: {dados['nome']} - Email: {dados['email']} - Telefone: {dados['telefone']} - Saldo Devedor: R${dados['saldo_devedor']:.2f}")
            
            if not excluir and not atualizar and not rehabilitar:
                input("\nPressione Enter Para Continuar...")
                limpar_terminal()
                
            if excluir:
                cpf_escolhido = input("\nDigite O CPF Do Cliente Desejado: ").strip()
                if cpf_escolhido in clientes_encontrados:
                    clientes[cpf_escolhido]["habilitado"] = False
                    atualizar_arquivos(clientes=clientes)                    
                    print("Cliente Excluído Com Sucesso!")
                    limpar_terminal(1)
                else:
                    print("CPF Inválido Ou Não Correspondente À Busca.")
                    limpar_terminal(1)

            elif atualizar:
                cpf_escolhido = input("\nDigite O CPF Do Cliente Desejado: ").strip()
                if cpf_escolhido in clientes_encontrados:
                    cliente_atualizar = clientes[cpf_escolhido]

                    print("\nDigite Os Novos Dados (Deixe Em Branco Para Manter O Atual):")
                    nome = input(f"Nome ({cliente_atualizar['nome']}): ") or cliente_atualizar['nome']
                    email = input(f"Email ({cliente_atualizar['email']}): ") or cliente_atualizar['email']
                    telefone = input(f"Telefone ({cliente_atualizar['telefone']}): ") or cliente_atualizar['telefone']
                    saldo_devedor = cliente_atualizar["saldo_devedor"]
                    habilitado = cliente_atualizar['habilitado']

                    clientes[cpf_escolhido] = {
                        "nome": nome,
                        "email": email,
                        "telefone": telefone,
                        "cpf": cpf_escolhido,
                        "saldo_devedor": saldo_devedor,
                        "habilitado": habilitado
                    }

                    atualizar_arquivos(clientes=clientes)
                    print("Cliente Atualizado Com Sucesso!")
                    limpar_terminal(1)
                else:
                    print("CPF Inválido Ou Não Correspondente À Busca.")
                    limpar_terminal(1)

            elif rehabilitar:
                cpf_escolhido = input("\nDigite O CPF Do Cliente Desejado: ").strip()
                if cpf_escolhido in clientes_encontrados:
                    clientes[cpf_escolhido]["habilitado"] = True
                    atualizar_arquivos(clientes=clientes)
                    print("Cliente Reabilitado Com Sucesso!")
                    limpar_terminal(1)
                else:
                    print("CPF Inválido Ou Não Correspondente À Busca.")
                    limpar_terminal(1)

        else:
            print("Nenhum Cliente Encontrado.")
            limpar_terminal(1)

def VisualizarClientes():
    if not clientes:
        print("Nenhum cliente cadastrado no sistema.")
    else:
        # Cabeçalho da tabela
        print("=" * 110)
        print(f"{'ID':<5}| {'Nome':<20}| {'Email':<25}| {'Telefone':<17}| {'CPF':<17}| {'Saldo Devedor':>15}")
        print("-" * 110)

        # Linhas de dados (ID baseado no índice da iteração)
        for idx, (cpf, dados) in enumerate(clientes.items(), start=1):
            if dados["habilitado"]:
                print(f"{idx:<5}| {dados['nome']:<20}| {dados['email']:<25}| "
                      f"{dados['telefone']:<17}| {cpf:<17}| R$ {dados['saldo_devedor']:>12.2f}")
        
        print("=" * 110)

    input("\nPressione Enter para voltar ao Menu...")
    limpar_terminal()



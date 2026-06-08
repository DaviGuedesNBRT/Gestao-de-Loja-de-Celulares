excluir = False
atualizar = False


print(f"""
            =======================
            De Qual Forma Você Deseja Buscar O Cliente {
                'para Exclusão' if excluir else 'para Atualização' if atualizar else ''
            } ?
            1 - Buscar Por Nome
            2 - Buscar Por CPF
            3 - Buscar Por Telefone
            =======================
        """)
print()
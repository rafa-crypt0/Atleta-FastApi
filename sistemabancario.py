"""
Sistema Bancário Modularizado - Versão 2.0
Gerenciamento de contas bancárias com usuários e operações.
"""

import re
from datetime import datetime

# Listas para armazenar dados
usuarios = []
contas = []
NUMERO_CONTA_INICIAL = 1

# Constantes
AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500


def sacar(*, saldo, valor, extrato, numero_saques):
    """
    Realiza operação de saque (argumentos keyword only).

    Retorna: tupla (saldo, extrato, numero_saques)
    """
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > LIMITE_VALOR_SAQUE
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("\n❌ Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        limite_formatado = LIMITE_VALOR_SAQUE
        print(f"\n❌ Operação falhou! Valor excede o limite de R$ {limite_formatado:.2f}.")
    elif excedeu_saques:
        print(f"\n❌ Operação falhou! Máximo de saques ({LIMITE_SAQUES}) excedido.")
    elif valor <= 0:
        print("\n❌ Operação falhou! O valor informado é inválido.")
    else:
        saldo -= valor
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f"Saque:    R$ {valor:>10.2f}  [{data_hora}]\n"
        numero_saques += 1
        print(f"\n✅ Saque de R$ {valor:.2f} realizado com sucesso!")

    return saldo, extrato, numero_saques


def depositar(saldo, valor, extrato, /):
    """
    Realiza operação de depósito (argumentos positional only).

    Retorna: tupla (saldo, extrato)
    """
    if valor > 0:
        saldo += valor
        data_hora = datetime.now().strftime('%d/%m/%Y %H:%M')
        extrato += f"Depósito: R$ {valor:>10.2f}  [{data_hora}]\n"
        print(f"\n✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("\n❌ Operação falhou! O valor informado é inválido.")

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato da conta (argumentos positional e keyword only).
    """
    print("\n" + "=" * 50)
    print(" " * 18 + "EXTRATO")
    print("=" * 50)

    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)

    print("-" * 50)
    print(f"Saldo atual: R$ {saldo:>10.2f}")
    print("=" * 50)


def criar_usuario():
    """
    Cria um novo usuário no sistema.
    """
    print("\n" + "=" * 50)
    print(" " * 15 + "NOVO USUÁRIO")
    print("=" * 50)

    cpf = input("Informe o CPF (somente números): ")
    cpf = limpar_cpf(cpf)

    if not validar_cpf(cpf):
        print("\n❌ CPF inválido! Deve conter 11 dígitos.")
        return

    # Verifica se CPF já existe
    if buscar_usuario_por_cpf(cpf):
        print("\n❌ Já existe um usuário cadastrado com este CPF!")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")

    print("\n--- Endereço ---")
    logradouro = input("Logradouro: ")
    numero = input("Número: ")
    bairro = input("Bairro: ")
    cidade = input("Cidade: ")
    estado = input("Estado (sigla): ").upper()

    endereco = f"{logradouro}, {numero} - {bairro} - {cidade}/{estado}"

    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios.append(usuario)
    print(f"\n✅ Usuário {nome} cadastrado com sucesso!")


def criar_conta_corrente():
    """
    Cria uma nova conta corrente vinculada a um usuário.
    """
    print("\n" + "=" * 50)
    print(" " * 12 + "NOVA CONTA CORRENTE")
    print("=" * 50)

    cpf = input("Informe o CPF do usuário: ")
    cpf = limpar_cpf(cpf)

    usuario = buscar_usuario_por_cpf(cpf)

    if not usuario:
        print("\n❌ Usuário não encontrado! Cadastre o usuário primeiro.")
        return

    numero_conta = len(contas) + NUMERO_CONTA_INICIAL

    conta = {
        "agencia": AGENCIA,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0
    }

    contas.append(conta)
    print("\n✅ Conta criada com sucesso!")
    print(f"Agência: {AGENCIA}")
    print(f"Conta: {numero_conta}")
    print(f"Titular: {usuario['nome']}")


def listar_contas():
    """
    Lista todas as contas cadastradas no sistema.
    """
    print("\n" + "=" * 50)
    print(" " * 15 + "CONTAS CADASTRADAS")
    print("=" * 50)

    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    for conta in contas:
        print(f"\nAgência: {conta['agencia']} | Conta: {conta['numero_conta']}")
        print(f"Titular: {conta['usuario']['nome']}")
        print(f"CPF: {formatar_cpf(conta['usuario']['cpf'])}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("-" * 50)


def listar_usuarios():
    """
    Lista todos os usuários cadastrados no sistema.
    """
    print("\n" + "=" * 50)
    print(" " * 15 + "USUÁRIOS CADASTRADOS")
    print("=" * 50)

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    for usuario in usuarios:
        print(f"\nNome: {usuario['nome']}")
        print(f"CPF: {formatar_cpf(usuario['cpf'])}")
        print(f"Data de Nascimento: {usuario['data_nascimento']}")
        print(f"Endereço: {usuario['endereco']}")
        print("-" * 50)


def buscar_usuario_por_cpf(cpf):
    """
    Busca um usuário pelo CPF.

    Retorna: dicionário do usuário ou None
    """
    for usuario in usuarios:
        if usuario['cpf'] == cpf:
            return usuario
    return None


def buscar_conta_por_numero(numero_conta):
    """
    Busca uma conta pelo número.

    Retorna: dicionário da conta ou None
    """
    for conta in contas:
        if conta['numero_conta'] == numero_conta:
            return conta
    return None


def limpar_cpf(cpf):
    """
    Remove caracteres não numéricos do CPF.
    """
    return re.sub(r'\D', '', cpf)


def validar_cpf(cpf):
    """
    Valida se o CPF tem 11 dígitos.
    """
    return len(cpf) == 11 and cpf.isdigit()


def formatar_cpf(cpf):
    """
    Formata CPF para exibição (000.000.000-00).
    """
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def selecionar_conta():
    """
    Permite ao usuário selecionar uma conta para operar.

    Retorna: dicionário da conta ou None
    """
    if not contas:
        print("\n❌ Nenhuma conta cadastrada! Crie uma conta primeiro.")
        return None

    print("\n--- Selecione a conta ---")
    numero_conta = int(input("Número da conta: "))

    conta = buscar_conta_por_numero(numero_conta)

    if not conta:
        print("\n❌ Conta não encontrada!")
        return None

    nome_titular = conta['usuario']['nome']
    print(f"\n✅ Conta selecionada: {conta['numero_conta']} - {nome_titular}")
    return conta


def processar_deposito(conta_atual):
    """Processa operação de depósito."""
    valor = float(input("\nInforme o valor do depósito: R$ "))
    conta_atual['saldo'], conta_atual['extrato'] = depositar(
        conta_atual['saldo'],
        valor,
        conta_atual['extrato']
    )


def processar_saque(conta_atual):
    """Processa operação de saque."""
    valor = float(input("\nInforme o valor do saque: R$ "))
    resultado = sacar(
        saldo=conta_atual['saldo'],
        valor=valor,
        extrato=conta_atual['extrato'],
        numero_saques=conta_atual['numero_saques']
    )
    conta_atual['saldo'], conta_atual['extrato'], conta_atual['numero_saques'] = resultado


def processar_extrato(conta_atual):
    """Processa exibição de extrato."""
    exibir_extrato(conta_atual['saldo'], extrato=conta_atual['extrato'])


def processar_operacao_bancaria(opcao, conta_atual):
    """Processa operações bancárias (depósito, saque, extrato)."""
    if not conta_atual:
        conta_atual = selecionar_conta()
        if not conta_atual:
            return conta_atual

    if opcao == "d":
        processar_deposito(conta_atual)
    elif opcao == "s":
        processar_saque(conta_atual)
    elif opcao == "e":
        processar_extrato(conta_atual)

    return conta_atual


def processar_opcao_menu(opcao, conta_atual):
    """Processa a opção escolhida no menu."""
    operacoes_bancarias = {"d", "s", "e"}

    if opcao in operacoes_bancarias:
        return processar_operacao_bancaria(opcao, conta_atual)

    if opcao == "nu":
        criar_usuario()
    elif opcao == "nc":
        criar_conta_corrente()
    elif opcao == "lc":
        listar_contas()
    elif opcao == "lu":
        listar_usuarios()
    elif opcao != "q":
        print("\n❌ Operação inválida! Por favor, selecione uma opção válida.")

    return conta_atual


def main():
    """
    Função principal do sistema bancário.
    """
    menu = """
╔════════════════════════════════════════════════╗
║          SISTEMA BANCÁRIO - v2.0               ║
╠════════════════════════════════════════════════╣
║  [d]  Depositar                                ║
║  [s]  Sacar                                    ║
║  [e]  Extrato                                  ║
║  [nu] Novo Usuário                             ║
║  [nc] Nova Conta                               ║
║  [lc] Listar Contas                            ║
║  [lu] Listar Usuários                          ║
║  [q]  Sair                                     ║
╚════════════════════════════════════════════════╝
=> """

    conta_atual = None

    while True:
        opcao = input(menu).lower()

        if opcao == "q":
            print("\n👋 Obrigado por usar nosso sistema! Até logo!")
            break

        conta_atual = processar_opcao_menu(opcao, conta_atual)


if __name__ == "__main__":
    main()

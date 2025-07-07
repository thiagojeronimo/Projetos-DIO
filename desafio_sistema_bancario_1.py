usuarios = []
contas = []

AGENCIA = "0001"
LIMITE_SAQUES = 3
LIMITE_VALOR = 500.0

def criar_usuario():
    cpf = input("CPF (somente números): ").strip()
    for u in usuarios:
        if u["cpf"] == cpf:
            print("Usuário já existe.")
            return
    nome = input("Nome completo: ").strip()
    nasc = input("Data de nascimento (dd/mm/aaaa): ").strip()
    endereco = input("Endereço (Rua, nº - Bairro - Cidade/UF): ").strip()
    usuarios.append({"nome": nome, "cpf": cpf, "nasc": nasc, "endereco": endereco})
    print("Usuário cadastrado com sucesso.")

def criar_conta():
    cpf = input("CPF do titular: ").strip()
    for u in usuarios:
        if u["cpf"] == cpf:
            numero = len(contas) + 1
            contas.append({
                "agencia": AGENCIA,
                "numero": numero,
                "cpf": cpf,
                "saldo": 0.0,
                "movs": [],
                "saques": 0
            })
            print(f"Conta {numero:04} criada.")
            return
    print("CPF não encontrado.")

def buscar_conta():
    numero = input("Número da conta: ").strip()
    for c in contas:
        if str(c["numero"]) == numero:
            return c
    print("Conta não encontrada.")
    return None

def depositar():
    conta = buscar_conta()
    if conta:
        valor = float(input("Valor do depósito: "))
        if valor > 0:
            conta["saldo"] += valor
            conta["movs"].append(f"Depósito: R${valor:.2f}")
            print("Depósito realizado.")
        else:
            print("Valor inválido.")

def sacar():
    conta = buscar_conta()
    if conta:
        valor = float(input("Valor do saque: "))
        if valor <= 0:
            print("Valor inválido.")
        elif valor > conta["saldo"]:
            print("Saldo insuficiente.")
        elif valor > LIMITE_VALOR:
            print("Excede o limite por saque.")
        elif conta["saques"] >= LIMITE_SAQUES:
            print("Limite diário de saques atingido.")
        else:
            conta["saldo"] -= valor
            conta["movs"].append(f"Saque: -R${valor:.2f}")
            conta["saques"] += 1
            print("Saque realizado.")

def mostrar_extrato():
    conta = buscar_conta()
    if conta:
        print("\n=== EXTRATO ===")
        if not conta["movs"]:
            print("Sem movimentações.")
        else:
            for m in conta["movs"]:
                print(m)
        print(f"Saldo atual: R${conta['saldo']:.2f}")
        print("================\n")

def listar_contas():
    for c in contas:
        dono = next((u for u in usuarios if u["cpf"] == c["cpf"]), None)
        print(f"Agência: {c['agencia']} | Conta: {c['numero']:04} | Titular: {dono['nome']}")

# Loop principal com menu
while True:
    print("""
[1] Novo Usuário
[2] Nova Conta
[3] Depositar
[4] Sacar
[5] Extrato
[6] Listar Contas
[0] Sair
""")
    opcao = input("=> ")

    if opcao == "1":
        criar_usuario()
    elif opcao == "2":
        criar_conta()
    elif opcao == "3":
        depositar()
    elif opcao == "4":
        sacar()
    elif opcao == "5":
        mostrar_extrato()
    elif opcao == "6":
        listar_contas()
    elif opcao == "0":
        print("Saindo do sistema...")
        break
    else:
        print("Opção inválida.")

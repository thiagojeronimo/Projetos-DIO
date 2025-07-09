from abc import ABC, abstractmethod
from datetime import date

# --------------------------- Transação --------------------------- #
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass

# ------------------------ Implementações de Transações ------------------------ #
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta._saldo += self.valor
            conta.historico.adicionar_transacao(self)
            print(f"Depósito de R${self.valor:.2f} realizado com sucesso.")

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)
            print(f"Saque de R${self.valor:.2f} realizado com sucesso.")

# --------------------------- Histórico --------------------------- #
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# --------------------------- Conta --------------------------- #
class Conta:
    def __init__(self, cliente, numero):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self.historico = Historico()

    def saldo(self):
        return self._saldo

    def sacar(self, valor):
        if valor <= self._saldo:
            self._saldo -= valor
            return True
        print("Saldo insuficiente.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            return True
        return False

# --------------------------- Conta Corrente --------------------------- #
class ContaCorrente(Conta):
    def __init__(self, cliente, numero):
        super().__init__(cliente, numero)
        self._limite = 500
        self._limite_saques = 3
        self._saques_realizados = 0

    def sacar(self, valor):
        if self._saques_realizados >= self._limite_saques:
            print("Limite de saques diários atingido.")
            return False
        if valor > self._limite:
            print("Valor excede o limite de saque.")
            return False
        if super().sacar(valor):
            self._saques_realizados += 1
            return True
        return False

# --------------------------- Cliente --------------------------- #
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

# --------------------------- Pessoa Física --------------------------- #
class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# --------------------------- Banco com Menu --------------------------- #
class Banco:
    def __init__(self):
        self.clientes = []
        self.contas = []

    def cadastrar_cliente(self):
        nome = input("Nome: ")
        cpf = input("CPF: ")
        nasc = input("Data de nascimento (AAAA-MM-DD): ")
        endereco = input("Endereço: ")
        cliente = PessoaFisica(cpf, nome, nasc, endereco)
        self.clientes.append(cliente)
        print("Cliente cadastrado com sucesso!")

    def criar_conta(self):
        cpf = input("CPF do cliente: ")
        cliente = self.buscar_cliente(cpf)
        if cliente:
            numero = len(self.contas) + 1
            conta = ContaCorrente(cliente, numero)
            cliente.adicionar_conta(conta)
            self.contas.append(conta)
            print("Conta criada com sucesso!")
        else:
            print("Cliente não encontrado.")

    def buscar_cliente(self, cpf):
        for cliente in self.clientes:
            if isinstance(cliente, PessoaFisica) and cliente.cpf == cpf:
                return cliente
        return None

    def menu(self):
        while True:
            print("""
[1] Cadastrar cliente
[2] Criar conta
[3] Depositar
[4] Sacar
[5] Extrato
[0] Sair
""")
            opcao = input("Escolha: ")

            if opcao == "1":
                self.cadastrar_cliente()
            elif opcao == "2":
                self.criar_conta()
            elif opcao == "3":
                self.operacao_financeira(Deposito)
            elif opcao == "4":
                self.operacao_financeira(Saque)
            elif opcao == "5":
                self.exibir_extrato()
            elif opcao == "0":
                print("Saindo...")
                break
            else:
                print("Opção inválida")

    def operacao_financeira(self, operacao_cls):
        cpf = input("CPF do titular: ")
        cliente = self.buscar_cliente(cpf)
        if not cliente:
            print("Cliente não encontrado.")
            return
        if not cliente.contas:
            print("Cliente não possui conta.")
            return
        valor = float(input("Valor: "))
        transacao = operacao_cls(valor)
        cliente.realizar_transacao(cliente.contas[0], transacao)

    def exibir_extrato(self):
        cpf = input("CPF do titular: ")
        cliente = self.buscar_cliente(cpf)
        if not cliente or not cliente.contas:
            print("Conta não encontrada.")
            return
        conta = cliente.contas[0]
        print(f"\nExtrato da Conta {conta._numero}:")
        for t in conta.historico.transacoes:
            tipo = t.__class__.__name__
            print(f"{tipo}: R$ {t.valor:.2f}")
        print(f"Saldo atual: R$ {conta._saldo:.2f}")

if __name__ == "__main__":
    banco = Banco()
    banco.menu()

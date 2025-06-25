menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[4] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
valor_saque = 0
valor_deposito = 0



while True:

    opcao = input(menu)

    if opcao == "1":
        valor_deposito = float(input("Informe o valor do depósito: "))
        if valor_deposito <= 0:
            print("Valor informado é invalido")
                
        elif valor_deposito > 0 :
            saldo = saldo + valor_deposito
            extrato += f"Deposito: R$ {valor_deposito: .2f}\n"
            print(f"Deposito de R${valor_deposito} efetuado com sucesso")



    elif opcao == "2":
        valor_saque = int(input("Informe o valor do saque: "))
        if valor_saque <= 0:
              print(f"Valor inválido")  
        elif numero_saques > LIMITE_SAQUES:
              print(f"Não é possivel efetuar saque, limite excedido")
        elif valor_saque >= saldo:
             print("Não há saldo suficiente para saque")
        elif valor_saque<= saldo:
             numero_saques += 1
             saldo = saldo - valor_saque
             extrato += f"Saque: R$ {valor_saque: .2f}\n"
             print(f"Saque no valor de R${valor_saque} concluido")
      
    elif opcao == "3":
        print("********Extrato********")
        print(f"Seu saldo atual é de R${saldo:.2f}")
        print("******Movimentações*****")
        print("Não houve movimentações" if not extrato else extrato)

    elif opcao == "4":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")


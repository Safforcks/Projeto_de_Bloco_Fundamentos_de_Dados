from datetime import datetime
from tabulate import tabulate

headers_cliente = ["Cliente", "Total"]

def fechamento_caixa(lista_clientes):
    print()
    print("Fechamento do caixa")
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M"); 
    print(f"Data: {data_atual}")
    print()

    if lista_clientes == []:
        print("Nenhum cliente atendido.")
        return
    
    print(tabulate(lista_clientes, headers_cliente, tablefmt="grid"))

    print()
    print(f"Total de vendas: {sum(total[1] for total in lista_clientes)}")
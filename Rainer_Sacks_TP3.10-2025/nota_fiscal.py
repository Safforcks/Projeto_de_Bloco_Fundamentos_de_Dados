from datetime import datetime
from tabulate import tabulate

headers_antedimento = ["Item", "Produto", "Quant.", "Preço", "Total"]

def nota_fiscal(lista_produtos):

    for x, index_cliente in enumerate(lista_produtos, start=1):

        print()
        print(f"Cliente {x}")
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M"); 
        print(f"Data: {data_atual}" )
        print()

        print(tabulate(index_cliente, headers_antedimento, tablefmt="grid", showindex=False))

        print()
        print(f"Itens: {len(index_cliente)}")
        print(f"Total: {sum(produto[4] for produto in index_cliente)}")
        print()
        print("-"*50)
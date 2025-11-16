import pandas as pd

from nota_fiscal import nota_fiscal
from fechamento_caixa import fechamento_caixa
from sem_estoque import sem_estoque


headers_antedimento = ["Item", "Produto", "Quant.", "Preço", "Total"]
headers_cliente = ["Cliente", "Total"]

df = pd.read_csv("produtos.csv", header=None, names=headers_antedimento[:-1]) # [:-1] --> todos os elementos da lista, menos o último ("Total)

df["Total"] = 0


def antedimento(df, id_cliente=0):
    lista_clientes = []
    lista_produtos = []
    numero = id_cliente

    while True:
        
        atendimento_inicial = str(input("\nDigite 'sim' para iniciar o atendimento ou 'não' para finalizar o atendimento: ").lower().strip())
        
        if atendimento_inicial in ("sim", "s"):
            numero += 1
            lista_produtos_sub = []
            item_id = 0

            while True:
                
                resposta = input("Número do produto entre 1 e 5/Enter para fechar a lista de compras: ").strip()

                # Enter fecha a lista do cliente
                if resposta == "":
                    print("\nFechamento da lista de compras")
                    break

                # valida id do produto
                try:
                    produto = int(resposta)
                except ValueError:
                    print("\nErro: valor inválido.")
                    continue

                if produto > 5 or produto < 1:
                    print("\nErro: o número deve estar entre 1 e 5.")
                    continue

                # quantidade
                try:
                    qtd = int(input("\nQuantidade: "))
                except:
                    print("\nErro: quantidade inválida.")
                    continue
                        
                if qtd <= 0:
                    print("\nErro: quantidade deve ser maior que zero.")
                    continue
                        

                index = produto - 1

                # checar estoque disponível
                if df.at[index ,"Quant."] < qtd:
                    print(f"Não tem mais de {df.at[index, 'Quant.']}")
                    continue

                # baixa no estoque
                df.at[index, "Quant."] -= qtd

                # dados do produto
                produto_val = df.at[index, "Produto"]
                preco = df.at[index, "Preço"]
                total = preco * qtd

                # id sequencial do item do carrinho
                item_id += 1

                lista_produtos_sub.append([item_id, produto_val, qtd, preco, total])

            # final do cliente: guarda itens e total
            lista_produtos.append(lista_produtos_sub[:]) # [:] --> cria uma cópia
            df_produtos_sub = pd.DataFrame(lista_produtos_sub, columns=headers_antedimento)
            total_cliente = sum(df_produtos_sub["Total"])
            lista_clientes.append([f"Cliente {numero}", total_cliente])
            lista_produtos_sub = []
                
        elif atendimento_inicial in ("não", "nao", "n"):
            print("\nO atendimento está encerrando.\n")  
            nota_fiscal(lista_produtos)
            fechamento_caixa(lista_clientes)
            sem_estoque(df)

            # grava só id, Produto, Quant., Preço
            df_out = df[headers_antedimento[:-1]]  # só id, Produto, Quant., Preço
            df_out.to_csv("produtos.csv", header=False, index=False)
            return df, lista_produtos, lista_clientes
        
        else:
            print("Digite 'sim' ou 'não'.")
            continue

antedimento(df, id_cliente=0)

'''
15. O sistema considerou que apenas um caixa estava operando no supermercado. Cite um
problema caso houvesse mais de um caixa operando ao mesmo tempo no
supermercado?

R: No meu teste, funciona em só um caixa de atendimento. Se dois caixas usassem o mesmo programa ao mesmo tempo, o estoque ficaria errado ou negativo porque os dois caixas tirariam produtos do mesmo lugar ao mesmo tempo. Isso não funciona com vários caixas ao mesmo tempo.

16. Qual seria uma possível solução para o problema anterior considerando o conteúdo
apresentado no bloco?

R: A solução seria impedir que os dois caixas atualizam o estoque ao mesmo tempo. Cada caixa faz o carrinho normalmente na memória. Quando chega a hora de confirmar a compra, o caixa tenta criar um arquivo de trava.

Por exemplo, se o caixa conseguir criar primeiro, entra na sala de estoque, fazendo com que outro caixa não conseguesse acessar o estoque e esperasse a trava ser liberada para tentar de novo. Quando a trava for liberada, consegue atualizar depois 
'''
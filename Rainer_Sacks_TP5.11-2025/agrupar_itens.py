import pandas as pd

def agrupar_itens(itens):

    df = pd.DataFrame(itens, columns=["id_produto", "nome", "preco", "qtd", "total"])

    if df.empty:
        return df
    
    return (df.groupby(["id_produto", "nome", "preco"], as_index=False).agg(qtd=("qtd", "sum"), total=("total", "sum")))
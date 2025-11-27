import pandas as pd
from models import Sessao, Cliente 

def carregar_cliente():
    df = pd.read_json("clientes.json")

    with Sessao() as sessao:
        clentes_existentes = {c.nome for c in sessao.query(Cliente).all()}

        for _, linha in df.iterrows():
            nome = linha["nome"]
            if nome in clentes_existentes:
                continue

            cliente = Cliente(nome=nome)
            sessao.add(cliente)

        sessao.commit()

if __name__ == "__main__":
    carregar_cliente()
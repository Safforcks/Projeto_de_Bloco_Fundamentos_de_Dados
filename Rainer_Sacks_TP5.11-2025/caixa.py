from tabulate import tabulate
from typing import List, Dict
from datetime import datetime
from agrupar_itens import agrupar_itens
from typing import List, Dict
from models import sessao, Cliente, Produto, Compra, Item


def ler_arquivo(sessao):
    """Lê um produto e quantidade a partir do ID informado pelo usuário."""

    escolha = input("ID do produto (Enter para fechar): ").strip()

    if escolha == "":
        # sinal de que o cliente terminou de escolher
        return None

    try:
        numero = int(escolha)
    except ValueError:
        print("Valor inválido")
        return {}

    pro = sessao.get(Produto, int(numero))
    if not pro:
        print("Produto não encontrado.")
        return {}

    try:
        qtd = int(input("Quantidade: ").strip())
    except ValueError:
        print("Quantidade inválida.")
        return {}

    if qtd <= 0:
        print("Quantidade deve ser > 0.")
        return {}

    if pro.quantidade < qtd:
        print(f"Estoque insuficiente. Disponível: {pro.quantidade}")
        return {}

    return {
        "id_produto": pro.id_produto,
        "nome": pro.nome,
        "preco": float(pro.preco),
        "qtd": qtd,
        "total": float(pro.preco) * qtd,
    }

def criar_cliente():
    escolha = input("Informe o ID do cliente: ").strip()

    if not escolha.isdigit():
        print("ID inválido.")
        return criar_cliente()

    cliente = sessao.get(Cliente, int(escolha))

    if cliente:
        print(f"Cliente encontrado: {cliente.nome}")
        return cliente

    # não existe -> criar
    novo = Cliente(nome="") # nome temporário
    sessao.add(novo)
    sessao.flush() # gera id_cliente

    novo.nome = f"Cliente {novo.id_cliente}"
    sessao.commit()

    print(f"Cliente criado: {novo.nome}")
    return novo

def nota_fiscal(cliente, df_group):
    print("\n======= NOTA FISCAL =======")
    print(f"Cliente: {cliente.nome} ")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    tabela = []
    for _, x in df_group.iterrows():
        tabela.append([
            int(x["id_produto"]),
            x["nome"],
            int(x["qtd"]),
            f"R$ {float(x['preco']):.2f}",
            f"R$ {float(x['total']):.2f}",
        ])

    print(tabulate(
        tabela,
        headers=["ID", "Produto", "Qtd", "Preço", "Total"],
        tablefmt="grid"
    ))

    total = float(df_group["total"].sum())
    print(f"Total: R$ {total:.2f}")
    print("===========================\n")

def antedimento(sessao):
    while True:
        atendimento_inicial = input("\nDigite 's' para iniciar ou 'n' para encerrar: ").lower().strip()

        if atendimento_inicial in ("n", "nao", "não"):
            break
        if atendimento_inicial not in ("s", "sim"):
            print("Use 's' ou 'n'")
            continue

        cliente = criar_cliente()

        produtos = sessao.query(Produto).all()
        lista_produtos = [[p.id_produto, p.nome, p.preco, p.quantidade] for p in produtos]
        print("\n","="*35 + " PRODUTOS DISPONÍVEIS " + "="*34)
        print(tabulate(lista_produtos, headers=["ID", "Produto", "Preço", "Qtd"], tablefmt="grid"))

        itens: List[Dict] = []

        while True:
            item = ler_arquivo(sessao)

            if item is None:
                break # termina a escolha

            if item:
                itens.append(item)

        if not itens:
            print("Nenhum item selecionado. Voltando ao menu inicial.")
            continue
        
        # agrupar_itens.py 
        df_group = agrupar_itens(itens)
        total = float(df_group["total"].sum())

        compra = Compra(id_cliente=cliente.id_cliente)
        sessao.add(compra)
        sessao.flush()

        for _, it in df_group.iterrows():
            novo_item = Item(
                id_compra=compra.id_compra,
                id_produto=it["id_produto"],
                quantidade=it["qtd"],
                preco=it["preco"],
            )
            sessao.add(novo_item)

            produto = sessao.get(Produto, int(it["id_produto"]))
            produto.quantidade -= int(it["qtd"])

        sessao.commit()
        nota_fiscal(cliente, df_group)

antedimento(sessao)

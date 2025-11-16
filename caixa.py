from tabulate import tabulate
from typing import List, Dict
from nota_fiscal import nota_fiscal
from agrupar_itens import agrupar_itens
from typing import List, Dict
from models import Cliente, Produtos, sessao


headers_titulos = ["ID", "Produto", "Preço", "Quant."]

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

    pro = sessao.get(Produtos, numero)
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

    if pro.estoque < qtd:
        print(f"Estoque insuficiente. Disponível: {pro.estoque}")
        return {}

    return {
        "id_produto": pro.id_produto,
        "nome": pro.nome,
        "preco": float(pro.preco),
        "qtd": qtd,
        "total": float(pro.preco) * qtd,
    }

def criar_cliente(sessao):
    escolha = input("Informe o ID do cliente: ").strip()

    if not escolha.isdigit():
        print("ID inválido.")
        return criar_cliente(sessao)

    id_cliente = int(escolha)
    cli = sessao.get(Cliente, id_cliente)

    if cli:
        print(f"Cliente encontrado: {cli.nome}")
        return cli

    # não existe -> criar
    novo = Cliente(nome="") # nome temporário
    sessao.add(novo)
    sessao.flush() # gera id_cliente

    novo.nome = f"Cliente {novo.id_cliente}"
    sessao.commit()

    print(f"Cliente criado: {novo.nome}")
    return novo

def baixar_estoque(sessao, df_group):
    for _, row in df_group.iterrows():
        prod_id = int(row["id_produto"]) 
        qtd = int(row["qtd"])

        produto = sessao.get(Produtos, prod_id)
        if not produto:
            print(f"Produto {prod_id} não encontrado ao dar baixa.")
            continue

        if produto.estoque < qtd:
            print(f"Estoque insuficiente para {produto.nome}. Disponível: {produto.estoque}")
            continue

        produto.estoque -= qtd

    sessao.commit()
    print("Estoque atualizado após a compra.")

def antedimento(sessao):
    while True:
        atendimento_inicial = input("\nDigite 's' para iniciar ou 'n' para encerrar: ").lower().strip()

        if atendimento_inicial in ("n", "nao", "não"):
            break
        if atendimento_inicial not in ("s", "sim"):
            print("Use 's' ou 'n'")
            continue

        cliente = criar_cliente(sessao)

        produtos = sessao.query(Produtos).all()
        lista_produtos = [[p.id_produto, p.nome, p.preco, p.estoque] for p in produtos]
        print("\n","="*35 + " PRODUTOS DISPONÍVEIS " + "="*34)
        print(tabulate(lista_produtos, headers_titulos, tablefmt="grid"))

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

        # nota_fiscal.py
        nota_fiscal(cliente, df_group)

        baixar_estoque(sessao, df_group)


antedimento(sessao)

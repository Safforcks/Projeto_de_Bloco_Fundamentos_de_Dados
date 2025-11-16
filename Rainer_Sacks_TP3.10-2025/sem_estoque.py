def sem_estoque(df):
    print("-"*50)
    print()

    # Cria uma lista apenas com os produtos cujo estoque é zero
    produtos_sem_estoque = df[df["Quant."] == 0]["Produto"].tolist() # tolist() --> converte uma coluna em uma lista comum

    if not produtos_sem_estoque:
        print("Não tem produtos sem estoque.")
    else:
        print("Produtos sem estoque:")
        for nome in produtos_sem_estoque:
            print(nome)
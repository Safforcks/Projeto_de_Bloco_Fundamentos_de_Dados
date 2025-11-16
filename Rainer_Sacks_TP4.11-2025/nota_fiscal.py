from datetime import datetime


def nota_fiscal(cliente, df_group):
    print("\n======= NOTA FISCAL =======")
    print(f"Cliente: {cliente.nome} ")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    if df_group.empty:
        print("Nenhum item.")
        return
    
    print(f"Itens: {len(df_group)}")
    print(f"Total: R$ {df_group['total'].sum():.2f}")
    print("===========================\n")





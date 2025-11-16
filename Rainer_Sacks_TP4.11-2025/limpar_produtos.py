from models import sessao, Produtos

sessao.query(Produtos).delete()
sessao.commit()

print("Tabela produto esvaziada com sucesso.")

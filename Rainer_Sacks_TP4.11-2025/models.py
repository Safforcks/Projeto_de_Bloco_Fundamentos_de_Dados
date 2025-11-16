from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Base(DeclarativeBase):
    pass

class Cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)



class Produtos(Base):
    __tablename__ = "produto"
    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    estoque = Column(Integer, nullable=False)

engine = create_engine("sqlite:///supermercado.db")
Sessao = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
sessao = Sessao()
Base.metadata.create_all(engine)

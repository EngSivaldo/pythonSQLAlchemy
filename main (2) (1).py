from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Configurando o banco de dados e a sessão
db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

# Definindo a tabela Usuario
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)
    ativo = Column(Boolean)

    def __init__(self, nome, email, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

# Definindo a tabela Livro
class Livro(Base):
    __tablename__ = "livros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String)
    qtde_paginas = Column(Integer)
    dono = Column(Integer, ForeignKey("usuarios.id"))

    def __init__(self, titulo, qtde_paginas, dono):
        self.titulo = titulo
        self.qtde_paginas = qtde_paginas
        self.dono = dono

# Criando as tabelas no banco de dados
Base.metadata.create_all(bind=db)

# Operações CRUD

# C - Create (Criar)
# usuario = Usuario(nome="gute", email="gute2@email.com", senha="123123")
# session.add(usuario)  # Adiciona no banco
# session.commit()  # Salva no banco

# R - Read (Ler)
# lista_usuarios = session.query(Usuario).all()
# print(lista_usuarios)  # Isso deve funcionar corretamente



usuario_lira = session.query(Usuario).filter_by(id="11").first()
print(usuario_lira) 

# print(usuario_lira.nome) 
# print(usuario_lira.email) 

# livro = Livro(titulo="Nome da Montanha", qtde_paginas=1000, dono=usuario_lira.id)
# session.add(livro)
# session.commit()

# U - Update
# usuario_lira.nome = "Joao Lira"
# session.add(usuario_lira)
# session.commit()

# D - Delete
session.delete(usuario_lira)
session.commit()



# Fechando a sessão
session.close()
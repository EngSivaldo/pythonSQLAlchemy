from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, func
from sqlalchemy.orm import sessionmaker, declarative_base

# Definir a conexão com o banco de dados e a sessão
db = create_engine("sqlite:///meubanco.db")
Session = sessionmaker(bind=db)
session = Session()

# Definir a classe base
Base = declarative_base()

# Definir a tabela Usuario
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    email = Column(String, unique=True)
    senha = Column(String)
    ativo = Column(Boolean, default=True)

    def __init__(self, nome, email, senha, ativo=True):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo

# Definir a tabela Livro
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

# Criar as tabelas
Base.metadata.create_all(bind=db)

# Função para deletar duplicados de usuários
def deletar_usuarios_duplicados():
    subquery = session.query(
        Usuario.email,
        func.count(Usuario.id).label('count')
    ).group_by(Usuario.email).having(func.count(Usuario.id) > 1).subquery()
    
    duplicados = session.query(Usuario).join(subquery, Usuario.email == subquery.c.email).all()
    
    for usuario in duplicados[1:]:  # Mantém o primeiro usuário e deleta os restantes
        session.delete(usuario)
    session.commit()

# Função para deletar duplicados de livros
def deletar_livros_duplicados():
    subquery = session.query(
        Livro.titulo,
        Livro.dono,
        func.count(Livro.id).label('count')
    ).group_by(Livro.titulo, Livro.dono).having(func.count(Livro.id) > 1).subquery()
    
    duplicados = session.query(Livro).join(subquery, (Livro.titulo == subquery.c.titulo) & (Livro.dono == subquery.c.dono)).all()
    
    for livro in duplicados[1:]:  # Mantém o primeiro livro e deleta os restantes
        session.delete(livro)
    session.commit()

# Chamando as funções para deletar duplicados
deletar_usuarios_duplicados()
deletar_livros_duplicados()

# Consultar o banco de dados para verificar
for livro in session.query(Livro).all():
    print(livro.titulo, livro.qtde_paginas, livro.dono)
for usuario in session.query(Usuario).all():
    print(usuario.nome, usuario.email, usuario.ativo)
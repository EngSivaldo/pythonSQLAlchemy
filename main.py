import tkinter as tk
from tkinter import ttk, messagebox
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

# Funções de banco de dados
def inserir_usuario(nome, email, senha):
    usuario_existente = session.query(Usuario).filter_by(email=email).first()
    if not usuario_existente:
        novo_usuario = Usuario(nome=nome, email=email, senha=senha)
        session.add(novo_usuario)
        session.commit()
        messagebox.showinfo("Sucesso", f"Novo usuário {nome} criado.")
        return novo_usuario
    else:
        messagebox.showinfo("Aviso", f"Usuário {nome} já existe no banco de dados.")
        return usuario_existente

def inserir_livro(titulo, qtde_paginas, dono_id):
    livro_existente = session.query(Livro).filter_by(titulo=titulo, qtde_paginas=qtde_paginas, dono=dono_id).first()
    if not livro_existente:
        novo_livro = Livro(titulo=titulo, qtde_paginas=qtde_paginas, dono=dono_id)
        session.add(novo_livro)
        session.commit()
        messagebox.showinfo("Sucesso", f"Novo livro '{titulo}' criado.")
        return novo_livro
    else:
        messagebox.showinfo("Aviso", f"Livro '{titulo}' já existe no banco de dados.")
        return livro_existente

def deletar_livros_duplicados():
    duplicados = session.query(
        Livro.titulo,
        Livro.qtde_paginas,
        func.count(Livro.id).label('count')
    ).group_by(Livro.titulo, Livro.qtde_paginas).having(func.count(Livro.id) > 1).all()

    for duplicado in duplicados:
        livros = session.query(Livro).filter_by(titulo=duplicado.titulo, qtde_paginas=duplicado.qtde_paginas).all()
        for livro in livros[1:]:  # Mantém o primeiro livro e deleta os restantes
            session.delete(livro)
    session.commit()
    messagebox.showinfo("Sucesso", "Livros duplicados deletados.")

def listar_livros():
    livros = session.query(Livro).all()
    return livros

def listar_usuarios():
    usuarios = session.query(Usuario).all()
    return usuarios

def pesquisar_livro(titulo):
    livros = session.query(Livro).filter(Livro.titulo.like(f"%{titulo}%")).all()
    return livros

def pesquisar_usuario(nome):
    usuarios = session.query(Usuario).filter(Usuario.nome.like(f"%{nome}%")).all()
    return usuarios

# Funções de interface gráfica
def adicionar_usuario():
    nome = nome_usuario_entry.get()
    email = email_usuario_entry.get()
    senha = senha_usuario_entry.get()
    inserir_usuario(nome, email, senha)
    atualizar_lista_usuarios()

def adicionar_livro():
    titulo = titulo_livro_entry.get()
    qtde_paginas = int(paginas_livro_entry.get())
    dono_email = dono_livro_entry.get()
    dono = session.query(Usuario).filter_by(email=dono_email).first()
    
    if dono:
        messagebox.showinfo("Sucesso", f"Dono encontrado: {dono.nome}")
        inserir_livro(titulo, qtde_paginas, dono.id)
        atualizar_lista_livros()
    else:
        messagebox.showwarning("Aviso", f"Dono não encontrado. Certifique-se de que o usuário está cadastrado. E-mail buscado: {dono_email}")


def atualizar_lista_livros():
    livros = listar_livros()
    livros_listbox.delete(0, tk.END)
    for livro in livros:
        livros_listbox.insert(tk.END, f"ID: {livro.id}, Título: {livro.titulo}, Páginas: {livro.qtde_paginas}, Dono ID: {livro.dono}")

def atualizar_lista_usuarios():
    usuarios = listar_usuarios()
    usuarios_listbox.delete(0, tk.END)
    for usuario in usuarios:
        usuarios_listbox.insert(tk.END, f"ID: {usuario.id}, Nome: {usuario.nome}, Email: {usuario.email}, Ativo: {usuario.ativo}")

def pesquisar_livro_interface():
    titulo = titulo_pesquisa_entry.get()
    livros = pesquisar_livro(titulo)
    livros_listbox.delete(0, tk.END)
    for livro in livros:
        livros_listbox.insert(tk.END, f"ID: {livro.id}, Título: {livro.titulo}, Páginas: {livro.qtde_paginas}, Dono ID: {livro.dono}")

def pesquisar_usuario_interface():
    nome = nome_pesquisa_entry.get()
    usuarios = pesquisar_usuario(nome)
    usuarios_listbox.delete(0, tk.END)
    for usuario in usuarios:
        usuarios_listbox.insert(tk.END, f"ID: {usuario.id}, Nome: {usuario.nome}, Email: {usuario.email}, Ativo: {usuario.ativo}")

# Criação da janela principal
root = tk.Tk()
root.title("Gerenciamento de Livros e Usuários")

# Frames
frame_usuarios = ttk.Frame(root, padding="10")
frame_livros = ttk.Frame(root, padding="10")
frame_pesquisa = ttk.Frame(root, padding="10")
frame_usuarios.grid(row=0, column=0, sticky="nsew")
frame_livros.grid(row=1, column=0, sticky="nsew")  # Alterado para ficar abaixo do frame de usuários
frame_pesquisa.grid(row=2, column=0, sticky="nsew")  # Alterado para ficar abaixo do frame de livros

# Frame de usuários
ttk.Label(frame_usuarios, text="Adicionar Usuário").grid(row=0, column=0, columnspan=2)
ttk.Label(frame_usuarios, text="Nome:").grid(row=1, column=0)
nome_usuario_entry = ttk.Entry(frame_usuarios)
nome_usuario_entry.grid(row=1, column=1)
ttk.Label(frame_usuarios, text="Email:").grid(row=2, column=0)
email_usuario_entry = ttk.Entry(frame_usuarios)
email_usuario_entry.grid(row=2, column=1)
ttk.Label(frame_usuarios, text="Senha:").grid(row=3, column=0)
senha_usuario_entry = ttk.Entry(frame_usuarios, show="*")
senha_usuario_entry.grid(row=3, column=1)
ttk.Button(frame_usuarios, text="Adicionar Usuário", command=adicionar_usuario).grid(row=4, column=0, columnspan=2)

# Listbox de usuários
usuarios_listbox = tk.Listbox(frame_usuarios, height=10, width=50)
usuarios_listbox.grid(row=5, column=0, columnspan=2, pady=10)
ttk.Button(frame_usuarios, text="Listar Usuários", command=atualizar_lista_usuarios).grid(row=6, column=0, columnspan=2)

# Frame de livros
ttk.Label(frame_livros, text="Adicionar Livro").grid(row=0, column=0, columnspan=2)
ttk.Label(frame_livros, text="Título:").grid(row=1, column=0)
titulo_livro_entry = ttk.Entry(frame_livros)
titulo_livro_entry.grid(row=1, column=1)
ttk.Label(frame_livros, text="Páginas:").grid(row=2, column=0)
paginas_livro_entry = ttk.Entry(frame_livros)
paginas_livro_entry.grid(row=2, column=1)
ttk.Label(frame_livros, text="Email do Dono:").grid(row=3, column=0)
dono_livro_entry = ttk.Entry(frame_livros)
dono_livro_entry.grid(row=3, column=1)

# Configuração do estilo personalizado para o botão
style = ttk.Style()
style.configure("My.TButton", foreground="white", background="blue", font=("Helvetica", 12, "bold"), padding=10)

ttk.Button(frame_livros, text="Adicionar Livro", command=adicionar_livro, style="My.TButton").grid(row=4, column=0, columnspan=2)

root.mainloop()



root.mainloop()










# CRUD

# C - Create
# usuario = Usuario(nome="sivaldo", email="sivaldo@email.com", senha="124124")
# session.add(usuario)
# session.commit()

# R - READ
# lista_usuarios = session.query(Usuario).all()
# print(lista_usuarios[3])
# usuario_lira2 = session.query(Usuario).filter_by(email="qlqcoisa2@email.com").first()
# print(usuario_lira2) 
# print(usuario_lira2.nome) 
# print(usuario_lira2.email) 

# livro = Livro(titulo="Nome do Vento", qtde_paginas=1000, dono=usuario_lira.id)
# session.add(livro)
# session.commit()

# U - Update
# usuario_lira.nome = "Joao Lira"
# session.add(usuario_lira)
# session.commit()

# D - Delete
# session.delete(usuario_lira2)
# session.commit()
from models import Livros, Autor, Emprestimo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///db_livros.db")

Session = sessionmaker(bind=db)
session = Session()


def listar_livros():
    livros = session.query(Livros).all()
    print(livros)
    

def listar_livros_autor():
    nome = input("Digita ai um autor: ")
    # Esse sessiion query e diferente pois usamos o relacionamento do campo muitos-para-muitos formando uma clase de list
    lista = session.query(Livros).filter(Livros.autores.any(Autor.nome == nome)).all()
    print(lista)


def registrar_emprestimo_devolucao():
    livro_nome = input("Qual Livro você deseja? ")
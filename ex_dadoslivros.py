from models import Livros, Autor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///db_livros.db")

Session = sessionmaker(bind=db)
session = Session()

autor = session.query(Autor).filter_by(nome="J.K. Rowling").first()
autor2 = session.query(Autor).filter_by(nome="George R.R. Martin").first()
autor3 = session.query(Autor).filter_by(nome="J.R.R. Tolkien").first()




# Livros de J.R.R. Tolkien
livro1 = Livros(nome="O Senhor dos Anéis", autores=[autor3], disponivel=True)
livro2 = Livros(nome="O Hobbit", autores=[autor3], disponivel=True)
livro3 = Livros(nome="Silmarillion", autores=[autor3], disponivel=True)

# Livros de George R.R. Martin
livro4 = Livros(nome="A Game of Thrones", autores=[autor2], disponivel=True)
livro5 = Livros(nome="A Clash of Kings", autores=[autor2], disponivel=True)
livro6 = Livros(nome="A Storm of Swords", autores=[autor2], disponivel=True)

session.add_all([livro1,livro2,livro3,livro4,livro5,livro6])
session.commit()

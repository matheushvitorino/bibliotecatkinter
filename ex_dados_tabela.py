from models import Autor
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = create_engine("sqlite:///db_livros.db")

Session = sessionmaker(bind=db)
session = Session()


# Criando instâncias de autores
autor1 = Autor(nome="J.K. Rowling")
autor2 = Autor(nome="George R.R. Martin")
autor3 = Autor(nome="J.R.R. Tolkien")

# Salvando no banco de dados
session.add_all([autor1, autor2, autor3])
session.commit()




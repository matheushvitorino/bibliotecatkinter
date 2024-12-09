from sqlalchemy import create_engine, Column, Integer, String, Boolean,ForeignKey, Table
from sqlalchemy.orm import sessionmaker,declarative_base,relationship



#Criação do banco e sessão
db = create_engine("sqlite:///db_livros.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

#Criação de tabelas
class Autor(Base):
    __tablename__ = "autor"
    id = Column(Integer, primary_key =True, autoincrement= True)
    nome = Column(String(255))
    livros = relationship("Livros", secondary="autor_livros", back_populates="autores",)
    
    def __init__(self, nome):
        self.nome = nome
        
    def __str__(self):
        return f"{self.nome}"
    
    def __repr__(self):
        return f"{self.nome}" 
    


class Livros(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key =True, autoincrement= True)
    nome = Column(String(255))    
    autores = relationship("Autor", secondary="autor_livros",back_populates="livros")
    
    disponivel = Column(Boolean, default=True)
    
    def __init__(self,nome,autores,disponivel):
        self.nome = nome
        self.autores = autores
        self.disponivel = disponivel
        
    def __str__(self):
        return f"Livro: {self.nome}\nAutor: {self.autores}\nDisponivel: {self.disponivel}"

    def __repr__(self):
        return f"Livro: {self.nome}\n Autor: {self.autores}\n Disponivel: {self.disponivel}"

   # Tabela de relacionamento    
autor_livros = Table( 
    "autor_livros",Base.metadata,   
    Column("autor_id", Integer, ForeignKey("autor.id"), primary_key =True),    
    Column("livro_id", Integer, ForeignKey("livros.id"), primary_key =True)
)

Base.metadata.create_all(bind=db)


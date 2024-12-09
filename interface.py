from tkinter import *
from tkinter import ttk
import tkinter as tk
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Livros, Autor

root = Tk()

class Funcs():
    def limpa_campos(self):
        self.entrada_titulo.delete(0, END)
        self.entrada_autor.delete(0, END)
        self.entrada_busca.delete(0, END)
    
    def conecta_banco(self):
        self.db = create_engine("sqlite:///db_livros.db")
        self.Session = sessionmaker(bind=self.db)
        self.session = self.Session()
    
    def selecionar_campo(self, event):
        self.limpa_campos()
        self.lista_livros.selection()
        
        for n in self.lista_livros.selection():
            col1, col2, col3, col4 = self.lista_livros.item(n, 'values')
            self.id = col1
            self.entrada_titulo.insert(END, col2)
            self.entrada_autor.insert(END, col3)
        
    def desconecta_banco(self):
        self.session.close()
        self.db.dispose()

    def get_livro(self):
        self.titulo = self.entrada_titulo.get()
        self.autor = self.session.query(Autor).filter_by(nome=self.entrada_autor.get()).first()
        self.entrada_autorget = self.entrada_autor.get()
        self.disponivel_string = self.disponibilidade.get()
        self.disponivel = True if self.disponivel_string == "Disponivel" else False
    
    def listar_livros(self):
        self.lista_livros.delete(*self.lista_livros.get_children())
        self.conecta_banco()
        lista = self.session.query(Livros).all()
        for livro in lista:
            disponibilidade = "Disponível" if livro.disponivel else "Indisponível"
            self.lista_livros.insert("", END,
                                     values=(livro.id,
                                             livro.nome,
                                             ", ".join([autor.nome for autor in livro.autores]),
                                             disponibilidade))
        self.desconecta_banco()

    def adicionar_livro(self):
        self.get_livro()
        novo_livro = Livros(nome=self.titulo, autores=[self.autor], disponivel=self.disponivel)
        self.session.add(novo_livro)
        self.session.commit()
        self.listar_livros()
        self.limpa_campos()
    
    def adicionar_autor(self):
        self.get_livro()
        novo_autor = Autor(nome=self.entrada_autorget)
        self.session.add(novo_autor)
        self.session.commit()
        self.listar_livros()
        self.limpa_campos()
    

    def deletar_livro(self):
        self.selecionar_campo(None)
        livro_id = self.id
        livro = self.session.query(Livros).filter_by(id=livro_id).first()
        if livro:
            self.session.delete(livro)
            self.session.commit()
            self.desconecta_banco()
            self.listar_livros()
            self.limpa_campos()
            
    def editar_livro(self):
        livro_id = self.id
        livro = self.session.query(Livros).filter_by(id=livro_id).first()
        if livro:
            livro.nome = self.entrada_titulo.get()
            autor = self.session.query(Autor).filter_by(nome=self.entrada_autor.get()).first()
            if autor:
                livro.autores = [autor]
            
            self.disponivel_string = self.disponibilidade.get()
            livro.disponivel = True if self.disponivel_string == "Disponivel" else False

            self.session.commit()
            self.desconecta_banco()
            self.listar_livros()
            self.limpa_campos()
            
    def busca_livro(self):
        termo_pesquisado = self.entrada_busca.get().lower()
        self.limpa_campos()
        self.lista_livros.delete(*self.lista_livros.get_children())
        self.conecta_banco()
        lista = self.session.query(Livros).join(Livros.autores).filter(
            (Livros.nome.ilike(f"%{termo_pesquisado}%")) |
            (Autor.nome.ilike(f"%{termo_pesquisado}%"))
            
        )
        for livro in lista:
            self.lista_livros.insert("", END,
                                     values=(livro.id,
                                             livro.nome,
                                             ", ".join([autor.nome for autor in livro.autores]),
                                             livro.disponivel))

class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames()
        self.widgets_frame1()
        self.widgets_frame2()
        self.listar_livros()
        root.mainloop()
        
    def tela(self):
        self.root.title("Sistema da biblioteca")
        self.root.configure(background="white")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        
    def frames(self):
        self.frame1 = Frame(self.root, highlightbackground="gray", highlightthickness=1)
        self.frame1.place(relx=0.01, rely=0.05, relwidth=0.98, relheight=0.44)
        
        self.frame2 = Frame(self.root, highlightbackground="gray", highlightthickness=1)
        self.frame2.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.49)
        
    def widgets_frame1(self):
        self.label_titulo = Label(self.frame1, text="SISTEMA BIBLIOTECA", font=('serdana', 12, 'bold'))
        self.label_titulo.place(relx=0.37, rely=0.02)
        
        self.entrada_titulo = Entry(self.frame1)
        self.entrada_titulo.place(relx=0.08, rely=0.2, relwidth=0.4)
        self.label_titulo = Label(self.frame1, text="Título")
        self.label_titulo.place(relx=0.02, rely=0.2)
        
        self.entrada_autor = Entry(self.frame1)
        self.entrada_autor.place(relx=0.08, rely=0.4, relwidth=0.4)
        self.label_autor = Label(self.frame1, text="Autor")
        self.label_autor.place(relx=0.02, rely=0.4)
        
        self.botao_adicionar_livro = Button(self.frame1, text="Adicionar Livro", command=self.adicionar_livro)
        self.botao_adicionar_livro.place(relx=0.37, rely=0.6)
        
        self.botao_adicionar_autor = Button(self.frame1, text="Adicionar Autor", command=self.adicionar_autor)
        self.botao_adicionar_autor.place(relx=0.37, rely=0.8) 
               
        self.botao_editar = Button(self.frame1, text="Editar", command=self.editar_livro)
        self.botao_editar.place(relx=0.27, rely=0.6)

        self.botao_deletar = Button(self.frame1, text="Deletar", command=self.deletar_livro)
        self.botao_deletar.place(relx=0.17, rely=0.6)
        
        self.entrada_busca = Entry(self.frame1)
        self.entrada_busca.place(relx=0.58, rely=0.4, relwidth=0.4)
        self.label_busca = Label(self.frame1, text="Buscar por titulo/autor:")
        self.label_busca.place(relx=0.58, rely=0.25)
        self.botao_buscar = Button(self.frame1, text="Buscar",command=self.busca_livro)
        self.botao_buscar.place(relx=0.58, rely=0.6)
        
        self.disponibilidade = StringVar(value="Disponivel")
        self.disponivel = Radiobutton(self.frame1, text="Disponivel", variable=self.disponibilidade, value="Disponivel")
        self.disponivel.place(relx=0.58, rely=0.8)
        self.indisponivel = Radiobutton(self.frame1, text="Indisponivel", variable=self.disponibilidade, value="Indisponivel")
        self.indisponivel.place(relx=0.78, rely=0.8)
        
        self.botao_atualizar = Button(self.frame1, text="Atualizar",command=self.listar_livros)
        self.botao_atualizar.place(relx=0.68, rely=0.6)

    def widgets_frame2(self):
        self.lista_livros = ttk.Treeview(self.frame2,height=4,columns=("col1","col2","col3","col4"))
        
        #Cabeçalho 
        self.lista_livros.heading("#0", text="#")
        self.lista_livros.heading("#1", text="Id")
        self.lista_livros.heading("#2", text="Título")
        self.lista_livros.heading("#3", text="Autor")
        self.lista_livros.heading("#4", text="Disponibilidade")
        
        self.lista_livros.column("#0", width=1)
        self.lista_livros.column("#1", width=25)
        self.lista_livros.column("#2", width=200)
        self.lista_livros.column("#3", width=200)
        self.lista_livros.column("#4", width=100)
        
        self.lista_livros.place(relx=0.01,rely=0.1, relwidth=0.95, relheight=0.85)
        self.lista_livros.bind("<Double-1>", self.selecionar_campo)
Application()

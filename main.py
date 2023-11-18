from tkinter import *
from produto import Produto
p = Produto(id='',nome='',desc='',preco='')
app = Tk()
app.geometry('300x300')
bt_cad = Button(app, text="Cadastrar", command=p.cad_produto)
bt_sair = Button(app, text="Sair", command=exit)
bt_mostrar_produto = Button(app, text="Produtos", command=p.mostrar_produto)
bt_mostrar_id = Button(app, text="Produto", command=p.mostrar_id)
bt_mostrar_nome = Button(app, text="Produto por Nome", command=p.mostrar_nome)
bt_editar = Button(app, text="Editar", command=p.editar_id)
bt_deletar = Button(app, text="Deletar", command=p.deletar_id)
bt_deletar.pack()
bt_mostrar_nome.pack()
bt_mostrar_id.pack()
bt_cad.pack()
bt_mostrar_produto.pack()
bt_editar.pack()
bt_sair.pack()
app.mainloop()
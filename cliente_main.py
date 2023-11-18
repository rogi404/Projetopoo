import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QFileDialog
from PyQt6.QtGui import QPixmap
from PyQt6 import uic
from cliente_form import Ui_cliente

class Cliente_main(QWidget):
    def __init__(self):
        super().__init__()
        self.ui =uic.loadUi('cliente_form.ui', self)
        self.escolher_produto()
        self.bt_inserir.clicked.connect(self.inserir_cli)
        self.bt_foto.clicked.connect(self.inserir_ft)
        self.local_foto = None
        self.bt_buscar.clicked.connect(self.buscar)
        self.bt_editar.clicked.connect(self.editar)
        self.bt_excluir.clicked.connect(self.excluir)
        self.show()

    def escolher_produto(self):
        conn = sqlite3.connect('lojapoo.sqlite3')
        cursor = conn.cursor()
        cursor.execute("SELECT nome_produto FROM produto")
        produtos = [row[0] for row in cursor.fetchall()]
        conn.close()
        self.cb_produto.addItem("Escolha um produto")
        self.cb_produto.addItems(produtos)

    def inserir_cli(self):
        try:
            nome = self.lineEdit_nome.text()
            cpf = self.lineEdit_cpf.text()
            produto = self.cb_produto.currentText()

            if not nome or not cpf or not produto:
                self.label_msg.setText("Por favor, preencha todos os campos.")
            else:
                conn = sqlite3.connect('lojapoo.sqlite3')
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO cliente (nome_cliente, cpf_cliente, foto_cliente, id_produto) VALUES (?, ?, ?, ?)",
                    (nome, cpf, self.local_foto, produto))
                conn.commit()
                self.ui.label_msg.setText(f"O cliente {nome} foi inserido com sucesso!")
                conn.close()
                self.limpar()
        except Exception as e:
            print(f"Erro! Não foi possível inserir o cliente: {str(e)}")
            self.limpar()

    def inserir_ft(self):
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Inserir foto", "", "Imagens (*.jpg *.png *.jpeg *.bmp);;Todos os Arquivos (*)")
            if file_path:
                pixmap = QPixmap(file_path)
                self.lb_foto.setPixmap(pixmap)
                self.lb_foto.setScaledContents(True)
                self.local_foto = file_path

        except Exception as e:
            print(f"Erro! Não foi possível carregar a foto: {str(e)}")

    def buscar(self):
        busca = self.ui.lineEdit_buscar.text()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            if busca.isdigit():
                cursor.execute("SELECT * FROM cliente WHERE id_cliente == ?", (int(busca),))
            else:
                cursor.execute("SELECT * FROM cliente WHERE nome_cliente == ?", (busca,))
            b = cursor.fetchone()
            if b is not None:
                self.ui.lineEdit_nome.setText(b[1])
                self.ui.lineEdit_cpf.setText(b[3])
                self.ui.cb_produto.setCurrentText(b[4])
                local_foto = b[2]
                if local_foto:
                    pixmap = QPixmap(local_foto)
                    self.ui.lb_foto.setPixmap(pixmap)
                    self.ui.lb_foto.setScaledContents(True)
                else:
                    self.ui.lb_foto.setPixmap(QPixmap())
            else:
                self.ui.label_msg.setText("Não foi possível encontrar o cliente!")
            con.close()
        except Exception as e:
            print(f"Erro! Não foi possível buscar o cliente: {str(e)}")

    def editar(self):
        cod = self.ui.lineEdit_buscar.text()
        nome = self.ui.lineEdit_nome.text()
        cpf = self.ui.lineEdit_cpf.text()
        produto = self.ui.cb_produto.currentText()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute("""UPDATE cliente SET nome_cliente = ?, cpf_cliente = ?, id_produto = ?
            WHERE id_cliente = ?""", (nome, cpf, produto, int(cod)))
            con.commit()
            con.close()
            self.ui.label_msg.setText("O cliente foi editado com sucesso!")
            self.limpar()
        except Exception as e:
            self.ui.label_msg.setText(f"Erro! Não foi possível editar o cliente: {str(e)}")

    def excluir(self):
        cod = self.ui.lineEdit_buscar.text()
        try:
            con = sqlite3.connect('lojapoo.sqlite3')
            cursor = con.cursor()
            cursor.execute("DELETE FROM cliente WHERE id_cliente = ?", (int(cod),))
            con.commit()
            con.close()
            self.ui.label_msg.setText("O cliente foi excluído com sucesso!")
            self.limpar()
        except Exception as e:
            self.ui.label_msg.setText(f"Erro! Não foi possível excluir o cliente: {str(e)}")

    def limpar(self):
        self.ui.lineEdit_nome.setText("")
        self.ui.lineEdit_cpf.setText("")
        self.ui.lb_foto.setPixmap(QPixmap())
        self.ui.lineEdit_foto.setText("")
        self.ui.cb_produto.setCurrentIndex(0)

if __name__=='__main__':
    janela = QApplication(sys.argv)
    app = Cliente_main()
    sys.exit(janela.exec())
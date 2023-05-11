from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QComboBox, QLabel, QLineEdit, QWidget, QPushButton, \
    QMessageBox, QSizePolicy, QTableWidget, QAbstractItemView, QTableWidgetItem, QTextEdit
from infra.configs.connection import DBConnectionHandler
from infra.repository.nota_repository import NotaRepository
from datetime import date
from infra.entities.nota import Nota


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bloco de Notas')
        self.setMinimumSize(520, 500)

        self.setWindowTitle('Notas')

        self.lbl_id = QLabel('ID')
        self.txt_id = QLineEdit()
        self.lbl_id.setVisible(False)
        self.txt_id.setVisible(False)
        self.txt_id.setReadOnly(False)
        self.lbl_nome_nota = QLabel('Nome da nota')
        self.txt_nome_nota = QLineEdit()
        self.lbl_nota = QLabel('Nota')
        self.txt_nota = QLineEdit()
        self.lbl_tabela_notas = QLabel('Notas cadastradas')
        self.tabela_notas = QTableWidget()
        self.tabela_notas.setColumnCount(4)
        self.tabela_notas.setHorizontalHeaderLabels(['ID NOTA', 'NOME DA NOTA', 'NOTA', 'DATA DA NOTA'])
        self.tabela_notas.resizeColumnsToContents()
        self.btn_salvar = QPushButton('Salvar')
        self.btn_limpar = QPushButton('Limpar')
        self.btn_remover = QPushButton('Remover')
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_nome_nota)
        layout.addWidget(self.txt_nome_nota)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)
        layout.addWidget(self.tabela_notas)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)

        layout.addWidget(self.btn_remover)
        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.btn_remover.setVisible(False)
        db_handler = DBConnectionHandler()
        self.popular_tabela_notas()

        self.popular_tabela_notas()
        self.btn_remover.clicked.connect(self.remover_nota)
        self.tabela_notas.cellDoubleClicked.connect(self.carregar_notas)
        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_limpar.clicked.connect(self.limpar_campos)

    def salvar_nota(self):
        db = NotaRepository()

        # id = self.txt_id.text()
        titulo_nota = self.txt_nome_nota.text()
        data = date.today()
        texto = str(self.txt_nota.text())

        nota = Nota(nome_nota=titulo_nota, nota=texto, data_nota=data)

        if self.btn_salvar.text() == 'Salvar':
            retorno = db.insert(nota)

            if retorno == 'ok':
                msg = QMessageBox()
                msg.setWindowTitle('Salvar Nota')
                msg.setText('Nota Salva com sucesso!')
                msg.exec()
                self.limpar_campos()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle('Erro!!!')
                msg.setText(f'Erro ao cadastrar a nota!')
                msg.exec()

        elif self.btn_salvar.text() == 'Atualizar':

            nota.id_nota = id = int(self.txt_id.text())
            db.update(nota)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle('Atualizações')
            msg.setText('Nota Atualizada com Sucesso!')
            msg.exec()
            self.limpar_campos()

        self.popular_tabela_notas()
        self.txt_id.setReadOnly(True)

    def popular_tabela_notas(self):
        self.tabela_notas.setRowCount(0)
        conn = NotaRepository()
        list_notas = conn.select_all()
        self.tabela_notas.setRowCount(len(list_notas))
        linha = 0
        for nota in list_notas:
            valores = [nota.id_nota, nota.nome_nota, nota.nota, nota.data_nota]
            for valor in valores:
                item = QTableWidgetItem(str(valor))
                self.tabela_notas.setItem(linha, valores.index(valor), item)
                self.tabela_notas.item(linha, valores.index(valor))
            linha += 1

    def remover_nota(self):
        msg = QMessageBox()
        msg.setWindowTitle('Remover Nota')
        msg.setText('Esta nota será removida :)')
        msg.setInformativeText(f'Você deseja remover a nota de ID n° {self.txt_id.text()} ?')
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.button(QMessageBox.Yes).setText('Sim')
        msg.button(QMessageBox.No).setText('Não')
        resposta = msg.exec()

        if resposta == QMessageBox.Yes:
            db = NotaRepository()
            retorno = db.delete(self.txt_id.text())

            if retorno == 'ok':
                new_msg = QMessageBox()
                new_msg.setWindowTitle('Remover Nota')
                new_msg.setText('Nota Removida com sucesso!')
                new_msg.exec()
                self.limpar_campos()

            else:
                new_msg = QMessageBox()
                new_msg.setWindowTitle('Remover nota')
                new_msg.setText('Erro ao remover nota')
                new_msg.exec()

        self.txt_id.setReadOnly(False)
        self.popular_tabela_notas()

    def carregar_notas(self, row, column):
        self.txt_id.setText(self.tabela_notas.item(row, 0).text())
        self.txt_nome_nota.setText(self.tabela_notas.item(row, 1).text())
        self.txt_nota.setText(self.tabela_notas.item(row, 2).text())
        self.btn_salvar.setText('Atualizar')
        self.btn_remover.setVisible(True)
        self.txt_id.setVisible(True)
        self.lbl_id.setVisible(True)
        self.txt_id.setReadOnly(True)

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QTextEdit):
                widget.clear()
            elif isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(0)

            self.btn_remover.setVisible(False)
            self.btn_salvar.setText('Salvar')
            self.txt_id.setReadOnly(True)

            self.txt_id.setVisible(False)
            self.lbl_id.setVisible(False)







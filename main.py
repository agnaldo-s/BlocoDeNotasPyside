import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from view.tela_principal import MainWindow

app = QApplication(sys.argv)

window = MainWindow()
icone = QIcon('images/home.svg')
window.setWindowIcon(icone)
window.show()
app.exec()

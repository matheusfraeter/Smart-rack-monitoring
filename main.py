import sys

from PySide6.QtWidgets import QApplication

from gui import SmartRackGUI


app = QApplication(sys.argv)

janela = SmartRackGUI()

janela.show()

sys.exit(app.exec())
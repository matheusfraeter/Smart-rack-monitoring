import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from gui import SmartRackGUI


app = QApplication(sys.argv)

# ===============================
# Carrega o tema global
# ===============================

tema = Path("assets/styles/theme.qss")

if tema.exists():
    with open(tema, "r", encoding="utf-8") as arquivo:
        app.setStyleSheet(arquivo.read())

# ===============================
# Janela principal
# ===============================

janela = SmartRackGUI()
janela.show()

sys.exit(app.exec())
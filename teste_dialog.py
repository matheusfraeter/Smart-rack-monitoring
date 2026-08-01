from PySide6.QtWidgets import QApplication
from ui.widgets.pallet_dialog import PalletDialog
import sys


app = QApplication(sys.argv)


janela = PalletDialog(
    "A1"
)


janela.show()


sys.exit(
    app.exec()
)
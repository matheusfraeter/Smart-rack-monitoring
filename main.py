import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from gui import SmartRackGUI

# ===============================
# Compatibilidade com tela touch
# ===============================

QApplication.setAttribute(
    Qt.AA_SynthesizeMouseForUnhandledTouchEvents,
    True
)

app = QApplication(sys.argv)


# ===============================
# Carrega o tema global
# ===============================

base_path = Path(__file__).resolve().parent

tema = base_path / "assets" / "styles" / "theme.qss"


if tema.exists():

    with open(
        tema,
        "r",
        encoding="utf-8"
    ) as arquivo:

        app.setStyleSheet(
            arquivo.read()
        )

else:

    print(
        "Tema não encontrado:",
        tema
    )


# ===============================
# Janela principal
# ===============================

janela = SmartRackGUI()

janela.show()


sys.exit(
    app.exec()
)
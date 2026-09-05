import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication

from gui import SmartRackGUI


# ===============================
# CRIA A APLICAÇÃO
# ===============================

app = QApplication(
    sys.argv
)


# ===============================
# CARREGA O TEMA GLOBAL
# ===============================

base_path = Path(__file__).resolve().parent

tema = (
    base_path
    / "assets"
    / "styles"
    / "theme.qss"
)


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
# JANELA PRINCIPAL
# ===============================

janela = SmartRackGUI()

janela.show()


sys.exit(
    app.exec()
)
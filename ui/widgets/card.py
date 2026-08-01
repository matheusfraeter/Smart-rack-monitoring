from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel
)

from theme import Theme


class InfoCard(QFrame):

    def __init__(
        self,
        titulo,
        valor
    ):

        super().__init__()

        self.setStyleSheet(
            f"""
            QFrame {{

                background-color: {Theme.CARD};

                border-radius: 12px;

                padding: 15px;

            }}
            """
        )


        layout = QVBoxLayout()


        self.titulo = QLabel(
            titulo
        )

        self.titulo.setStyleSheet("""
            font-size:14px;
            font-weight:bold;
        """)


        self.valor = QLabel(
            valor
        )

        self.valor.setStyleSheet("""
            font-size:22px;
        """)


        layout.addWidget(
            self.titulo
        )

        layout.addWidget(
            self.valor
        )


        self.setLayout(
            layout
        )



    def atualizar_valor(
        self,
        texto
    ):

        self.valor.setText(
            texto
        )
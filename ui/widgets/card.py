"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: card.py
 Descrição...: Widget de cartão de informações
=========================================================
"""


from PySide6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QLabel
)

from PySide6.QtCore import Qt



class InfoCard(QFrame):


    def __init__(self, titulo, valor):

        super().__init__()


        # Nome usado pelo theme.qss
        self.setObjectName(
            "infoCard"
        )


        layout = QVBoxLayout(
            self
        )


        layout.setContentsMargins(
            15,
            15,
            15,
            15
        )


        layout.setSpacing(
            10
        )


        # -----------------------------
        # TÍTULO
        # -----------------------------

        self.titulo = QLabel(
            titulo
        )


        self.titulo.setObjectName(
            "cardTitle"
        )


        self.titulo.setAlignment(
            Qt.AlignCenter
        )


        # -----------------------------
        # VALOR
        # -----------------------------

        self.valor = QLabel(
            valor
        )


        self.valor.setObjectName(
            "cardValue"
        )


        self.valor.setAlignment(
            Qt.AlignCenter
        )


        layout.addWidget(
            self.titulo
        )


        layout.addWidget(
            self.valor
        )



    def atualizar_valor(self, texto):

        self.valor.setText(
            texto
        )
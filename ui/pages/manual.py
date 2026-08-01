from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QGridLayout,
    QSpinBox
)


class ManualPage(QWidget):

    def __init__(self):

        super().__init__()

        self.criar_interface()


    def criar_interface(self):

        layout = QVBoxLayout()


        titulo = QLabel(
            "Controle Manual"
        )

        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)


        status = QLabel(
            "MKS DLC32: Aguardando conexão"
        )


        self.passo = QSpinBox()

        self.passo.setRange(
            1,
            100
        )

        self.passo.setValue(
            10
        )


        controle = QGridLayout()


        btn_zmais = QPushButton("Z +")

        btn_zmenos = QPushButton("Z -")

        btn_xmais = QPushButton("X +")

        btn_xmenos = QPushButton("X -")

        btn_ymais = QPushButton("Y +")

        btn_ymenos = QPushButton("Y -")


        botoes = [
            btn_zmais,
            btn_zmenos,
            btn_xmais,
            btn_xmenos,
            btn_ymais,
            btn_ymenos
        ]


        for botao in botoes:

            botao.setMinimumSize(
                100,
                50
            )


        controle.addWidget(
            btn_zmais,
            0,
            1
        )

        controle.addWidget(
            btn_ymenos,
            1,
            0
        )

        controle.addWidget(
            btn_xmais,
            1,
            1
        )

        controle.addWidget(
            btn_ymais,
            1,
            2
        )

        controle.addWidget(
            btn_zmenos,
            2,
            1
        )

        controle.addWidget(
            btn_xmenos,
            3,
            1
        )


        layout.addWidget(
            titulo
        )

        layout.addWidget(
            status
        )

        layout.addWidget(
            QLabel("Passo (mm)")
        )

        layout.addWidget(
            self.passo
        )

        layout.addLayout(
            controle
        )


        self.setLayout(
            layout
        )
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QHBoxLayout
)


class AutomationPage(QWidget):

    def __init__(self):

        super().__init__()

        self.criar_interface()



    def criar_interface(self):

        layout = QVBoxLayout()



        titulo = QLabel(
            "🤖 Automação"
        )


        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)



        # MODO

        modo_label = QLabel(
            "Modo de operação:"
        )


        self.modo = QComboBox()

        self.modo.addItems(
            [
                "Manual",
                "Automático"
            ]
        )



        # ORIGEM

        origem_label = QLabel(
            "Origem do pallet:"
        )


        self.origem = QComboBox()


        self.origem.addItems(
            [
                "A1",
                "A2",
                "A3",
                "A4",
                "B1",
                "B2",
                "B3",
                "B4",
                "C1",
                "C2",
                "C3",
                "C4",
                "D1",
                "D2",
                "D3",
                "D4"
            ]
        )



        # DESTINO

        destino_label = QLabel(
            "Destino:"
        )


        self.destino = QComboBox()


        self.destino.addItems(
            [
                "A1",
                "A2",
                "A3",
                "A4",
                "B1",
                "B2",
                "B3",
                "B4",
                "C1",
                "C2",
                "C3",
                "C4",
                "D1",
                "D2",
                "D3",
                "D4"
            ]
        )



        botao = QPushButton(
            "▶ INICIAR CICLO"
        )


        botao.setMinimumHeight(
            50
        )



        self.status = QLabel(
            "Status: Aguardando comando..."
        )


        self.status.setStyleSheet("""
            font-size:18px;
        """)



        linha_origem = QHBoxLayout()

        linha_origem.addWidget(
            origem_label
        )

        linha_origem.addWidget(
            self.origem
        )



        linha_destino = QHBoxLayout()

        linha_destino.addWidget(
            destino_label
        )

        linha_destino.addWidget(
            self.destino
        )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            modo_label
        )


        layout.addWidget(
            self.modo
        )


        layout.addLayout(
            linha_origem
        )


        layout.addLayout(
            linha_destino
        )


        layout.addWidget(
            botao
        )


        layout.addWidget(
            self.status
        )



        self.setLayout(
            layout
        )
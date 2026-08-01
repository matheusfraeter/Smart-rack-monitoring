from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)


class DiagnosticsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.criar_interface()


    def criar_interface(self):

        layout = QVBoxLayout()


        titulo = QLabel(
            "🔧 Diagnóstico do Sistema"
        )


        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)


        conexao = QLabel(
            "MKS DLC32:\n🔴 Desconectada"
        )


        firmware = QLabel(
            "Firmware:\nFluidNC"
        )


        eixos = QLabel(
            "Eixos:\n\nX ✅\nY ✅\nZ ✅"
        )


        comando = QLabel(
            "Último comando:\nNenhum"
        )


        layout.addWidget(
            titulo
        )


        layout.addWidget(
            conexao
        )


        layout.addWidget(
            firmware
        )


        layout.addWidget(
            eixos
        )


        layout.addWidget(
            comando
        )


        self.setLayout(
            layout
        )
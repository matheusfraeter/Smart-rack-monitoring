from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox
)


class SettingsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.criar_interface()



    def criar_interface(self):

        layout = QVBoxLayout()


        titulo = QLabel(
            "⚙ Configurações do Sistema"
        )


        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)


        ip_label = QLabel(
            "IP da MKS DLC32:"
        )


        self.ip = QLineEdit(
            "192.168.4.1"
        )


        velocidade_label = QLabel(
            "Velocidade padrão:"
        )


        self.velocidade = QSpinBox()

        self.velocidade.setRange(
            100,
            5000
        )

        self.velocidade.setValue(
            1000
        )


        passo_label = QLabel(
            "Passo de movimento:"
        )


        self.passo = QSpinBox()

        self.passo.setRange(
            1,
            100
        )

        self.passo.setValue(
            10
        )


        salvar = QPushButton(
            "💾 Salvar Configurações"
        )


        layout.addWidget(
            titulo
        )

        layout.addWidget(
            ip_label
        )

        layout.addWidget(
            self.ip
        )

        layout.addWidget(
            velocidade_label
        )

        layout.addWidget(
            self.velocidade
        )

        layout.addWidget(
            passo_label
        )

        layout.addWidget(
            self.passo
        )

        layout.addWidget(
            salvar
        )


        self.setLayout(
            layout
        )
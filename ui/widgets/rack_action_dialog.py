from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)



class RackActionDialog(QDialog):


    def __init__(
            self,
            endereco,
            pallet
    ):

        super().__init__()


        self.endereco = endereco


        self.remover = False


        self.setWindowTitle(
            "Operação do Rack"
        )


        layout = QVBoxLayout()



        texto = QLabel(
            f"{endereco}\n\nPallet:\n{pallet}"
        )


        texto.setStyleSheet(
            """
            font-size:18px;
            """
        )



        botao = QPushButton(
            "Retirar pallet"
        )


        botao.clicked.connect(
            self.retirar
        )



        layout.addWidget(
            texto
        )


        layout.addWidget(
            botao
        )


        self.setLayout(
            layout
        )



    def retirar(self):

        self.remover = True

        self.accept()
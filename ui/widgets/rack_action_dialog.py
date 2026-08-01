"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: rack_action_dialog.py
 Descrição...: Janela de operação do pallet
=========================================================
"""


from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout
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


        self.setMinimumSize(
            450,
            300
        )


        self.criar_interface(
            pallet
        )



    def criar_interface(self, pallet):


        layout = QVBoxLayout()



        titulo = QLabel(
            "📦 Pallet armazenado"
        )


        titulo.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )



        info = QLabel(
            f"""
            Posição:

            {self.endereco}


            Código do pallet:

            {pallet}
            """
        )


        info.setStyleSheet(
            """
            font-size:22px;
            padding:20px;
            """
        )



        botoes = QHBoxLayout()



        btn_retirar = QPushButton(
            "🚜 Retirar pallet"
        )


        btn_cancelar = QPushButton(
            "Cancelar"
        )



        btn_retirar.setMinimumHeight(
            60
        )


        btn_cancelar.setMinimumHeight(
            60
        )



        btn_retirar.clicked.connect(
            self.retirar
        )


        btn_cancelar.clicked.connect(
            self.reject
        )



        botoes.addWidget(
            btn_retirar
        )


        botoes.addWidget(
            btn_cancelar
        )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            info
        )


        layout.addLayout(
            botoes
        )



        self.setLayout(
            layout
        )



    def retirar(self):

        self.remover = True

        self.accept()
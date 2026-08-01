"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: pallet_dialog.py
 Descrição...: Janela de cadastro de pallet
=========================================================
"""


from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout
)



class PalletDialog(QDialog):


    def __init__(self, endereco):

        super().__init__()


        self.endereco = endereco


        self.setWindowTitle(
            "Cadastro de Pallet"
        )


        self.resize(
            350,
            200
        )


        self.criar_interface()



    def criar_interface(self):

        layout = QVBoxLayout()



        titulo = QLabel(
            f"Posição selecionada: {self.endereco}"
        )


        titulo.setStyleSheet(
            """
            font-size:18px;
            font-weight:bold;
            """
        )



        self.pallet = QLineEdit()


        self.pallet.setPlaceholderText(
            "Digite o código do pallet"
        )



        botoes = QHBoxLayout()



        btn_salvar = QPushButton(
            "Salvar"
        )


        btn_cancelar = QPushButton(
            "Cancelar"
        )



        btn_salvar.clicked.connect(
            self.accept
        )


        btn_cancelar.clicked.connect(
            self.reject
        )



        botoes.addWidget(
            btn_salvar
        )


        botoes.addWidget(
            btn_cancelar
        )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.pallet
        )


        layout.addLayout(
            botoes
        )



        self.setLayout(
            layout
        )



    def obter_pallet(self):

        return self.pallet.text()
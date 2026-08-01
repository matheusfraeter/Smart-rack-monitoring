from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout
)

from database import Database
from ui.widgets.pallet_dialog import PalletDialog


class RackPage(QWidget):

    def __init__(self):

        super().__init__()

        self.db = Database()

        self.criar_interface()



    def criar_interface(self):

        layout = QVBoxLayout()


        titulo = QLabel(
            "📦 Mapa do Rack"
        )


        titulo.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)



        self.selecionado = QLabel(
            "Nenhuma posição selecionada"
        )


        self.selecionado.setStyleSheet("""
            font-size:18px;
        """)



        grade = QGridLayout()



        # =====================================
        # CARREGA POSIÇÕES DO BANCO
        # =====================================

        posicoes = self.db.listar_posicoes()



        for indice, dados in enumerate(posicoes):

            endereco = dados[0]

            ocupado = dados[1]

            pallet = dados[2]



            botao = QPushButton(
                endereco
            )


            botao.setMinimumSize(
                80,
                60
            )



            # Cor conforme estado

            if ocupado:

                botao.setStyleSheet(
                    """
                    background-color:#c0392b;
                    color:white;
                    font-weight:bold;
                    """
                )

            else:

                botao.setStyleSheet(
                    """
                    background-color:#27ae60;
                    color:white;
                    font-weight:bold;
                    """
                )



            botao.clicked.connect(
                lambda checked=False, e=endereco:
                self.selecionar(e)
            )



            linha = indice // 4

            coluna = indice % 4



            grade.addWidget(
                botao,
                linha,
                coluna
            )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.selecionado
        )


        layout.addLayout(
            grade
        )


        self.setLayout(
            layout
        )



    def selecionar(self, endereco):

     dialog = PalletDialog(
        endereco
     )


     resultado = dialog.exec()


     if resultado:

        pallet = dialog.obter_pallet()


        if pallet:

            self.db.ocupar_posicao(
                endereco,
                pallet
            )


            self.selecionado.setText(
                f"{endereco} ocupado com {pallet}"
            )
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


        self.botoes = {}


        self.criar_interface()



    def criar_interface(self):

        layout = QVBoxLayout()



        titulo = QLabel(
            "📦 Mapa do Rack"
        )


        titulo.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )



        self.selecionado = QLabel(
            "Nenhuma posição selecionada"
        )



        self.selecionado.setStyleSheet(
            """
            font-size:18px;
            """
        )



        self.grade = QGridLayout()



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.selecionado
        )


        layout.addLayout(
            self.grade
        )



        self.setLayout(
            layout
        )



        self.carregar_rack()



    # =====================================
    # CARREGAR POSIÇÕES DO BANCO
    # =====================================

    def carregar_rack(self):


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



            self.atualizar_cor(
                botao,
                ocupado
            )



            botao.clicked.connect(
                lambda checked=False, e=endereco:
                self.selecionar(e)
            )



            linha = indice // 4

            coluna = indice % 4



            self.grade.addWidget(
                botao,
                linha,
                coluna
            )



            self.botoes[endereco] = botao



    # =====================================
    # ATUALIZA COR DO BOTÃO
    # =====================================

    def atualizar_cor(
            self,
            botao,
            ocupado
    ):


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



    # =====================================
    # SELECIONAR POSIÇÃO
    # =====================================

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
                    f"{endereco} → {pallet}"
                )



                self.atualizar_tela()




    # =====================================
    # ATUALIZAR VISUAL
    # =====================================

    def atualizar_tela(self):


        posicoes = self.db.listar_posicoes()



        for dados in posicoes:


            endereco = dados[0]

            ocupado = dados[1]



            if endereco in self.botoes:


                self.atualizar_cor(
                    self.botoes[endereco],
                    ocupado
                )
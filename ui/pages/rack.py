from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout
)

from database import Database

from ui.widgets.pallet_dialog import PalletDialog

from ui.widgets.rack_action_dialog import RackActionDialog



class RackPage(QWidget):


    def __init__(self):

        super().__init__()


        self.db = Database()


        self.botoes = {}


        self.criar_interface()



    # =====================================
    # INTERFACE
    # =====================================

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

        self.grade.setSpacing(20)

        self.grade.setContentsMargins(
           40,
           40,
           40,
           40
        )



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
    # CARREGAR RACK
    # =====================================

    def carregar_rack(self):


        posicoes = self.db.listar_posicoes()



        for indice, dados in enumerate(posicoes):


            endereco = dados[0]

            ocupado = dados[1]



            botao = QPushButton(
                endereco
            )


            botao.setMinimumSize(
                140,
                100
            )

            botao.setStyleSheet(
               """
               font-size:22px;
               font-weight:bold;
               """
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
    # CORES
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
            font-size:22px;
            font-weight:bold;
            border-radius:10px;
            """
        )


     else:

        botao.setStyleSheet(
            """
            background-color:#27ae60;
            color:white;
            font-size:22px;
            font-weight:bold;
            border-radius:10px;
            """
        )



    # =====================================
    # CLIQUE NA POSIÇÃO
    # =====================================

    def selecionar(self, endereco):


        dados = self.db.buscar_posicao(
            endereco
        )



        ocupado = dados[1]

        pallet = dados[2]



        # -----------------------------
        # POSIÇÃO LIVRE
        # -----------------------------

        if ocupado == 0:


            dialog = PalletDialog(
                endereco
            )



            resultado = dialog.exec()



            if resultado:


                codigo = dialog.obter_pallet()



                if codigo:


                    self.db.ocupar_posicao(
                        endereco,
                        codigo
                    )


                    self.selecionado.setText(
                        f"{endereco} ocupado com {codigo}"
                    )



        # -----------------------------
        # POSIÇÃO OCUPADA
        # -----------------------------

        else:


            dialog = RackActionDialog(
                endereco,
                pallet
            )



            resultado = dialog.exec()



            if resultado and dialog.remover:


                self.db.liberar_posicao(
                    endereco
                )


                self.selecionado.setText(
                    f"{endereco} liberado"
                )



        self.atualizar_tela()



    # =====================================
    # ATUALIZA VISUAL
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
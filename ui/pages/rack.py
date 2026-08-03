"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: rack.py
 Descrição...: Visualização e controle do Rack
 Versão......: 0.3.2
=========================================================
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGridLayout,
    QHBoxLayout,
    QFrame
)


from controllers.rack_controller import RackController

from ui.widgets.pallet_dialog import PalletDialog

from ui.widgets.rack_action_dialog import RackActionDialog



class RackPage(QWidget):


    def __init__(self):

        super().__init__()


        self.controller = RackController()

        self.botoes = {}


        self.criar_interface()



    # =================================================
    # INTERFACE PRINCIPAL
    # =================================================

    def criar_interface(self):


        layout = QVBoxLayout()


        titulo = QLabel(
            "📦 SMART RACK"
        )

        titulo.setStyleSheet(
            """
            font-size:28px;
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


        racks = QHBoxLayout()


        racks.addWidget(
            self.criar_estante("A")
        )


        racks.addWidget(
            self.criar_estante("B")
        )


        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.selecionado
        )


        layout.addLayout(
            racks
        )


        self.setLayout(
            layout
        )


        self.atualizar_tela()



    # =================================================
    # CRIAR ESTANTE
    # =================================================

    def criar_estante(
            self,
            estante
    ):


        frame = QFrame()


        layout = QVBoxLayout()


        titulo = QLabel(
            f"ESTANTE {estante}"
        )


        titulo.setStyleSheet(
            """
            font-size:22px;
            font-weight:bold;
            """
        )


        grade = QGridLayout()

        grade.setSpacing(15)



        for coluna in range(1,5):


            coluna_label = QLabel(
                str(coluna)
            )


            coluna_label.setStyleSheet(
                """
                font-weight:bold;
                font-size:18px;
                """
            )


            grade.addWidget(
                coluna_label,
                0,
                coluna
            )



        linha = 1


        for nivel in [3,2,1]:


            nivel_label = QLabel(
                f"Nível {nivel}"
            )


            nivel_label.setStyleSheet(
                """
                font-weight:bold;
                """
            )


            grade.addWidget(
                nivel_label,
                linha,
                0
            )



            for coluna in range(1,5):


                endereco = (
                    f"{estante}"
                    f"{nivel}"
                    f"{coluna}"
                )


                botao = QPushButton()


                botao.setMinimumSize(
                    90,
                    70
                )


                botao.clicked.connect(
                    lambda checked=False, e=endereco:
                    self.selecionar(e)
                )


                self.botoes[endereco] = botao



                grade.addWidget(
                    botao,
                    linha,
                    coluna
                )


            linha += 1



        layout.addWidget(
            titulo
        )


        layout.addLayout(
            grade
        )


        frame.setLayout(
            layout
        )


        return frame



    # =================================================
    # SELEÇÃO DA POSIÇÃO
    # =================================================

    def selecionar(
            self,
            endereco
    ):


        dados = self.controller.buscar_posicao(
            endereco
        )


        if dados is None:

            return



        ocupado = dados[1]

        pallet = dados[2]



        # -------------------------
        # POSIÇÃO LIVRE
        # -------------------------

        if ocupado == 0:


            dialog = PalletDialog(
                endereco
            )


            if dialog.exec():


                codigo = dialog.obter_pallet()



                if codigo:


                    self.controller.armazenar_pallet(
                        endereco,
                        codigo
                    )


                    self.selecionado.setText(
                        f"Pallet {codigo} armazenado em {endereco}"
                    )



        # -------------------------
        # POSIÇÃO OCUPADA
        # -------------------------

        else:


            dialog = RackActionDialog(
                endereco,
                pallet
            )



            if dialog.exec():


                if dialog.remover:


                    self.controller.retirar_pallet(
                        endereco
                    )


                    self.selecionado.setText(
                        f"Posição {endereco} liberada"
                    )



        self.atualizar_tela()




    # =================================================
    # ATUALIZAR MAPA
    # =================================================

    def atualizar_tela(self):


        posicoes = self.controller.listar_posicoes()



        for endereco, ocupado, pallet in posicoes:


            if endereco in self.botoes:


                self.atualizar_cor(
                    self.botoes[endereco],
                    ocupado
                )



    # =================================================
    # CORES DO RACK
    # =================================================

    def atualizar_cor(
            self,
            botao,
            ocupado
    ):


        if ocupado:


            botao.setText(
                "📦"
            )


            botao.setStyleSheet(
                """
                background-color:#c0392b;
                color:white;
                font-size:30px;
                border-radius:10px;
                """
            )


        else:


            botao.setText(
                ""
            )


            botao.setStyleSheet(
                """
                background-color:#27ae60;
                border-radius:10px;
                """
            )
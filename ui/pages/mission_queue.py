"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: mission_queue.py
 Descrição...: Tela da fila de missões da empilhadeira
=========================================================
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHBoxLayout,
    QHeaderView,
    QMessageBox
)


from controllers.mission_controller import MissionController



class MissionQueuePage(QWidget):


    def __init__(self):

        super().__init__()


        self.controller = MissionController()


        self.missao_atual = None


        self.criar_interface()



    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout()



        titulo = QLabel(
            "🚜 Fila de Missões"
        )


        titulo.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )



        self.info = QLabel(
            "Nenhuma missão selecionada"
        )


        self.info.setStyleSheet(
            """
            font-size:18px;
            """
        )



        self.tabela = QTableWidget()


        self.tabela.setColumnCount(
            4
        )


        self.tabela.setHorizontalHeaderLabels(
            [
                "ID",
                "Origem",
                "Destino",
                "Status"
            ]
        )



        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )



        botao_atualizar = QPushButton(
            "🔄 Atualizar Fila"
        )


        botao_atualizar.clicked.connect(
            self.carregar_fila
        )



        botao_iniciar = QPushButton(
            "▶ Iniciar Próxima"
        )


        botao_iniciar.clicked.connect(
            self.iniciar
        )



        botao_finalizar = QPushButton(
            "✔ Finalizar"
        )


        botao_finalizar.clicked.connect(
            self.finalizar
        )



        botoes = QHBoxLayout()


        botoes.addWidget(
            botao_atualizar
        )


        botoes.addWidget(
            botao_iniciar
        )


        botoes.addWidget(
            botao_finalizar
        )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.info
        )


        layout.addWidget(
            self.tabela
        )


        layout.addLayout(
            botoes
        )



        self.setLayout(
            layout
        )



        self.carregar_fila()



    # =====================================
    # CARREGAR FILA
    # =====================================

    def carregar_fila(self):


        missoes = self.controller.listar_fila()



        self.tabela.setRowCount(
            len(missoes)
        )



        for linha, dados in enumerate(missoes):


            for coluna, valor in enumerate(dados):


                self.tabela.setItem(
                    linha,
                    coluna,
                    QTableWidgetItem(
                        str(valor)
                    )
                )



    # =====================================
    # INICIAR PRÓXIMA
    # =====================================

    def iniciar(self):


        missao = self.controller.proxima_missao()



        if missao is None:


            QMessageBox.information(
                self,
                "Fila vazia",
                "Não existem missões aguardando."
            )

            return



        self.missao_atual = missao



        id_missao = missao[0]



        self.controller.iniciar_missao(
            id_missao
        )



        self.info.setText(
            f"Missão {id_missao} em movimento: "
            f"{missao[1]} → {missao[2]}"
        )


        self.carregar_fila()



    # =====================================
    # FINALIZAR
    # =====================================

    def finalizar(self):


        if self.missao_atual is None:


            QMessageBox.warning(
                self,
                "Erro",
                "Nenhuma missão em execução."
            )

            return



        id_missao = self.missao_atual[0]



        self.controller.finalizar_missao(
            id_missao
        )



        self.info.setText(
            f"Missão {id_missao} concluída"
        )


        self.missao_atual = None


        self.carregar_fila()
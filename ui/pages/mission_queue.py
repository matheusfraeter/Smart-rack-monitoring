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


from controllers.machine_controller import MachineController



class MissionQueuePage(QWidget):


    def __init__(self):

        super().__init__()


        self.controller = MachineController()


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
            "Nenhuma missão executada"
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



        # -----------------------------
        # BOTÃO ATUALIZAR
        # -----------------------------

        botao_atualizar = QPushButton(
            "🔄 Atualizar Fila"
        )


        botao_atualizar.clicked.connect(
            self.carregar_fila
        )



        # -----------------------------
        # BOTÃO EXECUTAR
        # -----------------------------

        botao_executar = QPushButton(
            "🚜 Executar Próxima Missão"
        )


        botao_executar.clicked.connect(
            self.executar
        )



        botoes = QHBoxLayout()



        botoes.addWidget(
            botao_atualizar
        )


        botoes.addWidget(
            botao_executar
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


        missoes = self.controller.mission.listar_fila()



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
    # EXECUTAR MISSÃO
    # =====================================

    def executar(self):


        resultado = self.controller.executar_proxima_missao()



        if resultado["sucesso"] is False:


            QMessageBox.warning(

                self,

                "Falha",

                resultado["mensagem"]

            )

            return



        self.info.setText(

            f"Movimento concluído: "
            f"{resultado['origem']} → "
            f"{resultado['destino']}"

        )



        QMessageBox.information(

            self,

            "Missão concluída",

            resultado["mensagem"]

        )


        self.carregar_fila()
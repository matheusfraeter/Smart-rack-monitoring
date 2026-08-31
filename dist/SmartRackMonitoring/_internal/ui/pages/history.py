"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: history.py
 Descrição...: Tela de histórico de movimentações
=========================================================
"""


from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView
)


from PySide6.QtCore import QTimer


from controllers.history_controller import HistoryController




class HistoryPage(QWidget):


    def __init__(self):

        super().__init__()


        self.controller = HistoryController()


        self.criar_interface()


        # Atualização automática

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.carregar_historico
        )


        self.timer.start(
            2000
        )



    # =====================================
    # INTERFACE
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout()



        titulo = QLabel(
            "📜 Histórico de Operações"
        )


        titulo.setStyleSheet(
            """
            font-size:26px;
            font-weight:bold;
            """
        )



        self.tabela = QTableWidget()


        self.tabela.setColumnCount(
            4
        )


        self.tabela.setHorizontalHeaderLabels(
            [
                "Data/Hora",
                "Origem",
                "Destino",
                "Status"
            ]
        )



        self.tabela.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )



        layout.addWidget(
            titulo
        )


        layout.addWidget(
            self.tabela
        )


        self.setLayout(
            layout
        )


        self.carregar_historico()



    # =====================================
    # CARREGAR DADOS
    # =====================================

    def carregar_historico(self):


        movimentos = self.controller.listar_movimentos()



        self.tabela.setRowCount(
            len(movimentos)
        )



        for linha, dados in enumerate(movimentos):


            for coluna, valor in enumerate(dados):


                item = QTableWidgetItem(
                    str(valor)
                )


                self.tabela.setItem(
                    linha,
                    coluna,
                    item
                )



    # =====================================
    # ATUALIZA AO ABRIR A TELA
    # =====================================

    def showEvent(self, event):

        self.carregar_historico()

        super().showEvent(event)
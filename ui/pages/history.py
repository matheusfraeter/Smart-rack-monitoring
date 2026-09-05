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
    QHeaderView,
    QFrame,
    QScrollArea,
    QSizePolicy
)

from PySide6.QtCore import (
    Qt,
    QTimer
)

from controllers.history_controller import HistoryController


class HistoryPage(QWidget):

    def __init__(self):

        super().__init__()

        # =====================================
        # CONTROLLER
        # =====================================

        self.controller = HistoryController()

        # =====================================
        # CRIAR INTERFACE
        # =====================================

        self.criar_interface()

        # =====================================
        # ATUALIZAÇÃO AUTOMÁTICA
        # =====================================

        self.timer = QTimer(
            self
        )

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

        layout_externo = QVBoxLayout(
            self
        )

        layout_externo.setContentsMargins(
            0,
            0,
            0,
            0
        )

        # =====================================
        # SCROLL ÚNICO
        # =====================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setFrameShape(
            QFrame.NoFrame
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        # =====================================
        # CONTEÚDO
        # =====================================

        conteudo = QWidget()

        self.layout_principal = QVBoxLayout(
            conteudo
        )

        self.layout_principal.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.layout_principal.setSpacing(
            15
        )

        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel(
            "HISTÓRICO DE OPERAÇÕES"
        )

        titulo.setObjectName(
            "title"
        )

        self.layout_principal.addWidget(
            titulo
        )

        # =====================================
        # TABELA
        # =====================================

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            3
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "Data/Hora",
                "Origem",
                "Destino"
            ]
        )

        self.tabela.setAlternatingRowColors(
            False
        )

        self.tabela.verticalHeader().setVisible(
            False
        )

        # =====================================
        # SELEÇÃO
        # =====================================

        self.tabela.setSelectionMode(
            QTableWidget.SingleSelection
        )

        # =====================================
        # SEM SCROLL INTERNO
        # =====================================

        self.tabela.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        # =====================================
        # CABEÇALHO
        # =====================================

        cabecalho = (
            self.tabela.horizontalHeader()
        )

        cabecalho.setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        cabecalho.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        cabecalho.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        self.layout_principal.addWidget(
            self.tabela
        )

        # =====================================
        # ESPAÇO FINAL
        # =====================================

        self.layout_principal.addStretch()

        self.scroll.setWidget(
            conteudo
        )

        layout_externo.addWidget(
            self.scroll
        )

        # =====================================
        # CARREGAMENTO INICIAL
        # =====================================

        self.carregar_historico()

    # =====================================
    # ALTURA DA TABELA
    # =====================================

    def ajustar_altura_tabela(self):

        self.tabela.resizeRowsToContents()

        altura_header = (
            self.tabela.horizontalHeader().height()
        )

        altura_linhas = sum(
            self.tabela.rowHeight(i)
            for i in range(
                self.tabela.rowCount()
            )
        )

        altura_bordas = (
            self.tabela.frameWidth()
            * 2
        )

        altura_total = (
            altura_header
            + altura_linhas
            + altura_bordas
            + 2
        )

        self.tabela.setFixedHeight(
            altura_total
        )

    # =====================================
    # CARREGAR HISTÓRICO
    # =====================================

    def carregar_historico(self):

        movimentos = (
            self.controller.listar_movimentos()
        )

        self.tabela.setRowCount(
            len(movimentos)
        )

        for linha, dados in enumerate(
            movimentos
        ):

            for coluna, valor in enumerate(
                dados
            ):

                if coluna >= 3:

                    continue

                item = QTableWidgetItem(
                    str(valor)
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.tabela.setItem(
                    linha,
                    coluna,
                    item
                )

        self.ajustar_altura_tabela()

    # =====================================
    # AO ABRIR A TELA
    # =====================================

    def showEvent(
        self,
        event
    ):

        self.carregar_historico()

        super().showEvent(
            event
        )

    # =====================================
    # FECHAR
    # =====================================

    def closeEvent(
        self,
        event
    ):

        self.timer.stop()

        event.accept()
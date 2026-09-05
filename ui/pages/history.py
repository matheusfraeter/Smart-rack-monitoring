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
    QSizePolicy,
    QApplication
)

from PySide6.QtCore import (
    Qt,
    QTimer,
    QEvent,
    QPoint
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
        # CONTROLE DO GESTO
        # =====================================

        self._touch_ativo = False
        self._touch_arrastando = False

        self._touch_posicao_inicial = QPoint()
        self._touch_posicao_anterior = QPoint()

        self._touch_limite_arrasto = 12

        # =====================================
        # CRIAR INTERFACE
        # =====================================

        self.criar_interface()

        # =====================================
        # FILTRO GLOBAL
        # =====================================

        app = QApplication.instance()

        if app is not None:

            app.installEventFilter(
                self
            )

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

        self.scroll.viewport().setAttribute(
            Qt.WA_AcceptTouchEvents,
            True
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

        self.tabela.setAttribute(
            Qt.WA_AcceptTouchEvents,
            True
        )

        self.tabela.viewport().setAttribute(
            Qt.WA_AcceptTouchEvents,
            True
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
    # PONTO DENTRO DO SCROLL
    # =====================================

    def ponto_dentro_scroll(
        self,
        ponto_global
    ):

        viewport = self.scroll.viewport()

        ponto_local = (
            viewport.mapFromGlobal(
                ponto_global
            )
        )

        return viewport.rect().contains(
            ponto_local
        )

    # =====================================
    # INICIAR GESTO
    # =====================================

    def iniciar_gesto(
        self,
        posicao
    ):

        self._touch_ativo = True

        self._touch_arrastando = False

        self._touch_posicao_inicial = (
            posicao
        )

        self._touch_posicao_anterior = (
            posicao
        )

    # =====================================
    # MOVER GESTO
    # =====================================

    def mover_gesto(
        self,
        posicao
    ):

        if not self._touch_ativo:

            return False

        deslocamento = (
            posicao
            -
            self._touch_posicao_inicial
        )

        # =====================================
        # INÍCIO DO ARRASTO
        # =====================================

        if not self._touch_arrastando:

            if (
                deslocamento.manhattanLength()
                <
                self._touch_limite_arrasto
            ):

                return False

            self._touch_arrastando = True

            # =================================
            # REMOVER SELEÇÃO
            # =================================

            self.tabela.clearSelection()

            self.tabela.clearFocus()

            self.tabela.setSelectionMode(
                QTableWidget.NoSelection
            )

        # =====================================
        # MOVIMENTO REAL
        # =====================================

        delta_y = (
            posicao.y()
            -
            self._touch_posicao_anterior.y()
        )

        barra = (
            self.scroll.verticalScrollBar()
        )

        novo_valor = (
            barra.value()
            -
            delta_y
        )

        novo_valor = max(
            barra.minimum(),
            min(
                barra.maximum(),
                novo_valor
            )
        )

        barra.setValue(
            novo_valor
        )

        self._touch_posicao_anterior = (
            posicao
        )

        return True

    # =====================================
    # FINALIZAR GESTO
    # =====================================

    def finalizar_gesto(self):

        foi_arrasto = (
            self._touch_arrastando
        )

        self._touch_ativo = False

        self._touch_arrastando = False

        # =====================================
        # RESTAURAR SELEÇÃO
        # =====================================

        self.tabela.setSelectionMode(
            QTableWidget.SingleSelection
        )

        return foi_arrasto

    # =====================================
    # EVENT FILTER GLOBAL
    # =====================================

    def eventFilter(
        self,
        obj,
        event
    ):

        # =====================================
        # IMPORTANTE:
        # NÃO PROCESSAR EVENTOS QUANDO
        # O HISTÓRICO NÃO ESTÁ VISÍVEL.
        # =====================================

        if not self.isVisible():

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # MOUSE PRESS
        # =====================================

        if event.type() == QEvent.MouseButtonPress:

            if event.button() != Qt.LeftButton:

                return super().eventFilter(
                    obj,
                    event
                )

            ponto = (
                event.globalPosition()
                .toPoint()
            )

            if not self.ponto_dentro_scroll(
                ponto
            ):

                return super().eventFilter(
                    obj,
                    event
                )

            self.iniciar_gesto(
                ponto
            )

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # MOUSE MOVE
        # =====================================

        if event.type() == QEvent.MouseMove:

            if not self._touch_ativo:

                return super().eventFilter(
                    obj,
                    event
                )

            ponto = (
                event.globalPosition()
                .toPoint()
            )

            arrastando = self.mover_gesto(
                ponto
            )

            if arrastando:

                event.accept()

                return True

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # MOUSE RELEASE
        # =====================================

        if event.type() == QEvent.MouseButtonRelease:

            if event.button() != Qt.LeftButton:

                return super().eventFilter(
                    obj,
                    event
                )

            if not self._touch_ativo:

                return super().eventFilter(
                    obj,
                    event
                )

            foi_arrasto = (
                self.finalizar_gesto()
            )

            if foi_arrasto:

                event.accept()

                return True

            return super().eventFilter(
                obj,
                event
            )

        # =====================================
        # TOUCH BEGIN
        # =====================================

        if event.type() == QEvent.TouchBegin:

            pontos = event.touchPoints()

            if not pontos:

                return super().eventFilter(
                    obj,
                    event
                )

            ponto = (
                pontos[0]
                .globalPosition()
                .toPoint()
            )

            if not self.ponto_dentro_scroll(
                ponto
            ):

                return super().eventFilter(
                    obj,
                    event
                )

            self.iniciar_gesto(
                ponto
            )

            event.accept()

            return True

        # =====================================
        # TOUCH UPDATE
        # =====================================

        if event.type() == QEvent.TouchUpdate:

            if not self._touch_ativo:

                return super().eventFilter(
                    obj,
                    event
                )

            pontos = event.touchPoints()

            if not pontos:

                return super().eventFilter(
                    obj,
                    event
                )

            ponto = (
                pontos[0]
                .globalPosition()
                .toPoint()
            )

            arrastando = self.mover_gesto(
                ponto
            )

            if arrastando:

                event.accept()

                return True

            return True

        # =====================================
        # TOUCH END
        # =====================================

        if event.type() == QEvent.TouchEnd:

            if not self._touch_ativo:

                return super().eventFilter(
                    obj,
                    event
                )

            self.finalizar_gesto()

            event.accept()

            return True

        # =====================================
        # TOUCH CANCEL
        # =====================================

        if event.type() == QEvent.TouchCancel:

            self._touch_ativo = False

            self._touch_arrastando = False

            self.tabela.setSelectionMode(
                QTableWidget.SingleSelection
            )

            return True

        return super().eventFilter(
            obj,
            event
        )

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

        app = QApplication.instance()

        if app is not None:

            app.removeEventFilter(
                self
            )

        event.accept()
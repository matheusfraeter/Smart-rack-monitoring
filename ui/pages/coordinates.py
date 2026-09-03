"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: coordinates.py
 Descrição...: Configuração de coordenadas
=========================================================
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QAbstractItemView,
    QScrollArea,
    QDialog,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox,
    QDoubleSpinBox,
    QApplication,
    QStyle,
    QStyleOptionSpinBox,
)

from PySide6.QtCore import (
    Qt,
    QEvent,
    QPoint,
)

from database import Database


# =========================================================
# DIÁLOGO DE SENHA
# =========================================================

class PasswordDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Acesso")
        self.setModal(True)
        self.setMinimumWidth(300)

        layout = QVBoxLayout(self)

        titulo = QLabel(
            "Digite a senha para desbloquear:"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        self.campo_senha = QLineEdit()

        self.campo_senha.setEchoMode(
            QLineEdit.Password
        )

        self.campo_senha.setAlignment(
            Qt.AlignCenter
        )

        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        botoes.accepted.connect(
            self.accept
        )

        botoes.rejected.connect(
            self.reject
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            self.campo_senha
        )

        layout.addWidget(
            botoes
        )

        self.campo_senha.returnPressed.connect(
            self.accept
        )

    def senha(self):

        return self.campo_senha.text()


# =========================================================
# PÁGINA DE COORDENADAS
# =========================================================

class CoordinatesPage(QWidget):

    SENHA = "1234"

    POSICOES_MAQUINA = [
        "RECEBIMENTO",
        "EXPEDICAO",
        "Z_TRANSPORTE"
    ]

    def __init__(self):

        super().__init__()

        self.db = Database()

        self.acesso_liberado = False

        self.campos = []
        self.campos_maquina = []

        # =====================================================
        # ESTADO DO GESTO
        # =====================================================

        self._touch_ativo = False
        self._touch_arrastando = False

        self._touch_posicao_inicial = QPoint()
        self._touch_posicao_anterior = QPoint()

        self._touch_limite_arrasto = 12

        # =====================================================
        # ESTADO ESPECÍFICO DOS SPINBOX
        # =====================================================

        self._spinbox_pendente = None
        self._spinbox_direcao = 0

        self.criar_interface()

        # =====================================================
        # FILTRO GLOBAL
        # =====================================================

        app = QApplication.instance()

        if app is not None:

            app.installEventFilter(
                self
            )

    # =========================================================
    # CRIAR INTERFACE
    # =========================================================

    def criar_interface(self):

        layout_principal = QVBoxLayout(
            self
        )

        layout_principal.setContentsMargins(
            10,
            10,
            10,
            10
        )

        layout_principal.setSpacing(
            10
        )

        # =====================================================
        # SCROLL
        # =====================================================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.scroll.setVerticalScrollBarPolicy(
            Qt.ScrollBarAsNeeded
        )

        layout_principal.addWidget(
            self.scroll
        )

        # =====================================================
        # CONTEÚDO
        # =====================================================

        self.conteudo = QWidget()

        self.layout_conteudo = QVBoxLayout(
            self.conteudo
        )

        self.layout_conteudo.setContentsMargins(
            5,
            5,
            5,
            5
        )

        self.layout_conteudo.setSpacing(
            12
        )

        self.scroll.setWidget(
            self.conteudo
        )

        # =====================================================
        # TÍTULO
        # =====================================================

        titulo = QLabel(
            "COORDENADAS"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setObjectName(
            "tituloPagina"
        )

        self.layout_conteudo.addWidget(
            titulo
        )

        # =====================================================
        # COORDENADAS DO RACK
        # =====================================================

        titulo_rack = QLabel(
            "COORDENADAS DO RACK"
        )

        titulo_rack.setAlignment(
            Qt.AlignCenter
        )

        self.layout_conteudo.addWidget(
            titulo_rack
        )

        self.tabela = QTableWidget()

        self.tabela.setColumnCount(
            4
        )

        self.tabela.setHorizontalHeaderLabels(
            [
                "Célula",
                "X",
                "Y",
                "Z"
            ]
        )

        self.tabela.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.tabela.setSelectionMode(
            QAbstractItemView.NoSelection
        )

        self.tabela.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        for coluna in range(4):

            self.tabela.horizontalHeader().setSectionResizeMode(
                coluna,
                QHeaderView.Stretch
            )

        self.layout_conteudo.addWidget(
            self.tabela
        )

        # =====================================================
        # POSIÇÕES DA EMPILHADEIRA
        # =====================================================

        titulo_maquina = QLabel(
            "POSIÇÕES DA EMPILHADEIRA"
        )

        titulo_maquina.setAlignment(
            Qt.AlignCenter
        )

        self.layout_conteudo.addWidget(
            titulo_maquina
        )

        self.tabela_maquina = QTableWidget()

        self.tabela_maquina.setColumnCount(
            4
        )

        self.tabela_maquina.setHorizontalHeaderLabels(
            [
                "Posição",
                "X",
                "Y",
                "Z"
            ]
        )

        self.tabela_maquina.setRowCount(
            len(self.POSICOES_MAQUINA)
        )

        self.tabela_maquina.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.tabela_maquina.setSelectionMode(
            QAbstractItemView.NoSelection
        )

        self.tabela_maquina.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela_maquina.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        for coluna in range(4):

            self.tabela_maquina.horizontalHeader().setSectionResizeMode(
                coluna,
                QHeaderView.Stretch
            )

        for linha, nome in enumerate(
            self.POSICOES_MAQUINA
        ):

            item = QTableWidgetItem(
                nome
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            self.tabela_maquina.setItem(
                linha,
                0,
                item
            )

        self.layout_conteudo.addWidget(
            self.tabela_maquina
        )

        # =====================================================
        # AJUSTES DA EMPILHADEIRA
        # =====================================================

        titulo_ajustes = QLabel(
            "AJUSTES DA EMPILHADEIRA"
        )

        titulo_ajustes.setAlignment(
            Qt.AlignCenter
        )

        self.layout_conteudo.addWidget(
            titulo_ajustes
        )

        ajustes = QHBoxLayout()

        ajustes.setSpacing(
            10
        )

        # =====================================================
        # Z LEVANTAR
        # =====================================================

        bloco_levantar = QVBoxLayout()

        label_levantar = QLabel(
            "Z LEVANTAR"
        )

        label_levantar.setAlignment(
            Qt.AlignCenter
        )

        self.campo_z_levantar = self.criar_campo(
            10.0
        )

        self.campo_z_levantar.setSuffix(
            " mm"
        )

        bloco_levantar.addWidget(
            label_levantar
        )

        bloco_levantar.addWidget(
            self.campo_z_levantar
        )

        # =====================================================
        # Z APOIAR
        # =====================================================

        bloco_apoiar = QVBoxLayout()

        label_apoiar = QLabel(
            "Z APOIAR"
        )

        label_apoiar.setAlignment(
            Qt.AlignCenter
        )

        self.campo_z_apoiar = self.criar_campo(
            10.0
        )

        self.campo_z_apoiar.setSuffix(
            " mm"
        )

        bloco_apoiar.addWidget(
            label_apoiar
        )

        bloco_apoiar.addWidget(
            self.campo_z_apoiar
        )

        ajustes.addLayout(
            bloco_levantar
        )

        ajustes.addLayout(
            bloco_apoiar
        )

        self.layout_conteudo.addLayout(
            ajustes
        )

        # =====================================================
        # BOTÕES
        # =====================================================

        botoes = QHBoxLayout()

        botoes.setSpacing(
            8
        )

        self.bt_desbloquear = QPushButton(
            "DESBLOQUEAR"
        )

        self.bt_salvar = QPushButton(
            "SALVAR COORDENADAS"
        )

        self.bt_atualizar = QPushButton(
            "ATUALIZAR"
        )

        botoes.addWidget(
            self.bt_desbloquear
        )

        botoes.addWidget(
            self.bt_salvar
        )

        botoes.addWidget(
            self.bt_atualizar
        )

        self.layout_conteudo.addLayout(
            botoes
        )

        # =====================================================
        # CONEXÕES
        # =====================================================

        self.bt_desbloquear.clicked.connect(
            self.alternar_bloqueio
        )

        self.bt_salvar.clicked.connect(
            self.salvar_coordenadas
        )

        self.bt_atualizar.clicked.connect(
            self.carregar_coordenadas
        )

        # =====================================================
        # ESTADO INICIAL
        # =====================================================

        self.carregar_coordenadas()

        self.bloquear()

    # =========================================================
    # CRIAR QDOUBLESPINBOX
    # =========================================================

    def criar_campo(
        self,
        valor=0.0
    ):

        campo = QDoubleSpinBox()

        campo.setRange(
            -99999.999,
            99999.999
        )

        campo.setDecimals(
            3
        )

        campo.setSingleStep(
            1.0
        )

        campo.setAlignment(
            Qt.AlignCenter
        )

        campo.setValue(
            float(valor)
        )

        return campo

    # =========================================================
    # DETECTAR QDOUBLESPINBOX
    # =========================================================

    def encontrar_spinbox(
        self,
        obj
    ):

        atual = obj

        while atual is not None:

            if isinstance(
                atual,
                QDoubleSpinBox
            ):

                return atual

            if hasattr(
                atual,
                "parentWidget"
            ):

                atual = atual.parentWidget()

            else:

                break

        return None

    # =========================================================
    # DETECTAR SETA DO SPINBOX
    # =========================================================

    def detectar_seta_spinbox(
        self,
        obj,
        ponto_global
    ):

        spinbox = self.encontrar_spinbox(
            obj
        )

        if spinbox is None:

            return None, 0

        ponto_local = spinbox.mapFromGlobal(
            ponto_global
        )

        opcao = QStyleOptionSpinBox()

        opcao.initFrom(
            spinbox
        )

        opcao.rect = spinbox.rect()

        subcontrole = spinbox.style().hitTestComplexControl(
            QStyle.CC_SpinBox,
            opcao,
            ponto_local,
            spinbox
        )

        if subcontrole == QStyle.SC_SpinBoxUp:

            return spinbox, 1

        if subcontrole == QStyle.SC_SpinBoxDown:

            return spinbox, -1

        return None, 0

    # =========================================================
    # VERIFICAR PONTO DENTRO DO SCROLL
    # =========================================================

    def _ponto_dentro_scroll(
        self,
        ponto
    ):

        viewport = self.scroll.viewport()

        ponto_local = viewport.mapFromGlobal(
            ponto
        )

        return viewport.rect().contains(
            ponto_local
        )

    # =========================================================
    # APLICAR CLIQUE DA SETA
    # =========================================================

    def aplicar_seta_spinbox(self):

        spinbox = self._spinbox_pendente

        direcao = self._spinbox_direcao

        self._spinbox_pendente = None

        self._spinbox_direcao = 0

        if spinbox is None:

            return

        valor = spinbox.value()

        passo = spinbox.singleStep()

        novo_valor = valor + (
            passo * direcao
        )

        if novo_valor > spinbox.maximum():

            novo_valor = spinbox.maximum()

        if novo_valor < spinbox.minimum():

            novo_valor = spinbox.minimum()

        spinbox.setValue(
            novo_valor
        )

    # =========================================================
    # CANCELAR CLIQUE DA SETA
    # =========================================================

    def cancelar_seta_spinbox(self):

        self._spinbox_pendente = None

        self._spinbox_direcao = 0

    # =========================================================
    # EVENT FILTER
    # =========================================================

    def eventFilter(
        self,
        obj,
        event
    ):

        # =====================================================
        # IGNORAR QUANDO A PÁGINA NÃO ESTÁ VISÍVEL
        # =====================================================

        if not self.isVisible():

            return super().eventFilter(
                obj,
                event
            )

        # =====================================================
        # MOUSE PRESS
        # =====================================================

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

            if not self._ponto_dentro_scroll(
                ponto
            ):

                return super().eventFilter(
                    obj,
                    event
                )

            # -------------------------------------------------
            # VERIFICAR SE COMEÇOU NAS SETAS
            # -------------------------------------------------

            spinbox, direcao = (
                self.detectar_seta_spinbox(
                    obj,
                    ponto
                )
            )

            if spinbox is not None:

                self._spinbox_pendente = (
                    spinbox
                )

                self._spinbox_direcao = (
                    direcao
                )

                self._touch_ativo = True

                self._touch_arrastando = False

                self._touch_posicao_inicial = (
                    ponto
                )

                self._touch_posicao_anterior = (
                    ponto
                )

                return True

            # -------------------------------------------------
            # CLIQUE NORMAL
            # -------------------------------------------------

            self._touch_ativo = True

            self._touch_arrastando = False

            self._touch_posicao_inicial = (
                ponto
            )

            self._touch_posicao_anterior = (
                ponto
            )

            self.cancelar_seta_spinbox()

            return super().eventFilter(
                obj,
                event
            )

        # =====================================================
        # MOUSE MOVE
        # =====================================================

        if event.type() == QEvent.MouseMove:

            if not self._touch_ativo:

                return super().eventFilter(
                    obj,
                    event
                )

            ponto_atual = (
                event.globalPosition()
                .toPoint()
            )

            deslocamento = (
                ponto_atual
                -
                self._touch_posicao_inicial
            )

            # -------------------------------------------------
            # AINDA NÃO ATINGIU LIMITE
            # -------------------------------------------------

            if not self._touch_arrastando:

                if (
                    deslocamento.manhattanLength()
                    <
                    self._touch_limite_arrasto
                ):

                    if self._spinbox_pendente is not None:

                        return True

                    return super().eventFilter(
                        obj,
                        event
                    )

                # ---------------------------------------------
                # COMEÇOU ARRASTE
                # ---------------------------------------------

                self._touch_arrastando = True

                self.cancelar_seta_spinbox()

            # -------------------------------------------------
            # ROLAR
            # -------------------------------------------------

            delta_y = (
                ponto_atual.y()
                -
                self._touch_posicao_anterior.y()
            )

            barra = (
                self.scroll.verticalScrollBar()
            )

            barra.setValue(
                barra.value()
                -
                delta_y
            )

            self._touch_posicao_anterior = (
                ponto_atual
            )

            return True

        # =====================================================
        # MOUSE RELEASE
        # =====================================================

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

            ponto = (
                event.globalPosition()
                .toPoint()
            )

            foi_arrasto = (
                self._touch_arrastando
            )

            self._touch_ativo = False

            self._touch_arrastando = False

            # -------------------------------------------------
            # ARRASTE
            # -------------------------------------------------

            if foi_arrasto:

                self.cancelar_seta_spinbox()

                return True

            # -------------------------------------------------
            # CLIQUE NAS SETAS
            # -------------------------------------------------

            if self._spinbox_pendente is not None:

                spinbox, direcao = (
                    self.detectar_seta_spinbox(
                        obj,
                        ponto
                    )
                )

                if (
                    spinbox is self._spinbox_pendente
                    and
                    direcao == self._spinbox_direcao
                ):

                    self.aplicar_seta_spinbox()

                else:

                    self.cancelar_seta_spinbox()

                return True

            return super().eventFilter(
                obj,
                event
            )

        # =====================================================
        # TOUCH BEGIN
        # =====================================================

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

            if self._ponto_dentro_scroll(
                ponto
            ):

                self._touch_ativo = True

                self._touch_arrastando = False

                self._touch_posicao_inicial = (
                    ponto
                )

                self._touch_posicao_anterior = (
                    ponto
                )

                self.cancelar_seta_spinbox()

                event.accept()

                return True

        # =====================================================
        # TOUCH UPDATE
        # =====================================================

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

            ponto_atual = (
                pontos[0]
                .globalPosition()
                .toPoint()
            )

            deslocamento = (
                ponto_atual
                -
                self._touch_posicao_inicial
            )

            # -------------------------------------------------
            # LIMITE
            # -------------------------------------------------

            if not self._touch_arrastando:

                if (
                    deslocamento.manhattanLength()
                    <
                    self._touch_limite_arrasto
                ):

                    return True

                self._touch_arrastando = True

                self.cancelar_seta_spinbox()

            # -------------------------------------------------
            # ROLAR
            # -------------------------------------------------

            delta_y = (
                ponto_atual.y()
                -
                self._touch_posicao_anterior.y()
            )

            barra = (
                self.scroll.verticalScrollBar()
            )

            barra.setValue(
                barra.value()
                -
                delta_y
            )

            self._touch_posicao_anterior = (
                ponto_atual
            )

            return True

        # =====================================================
        # TOUCH END
        # =====================================================

        if event.type() == QEvent.TouchEnd:

            self._touch_ativo = False

            self._touch_arrastando = False

            self.cancelar_seta_spinbox()

            event.accept()

            return True

        # =====================================================
        # TOUCH CANCEL
        # =====================================================

        if event.type() == QEvent.TouchCancel:

            self._touch_ativo = False

            self._touch_arrastando = False

            self.cancelar_seta_spinbox()

            return True

        return super().eventFilter(
            obj,
            event
        )

    # =========================================================
    # ALTERNAR BLOQUEIO
    # =========================================================

    def alternar_bloqueio(self):

        if self.acesso_liberado:

            self.bloquear()

        else:

            self.solicitar_senha()

    # =========================================================
    # SENHA
    # =========================================================

    def solicitar_senha(self):

        dialogo = PasswordDialog(
            self
        )

        if dialogo.exec() != QDialog.Accepted:

            return

        if dialogo.senha() == self.SENHA:

            self.desbloquear()

        else:

            QMessageBox.warning(
                self,
                "Senha incorreta",
                "A senha informada está incorreta."
            )

    # =========================================================
    # DESBLOQUEAR
    # =========================================================

    def desbloquear(self):

        self.acesso_liberado = True

        for campo in self.campos:

            campo.setEnabled(
                True
            )

        for campo in self.campos_maquina:

            campo.setEnabled(
                True
            )

        self.campo_z_levantar.setEnabled(
            True
        )

        self.campo_z_apoiar.setEnabled(
            True
        )

        self.bt_salvar.setEnabled(
            True
        )

        self.atualizar_estilo_status()

    # =========================================================
    # BLOQUEAR
    # =========================================================

    def bloquear(self):

        self.acesso_liberado = False

        for campo in self.campos:

            campo.setEnabled(
                False
            )

        for campo in self.campos_maquina:

            campo.setEnabled(
                False
            )

        self.campo_z_levantar.setEnabled(
            False
        )

        self.campo_z_apoiar.setEnabled(
            False
        )

        self.bt_salvar.setEnabled(
            False
        )

        self.atualizar_estilo_status()

    # =========================================================
    # TEXTO DO BOTÃO
    # =========================================================

    def atualizar_estilo_status(self):

        if self.acesso_liberado:

            self.bt_desbloquear.setText(
                "BLOQUEAR"
            )

        else:

            self.bt_desbloquear.setText(
                "DESBLOQUEAR"
            )

    # =========================================================
    # CARREGAR COORDENADAS
    # =========================================================

    def carregar_coordenadas(self):

        self.campos.clear()

        self.campos_maquina.clear()

        # =====================================================
        # RACK
        # =====================================================

        posicoes = (
            self.db.listar_coordenadas()
        )

        self.tabela.setRowCount(
            len(posicoes)
        )

        for linha, posicao in enumerate(
            posicoes
        ):

            endereco = posicao[0]

            x = posicao[1]
            y = posicao[2]
            z = posicao[3]

            item = QTableWidgetItem(
                str(endereco)
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            self.tabela.setItem(
                linha,
                0,
                item
            )

            campo_x = self.criar_campo(
                x
            )

            self.tabela.setCellWidget(
                linha,
                1,
                campo_x
            )

            campo_y = self.criar_campo(
                y
            )

            self.tabela.setCellWidget(
                linha,
                2,
                campo_y
            )

            campo_z = self.criar_campo(
                z
            )

            self.tabela.setCellWidget(
                linha,
                3,
                campo_z
            )

            self.campos.extend(
                [
                    campo_x,
                    campo_y,
                    campo_z
                ]
            )

        # =====================================================
        # POSIÇÕES DA MÁQUINA
        # =====================================================

        posicoes_maquina = (
            self.db.listar_posicoes_maquina()
        )

        self.tabela_maquina.setRowCount(
            len(self.POSICOES_MAQUINA)
        )

        for linha, nome in enumerate(
            self.POSICOES_MAQUINA
        ):

            dados = None

            for registro in posicoes_maquina:

                if registro[0] == nome:

                    dados = registro

                    break

            if dados is not None:

                x = dados[1]
                y = dados[2]
                z = dados[3]

            else:

                x = 0.0
                y = 0.0
                z = 0.0

            item = QTableWidgetItem(
                nome
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            self.tabela_maquina.setItem(
                linha,
                0,
                item
            )

            campo_x = self.criar_campo(
                x
            )

            self.tabela_maquina.setCellWidget(
                linha,
                1,
                campo_x
            )

            campo_y = self.criar_campo(
                y
            )

            self.tabela_maquina.setCellWidget(
                linha,
                2,
                campo_y
            )

            campo_z = self.criar_campo(
                z
            )

            self.tabela_maquina.setCellWidget(
                linha,
                3,
                campo_z
            )

            self.campos_maquina.extend(
                [
                    campo_x,
                    campo_y,
                    campo_z
                ]
            )

        # =====================================================
        # CONFIGURAÇÕES
        # =====================================================

        z_levantar = (
            self.db.obter_configuracao_empilhadeira(
                "Z_LEVANTAR"
            )
        )

        z_apoiar = (
            self.db.obter_configuracao_empilhadeira(
                "Z_APOIAR"
            )
        )

        if z_levantar is not None:

            self.campo_z_levantar.setValue(
                z_levantar
            )

        if z_apoiar is not None:

            self.campo_z_apoiar.setValue(
                z_apoiar
            )

        self.ajustar_alturas_tabelas()

    # =========================================================
    # ALTURAS DAS TABELAS
    # =========================================================

    def ajustar_alturas_tabelas(self):

        altura_rack = (
            self.tabela.horizontalHeader().height()
        )

        altura_rack += (
            self.tabela.rowCount()
            *
            self.tabela.verticalHeader().defaultSectionSize()
        )

        self.tabela.setFixedHeight(
            altura_rack + 4
        )

        altura_maquina = (
            self.tabela_maquina.horizontalHeader().height()
        )

        altura_maquina += (
            self.tabela_maquina.rowCount()
            *
            self.tabela_maquina.verticalHeader().defaultSectionSize()
        )

        self.tabela_maquina.setFixedHeight(
            altura_maquina + 4
        )

    # =========================================================
    # SALVAR COORDENADAS
    # =========================================================

    def salvar_coordenadas(self):

        if not self.acesso_liberado:

            QMessageBox.warning(
                self,
                "Acesso bloqueado",
                "Desbloqueie a edição antes de salvar."
            )

            return

        # =====================================================
        # RACK
        # =====================================================

        for linha in range(
            self.tabela.rowCount()
        ):

            item = self.tabela.item(
                linha,
                0
            )

            if item is None:

                continue

            endereco = item.text()

            campo_x = self.tabela.cellWidget(
                linha,
                1
            )

            campo_y = self.tabela.cellWidget(
                linha,
                2
            )

            campo_z = self.tabela.cellWidget(
                linha,
                3
            )

            if (
                campo_x is None
                or
                campo_y is None
                or
                campo_z is None
            ):

                continue

            self.db.salvar_coordenadas(
                endereco,
                campo_x.value(),
                campo_y.value(),
                campo_z.value()
            )

        # =====================================================
        # POSIÇÕES DA MÁQUINA
        # =====================================================

        for linha, nome in enumerate(
            self.POSICOES_MAQUINA
        ):

            campo_x = self.tabela_maquina.cellWidget(
                linha,
                1
            )

            campo_y = self.tabela_maquina.cellWidget(
                linha,
                2
            )

            campo_z = self.tabela_maquina.cellWidget(
                linha,
                3
            )

            if (
                campo_x is None
                or
                campo_y is None
                or
                campo_z is None
            ):

                continue

            self.db.salvar_posicao_maquina(
                nome,
                campo_x.value(),
                campo_y.value(),
                campo_z.value()
            )

        # =====================================================
        # CONFIGURAÇÕES
        # =====================================================

        self.db.salvar_configuracao_empilhadeira(
            "Z_LEVANTAR",
            self.campo_z_levantar.value()
        )

        self.db.salvar_configuracao_empilhadeira(
            "Z_APOIAR",
            self.campo_z_apoiar.value()
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Coordenadas salvas com sucesso."
        )

        self.carregar_coordenadas()

    # =========================================================
    # ATUALIZAR
    # =========================================================

    def atualizar(self):

        self.carregar_coordenadas()
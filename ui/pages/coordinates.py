"""
=========================================================
 Smart Rack Monitoring
---------------------------------------------------------
 Arquivo.....: coordinates.py
 Descrição...: Configuração das coordenadas do Rack
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
    QMessageBox,
    QDoubleSpinBox,
    QDialog,
    QLineEdit,
    QFrame,
    QFormLayout,
    QScrollArea,
    QSizePolicy
)

from PySide6.QtCore import Qt

from database import Database


class PasswordDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Acesso Restrito"
        )

        self.setModal(
            True
        )

        self.setMinimumWidth(
            350
        )

        self.criar_interface()


    # =====================================
    # INTERFACE DO DIÁLOGO
    # =====================================

    def criar_interface(self):

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            25,
            25,
            25,
            25
        )

        layout.setSpacing(
            15
        )

        titulo = QLabel(
            "ACESSO RESTRITO"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        titulo.setObjectName(
            "title"
        )

        mensagem = QLabel(
            "Digite a senha para acessar\n"
            "as coordenadas do Rack."
        )

        mensagem.setAlignment(
            Qt.AlignCenter
        )

        self.senha = QLineEdit()

        self.senha.setEchoMode(
            QLineEdit.Password
        )

        self.senha.setPlaceholderText(
            "Senha"
        )

        self.senha.setMinimumHeight(
            40
        )

        botoes = QHBoxLayout()

        cancelar = QPushButton(
            "Cancelar"
        )

        entrar = QPushButton(
            "Entrar"
        )

        cancelar.setObjectName(
            "actionButton"
        )

        entrar.setObjectName(
            "actionButton"
        )

        cancelar.setMinimumHeight(
            40
        )

        entrar.setMinimumHeight(
            40
        )

        botoes.addWidget(
            cancelar
        )

        botoes.addWidget(
            entrar
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            mensagem
        )

        layout.addWidget(
            self.senha
        )

        layout.addLayout(
            botoes
        )

        cancelar.clicked.connect(
            self.reject
        )

        entrar.clicked.connect(
            self.accept
        )

        self.senha.returnPressed.connect(
            self.accept
        )

        self.senha.setFocus()


    # =====================================
    # OBTER SENHA
    # =====================================

    def obter_senha(self):

        return self.senha.text()


class CoordinatesPage(QWidget):

    # =================================================
    # CONFIGURAÇÃO
    # =================================================

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

        self.campos = {}

        self.campos_maquina = {}

        self.criar_interface()


    # =================================================
    # INTERFACE
    # =================================================

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

        # =================================================
        # SCROLL ÚNICO DA ABA
        # =================================================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        scroll.setFrameShape(
            QFrame.NoFrame
        )

        # =================================================
        # CONTEÚDO DA ABA
        # =================================================

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

        # =============================================
        # TÍTULO
        # =============================================

        titulo = QLabel(
            "COORDENADAS DO RACK"
        )

        titulo.setObjectName(
            "title"
        )

        self.layout_principal.addWidget(
            titulo
        )

        # =============================================
        # STATUS
        # =============================================

        self.status = QLabel(
            "Acesso restrito."
        )

        self.status.setObjectName(
            "offline"
        )

        self.layout_principal.addWidget(
            self.status
        )

        # =============================================
        # TABELA DO RACK
        # =============================================

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

        self.tabela.setAlternatingRowColors(
            True
        )

        self.tabela.verticalHeader().setVisible(
            False
        )

        # ---------------------------------------------
        # REMOVER ROLAGEM INTERNA
        # ---------------------------------------------

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

        cabecalho = self.tabela.horizontalHeader()

        cabecalho.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        cabecalho.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        cabecalho.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        cabecalho.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        self.layout_principal.addWidget(
            self.tabela
        )

        # =============================================
        # POSIÇÕES DA EMPILHADEIRA
        # =============================================

        maquina_box = QFrame()

        maquina_box.setObjectName(
            "controlBox"
        )

        maquina_layout = QVBoxLayout(
            maquina_box
        )

        maquina_titulo = QLabel(
            "POSIÇÕES DA EMPILHADEIRA"
        )

        maquina_titulo.setObjectName(
            "rackTitle"
        )

        maquina_layout.addWidget(
            maquina_titulo
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

        self.tabela_maquina.setAlternatingRowColors(
            True
        )

        self.tabela_maquina.verticalHeader().setVisible(
            False
        )

        # ---------------------------------------------
        # REMOVER ROLAGEM INTERNA
        # ---------------------------------------------

        self.tabela_maquina.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela_maquina.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela_maquina.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Fixed
        )

        cabecalho_maquina = (
            self.tabela_maquina.horizontalHeader()
        )

        cabecalho_maquina.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents
        )

        cabecalho_maquina.setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        cabecalho_maquina.setSectionResizeMode(
            2,
            QHeaderView.Stretch
        )

        cabecalho_maquina.setSectionResizeMode(
            3,
            QHeaderView.Stretch
        )

        maquina_layout.addWidget(
            self.tabela_maquina
        )

        self.layout_principal.addWidget(
            maquina_box
        )

        # =============================================
        # AJUSTES DA EMPILHADEIRA
        # =============================================

        ajuste_box = QFrame()

        ajuste_box.setObjectName(
            "controlBox"
        )

        ajuste_layout = QVBoxLayout(
            ajuste_box
        )

        ajuste_titulo = QLabel(
            "AJUSTES DA EMPILHADEIRA"
        )

        ajuste_titulo.setObjectName(
            "rackTitle"
        )

        ajuste_layout.addWidget(
            ajuste_titulo
        )

        formulario = QFormLayout()

        formulario.setSpacing(
            10
        )

        # ---------------------------------------------
        # Z LEVANTAR
        # ---------------------------------------------

        self.campo_z_levantar = QDoubleSpinBox()

        self.campo_z_levantar.setDecimals(
            3
        )

        self.campo_z_levantar.setRange(
            0.0,
            99999.999
        )

        self.campo_z_levantar.setSingleStep(
            1.0
        )

        self.campo_z_levantar.setSuffix(
            " mm"
        )

        self.campo_z_levantar.setAlignment(
            Qt.AlignCenter
        )

        formulario.addRow(
            "Subir para levantar pallet:",
            self.campo_z_levantar
        )

        # ---------------------------------------------
        # Z APOIAR
        # ---------------------------------------------

        self.campo_z_apoiar = QDoubleSpinBox()

        self.campo_z_apoiar.setDecimals(
            3
        )

        self.campo_z_apoiar.setRange(
            0.0,
            99999.999
        )

        self.campo_z_apoiar.setSingleStep(
            1.0
        )

        self.campo_z_apoiar.setSuffix(
            " mm"
        )

        self.campo_z_apoiar.setAlignment(
            Qt.AlignCenter
        )

        formulario.addRow(
            "Descer para apoiar pallet:",
            self.campo_z_apoiar
        )

        ajuste_layout.addLayout(
            formulario
        )

        self.layout_principal.addWidget(
            ajuste_box
        )

        # =============================================
        # BOTÕES
        # =============================================

        botoes = QHBoxLayout()

        self.bt_entrar = QPushButton(
            "Desbloquear"
        )

        self.bt_salvar = QPushButton(
            "Salvar Coordenadas"
        )

        self.bt_atualizar = QPushButton(
            "Atualizar"
        )

        self.bt_entrar.setObjectName(
            "actionButton"
        )

        self.bt_salvar.setObjectName(
            "actionButton"
        )

        self.bt_atualizar.setObjectName(
            "actionButton"
        )

        botoes.addWidget(
            self.bt_entrar
        )

        botoes.addWidget(
            self.bt_salvar
        )

        botoes.addWidget(
            self.bt_atualizar
        )

        self.layout_principal.addLayout(
            botoes
        )

        self.layout_principal.addStretch()

        # =============================================
        # DEFINIR CONTEÚDO DO SCROLL
        # =============================================

        scroll.setWidget(
            conteudo
        )

        layout_externo.addWidget(
            scroll
        )

        # =============================================
        # EVENTOS
        # =============================================

        self.bt_entrar.clicked.connect(
            self.solicitar_senha
        )

        self.bt_salvar.clicked.connect(
            self.salvar_coordenadas
        )

        self.bt_atualizar.clicked.connect(
            self.carregar_coordenadas
        )

        # =============================================
        # ESTADO INICIAL
        # =============================================

        self.tabela.setEnabled(
            False
        )

        self.tabela_maquina.setEnabled(
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

        self.carregar_coordenadas()


    # =================================================
    # AJUSTAR ALTURA DA TABELA
    # =================================================

    def ajustar_altura_tabela(
        self,
        tabela
    ):

        tabela.resizeRowsToContents()

        altura_header = (
            tabela.horizontalHeader().height()
        )

        altura_linhas = sum(
            tabela.rowHeight(i)
            for i in range(
                tabela.rowCount()
            )
        )

        altura_bordas = (
            tabela.frameWidth() * 2
        )

        altura_scroll = (
            2
        )

        altura_total = (
            altura_header
            + altura_linhas
            + altura_bordas
            + altura_scroll
        )

        tabela.setFixedHeight(
            altura_total
        )


    # =================================================
    # CARREGAR COORDENADAS
    # =================================================

    def carregar_coordenadas(self):

        # =============================================
        # COORDENADAS DO RACK
        # =============================================

        dados = self.db.listar_coordenadas()

        self.tabela.setRowCount(
            len(dados)
        )

        self.campos.clear()

        for linha, registro in enumerate(
            dados
        ):

            endereco = registro[0]

            x = float(
                registro[1] or 0.0
            )

            y = float(
                registro[2] or 0.0
            )

            z = float(
                registro[3] or 0.0
            )

            item = QTableWidgetItem(
                endereco
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            item.setFlags(
                item.flags()
                & ~Qt.ItemIsEditable
            )

            self.tabela.setItem(
                linha,
                0,
                item
            )

            campo_x = self.criar_campo(
                x
            )

            campo_y = self.criar_campo(
                y
            )

            campo_z = self.criar_campo(
                z
            )

            self.tabela.setCellWidget(
                linha,
                1,
                campo_x
            )

            self.tabela.setCellWidget(
                linha,
                2,
                campo_y
            )

            self.tabela.setCellWidget(
                linha,
                3,
                campo_z
            )

            self.campos[endereco] = (
                campo_x,
                campo_y,
                campo_z
            )

        # =============================================
        # AJUSTAR ALTURA DA TABELA DO RACK
        # =============================================

        self.ajustar_altura_tabela(
            self.tabela
        )

        # =============================================
        # COORDENADAS DA EMPILHADEIRA
        # =============================================

        dados_maquina = (
            self.db.listar_posicoes_maquina()
        )

        self.campos_maquina.clear()

        mapa_maquina = {
            registro[0]: registro
            for registro in dados_maquina
        }

        self.tabela_maquina.setRowCount(
            len(self.POSICOES_MAQUINA)
        )

        for linha, nome in enumerate(
            self.POSICOES_MAQUINA
        ):

            registro = mapa_maquina.get(
                nome
            )

            if registro is None:

                x = 0.0
                y = 0.0
                z = 0.0

            else:

                x = float(
                    registro[1] or 0.0
                )

                y = float(
                    registro[2] or 0.0
                )

                z = float(
                    registro[3] or 0.0
                )

            item = QTableWidgetItem(
                nome
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            item.setFlags(
                item.flags()
                & ~Qt.ItemIsEditable
            )

            self.tabela_maquina.setItem(
                linha,
                0,
                item
            )

            campo_x = self.criar_campo(
                x
            )

            campo_y = self.criar_campo(
                y
            )

            campo_z = self.criar_campo(
                z
            )

            self.tabela_maquina.setCellWidget(
                linha,
                1,
                campo_x
            )

            self.tabela_maquina.setCellWidget(
                linha,
                2,
                campo_y
            )

            self.tabela_maquina.setCellWidget(
                linha,
                3,
                campo_z
            )

            self.campos_maquina[nome] = (
                campo_x,
                campo_y,
                campo_z
            )

        # =============================================
        # AJUSTAR ALTURA DA TABELA DA MÁQUINA
        # =============================================

        self.ajustar_altura_tabela(
            self.tabela_maquina
        )

        # =============================================
        # CONFIGURAÇÕES
        # =============================================

        self.carregar_configuracoes()


    # =================================================
    # CARREGAR CONFIGURAÇÕES
    # =================================================

    def carregar_configuracoes(self):

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


    # =================================================
    # CRIAR CAMPO
    # =================================================

    def criar_campo(
        self,
        valor
    ):

        campo = QDoubleSpinBox()

        campo.setDecimals(
            3
        )

        campo.setRange(
            -99999.999,
            99999.999
        )

        campo.setSingleStep(
            1.0
        )

        campo.setValue(
            valor
        )

        campo.setAlignment(
            Qt.AlignCenter
        )

        return campo


    # =================================================
    # SENHA
    # =================================================

    def solicitar_senha(self):

        print(
            "Abrindo tela de senha..."
        )

        if self.acesso_liberado:

            self.bloquear()

            return

        dialogo = PasswordDialog(
            self
        )

        resultado = dialogo.exec()

        if resultado != QDialog.Accepted:

            return

        senha = dialogo.obter_senha()

        if senha == self.SENHA:

            self.acesso_liberado = True

            self.tabela.setEnabled(
                True
            )

            self.tabela_maquina.setEnabled(
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

            self.bt_entrar.setText(
                "Bloquear"
            )

            self.status.setObjectName(
                "online"
            )

            self.status.setText(
                "Acesso autorizado."
            )

            self.atualizar_estilo_status()

        else:

            QMessageBox.warning(
                self,
                "Acesso negado",
                "Senha incorreta."
            )


    # =================================================
    # BLOQUEAR
    # =================================================

    def bloquear(self):

        self.acesso_liberado = False

        self.tabela.setEnabled(
            False
        )

        self.tabela_maquina.setEnabled(
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

        self.bt_entrar.setText(
            "Desbloquear"
        )

        self.status.setObjectName(
            "offline"
        )

        self.status.setText(
            "Acesso restrito."
        )

        self.atualizar_estilo_status()


    # =================================================
    # ATUALIZAR ESTILO
    # =================================================

    def atualizar_estilo_status(self):

        self.status.style().unpolish(
            self.status
        )

        self.status.style().polish(
            self.status
        )

        self.status.update()


    # =================================================
    # SALVAR COORDENADAS
    # =================================================

    def salvar_coordenadas(self):

        if not self.acesso_liberado:

            QMessageBox.warning(
                self,
                "Acesso restrito",
                "Desbloqueie a página antes de salvar."
            )

            return

        erros = []

        # =============================================
        # SALVAR RACK
        # =============================================

        for endereco, campos in self.campos.items():

            campo_x = campos[0]
            campo_y = campos[1]
            campo_z = campos[2]

            x = campo_x.value()
            y = campo_y.value()
            z = campo_z.value()

            sucesso = self.db.salvar_coordenadas(
                endereco,
                x,
                y,
                z
            )

            if not sucesso:

                erros.append(
                    endereco
                )

        # =============================================
        # SALVAR POSIÇÕES DA EMPILHADEIRA
        # =============================================

        for nome, campos in self.campos_maquina.items():

            campo_x = campos[0]
            campo_y = campos[1]
            campo_z = campos[2]

            x = campo_x.value()
            y = campo_y.value()
            z = campo_z.value()

            sucesso = self.db.salvar_posicao_maquina(
                nome,
                x,
                y,
                z
            )

            if not sucesso:

                erros.append(
                    nome
                )

        # =============================================
        # SALVAR AJUSTES DA EMPILHADEIRA
        # =============================================

        sucesso_levantar = (
            self.db.salvar_configuracao_empilhadeira(
                "Z_LEVANTAR",
                self.campo_z_levantar.value()
            )
        )

        sucesso_apoiar = (
            self.db.salvar_configuracao_empilhadeira(
                "Z_APOIAR",
                self.campo_z_apoiar.value()
            )
        )

        if not sucesso_levantar:

            erros.append(
                "Z_LEVANTAR"
            )

        if not sucesso_apoiar:

            erros.append(
                "Z_APOIAR"
            )

        # =============================================
        # RESULTADO
        # =============================================

        if erros:

            QMessageBox.critical(
                self,
                "Erro",
                "Não foi possível salvar:\n"
                + ", ".join(erros)
            )

            return

        QMessageBox.information(
            self,
            "Salvo",
            (
                "Coordenadas e ajustes "
                "salvos com sucesso."
            )
        )

        self.status.setText(
            "Coordenadas e ajustes salvos."
        )


    # =================================================
    # ATUALIZAR
    # =================================================

    def atualizar(self):

        self.carregar_coordenadas()
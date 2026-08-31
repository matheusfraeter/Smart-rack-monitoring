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
    QLineEdit
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


    def __init__(self):

        super().__init__()

        self.db = Database()

        self.acesso_liberado = False

        self.campos = {}

        self.criar_interface()


    # =================================================
    # INTERFACE
    # =================================================

    def criar_interface(self):

        self.layout_principal = QVBoxLayout(
            self
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
        # TABELA
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


        self.bt_salvar.setEnabled(
            False
        )


        self.carregar_coordenadas()


    # =================================================
    # CARREGAR COORDENADAS
    # =================================================

    def carregar_coordenadas(self):

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


            # -----------------------------------------
            # CÉLULA
            # -----------------------------------------

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


            # -----------------------------------------
            # X Y Z
            # -----------------------------------------

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
            "Coordenadas salvas com sucesso."
        )


        self.status.setText(
            "Coordenadas salvas."
        )


    # =================================================
    # ATUALIZAR
    # =================================================

    def atualizar(self):

        self.carregar_coordenadas()
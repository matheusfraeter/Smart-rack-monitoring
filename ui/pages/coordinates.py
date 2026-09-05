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
)

from PySide6.QtCore import (
    Qt,
    QTimer,
)

from PySide6.QtGui import (
    QGuiApplication,
)

from database import Database


# =========================================================
# DIÁLOGO DE SENHA
# =========================================================

class PasswordDialog(QDialog):

    def __init__(
        self,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.setWindowTitle(
            "Acesso"
        )

        self.setModal(
            True
        )

        self.setMinimumWidth(
            300
        )

        layout = QVBoxLayout(
            self
        )

        # =====================================
        # TÍTULO
        # =====================================

        titulo = QLabel(
            "Digite a senha para desbloquear:"
        )

        titulo.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            titulo
        )

        # =====================================
        # SENHA
        # =====================================

        self.campo_senha = QLineEdit()

        self.campo_senha.setEchoMode(
            QLineEdit.Password
        )

        self.campo_senha.setAlignment(
            Qt.AlignCenter
        )

        self.campo_senha.setInputMethodHints(
            Qt.ImhPreferNumbers
        )

        layout.addWidget(
            self.campo_senha
        )

        # =====================================
        # BOTÕES
        # =====================================

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
            botoes
        )

        self.campo_senha.returnPressed.connect(
            self.accept
        )

        # =====================================
        # FOCO AUTOMÁTICO
        # =====================================

        self.campo_senha.setFocus()

        self.campo_senha.selectAll()

        # =====================================
        # TENTAR ABRIR TECLADO
        # =====================================

        QTimer.singleShot(
            200,
            self.abrir_teclado
        )

    # =====================================================
    # TECLADO VIRTUAL
    # =====================================================

    def abrir_teclado(self):

        try:

            QGuiApplication.inputMethod().show()

        except Exception:

            pass

    # =====================================================
    # SENHA
    # =====================================================

    def senha(self):

        return self.campo_senha.text()


# =========================================================
# DIÁLOGO DE EDIÇÃO
# =========================================================

class EditValueDialog(QDialog):

    def __init__(
        self,
        valor,
        titulo="Alterar valor",
        decimais=3,
        minimo=-99999.999,
        maximo=99999.999,
        parent=None
    ):

        super().__init__(
            parent
        )

        self.decimais = decimais
        self.minimo = minimo
        self.maximo = maximo

        self.setWindowTitle(
            titulo
        )

        self.setModal(
            True
        )

        self.setMinimumWidth(
            320
        )

        layout = QVBoxLayout(
            self
        )

        # =====================================
        # TÍTULO
        # =====================================

        label = QLabel(
            "Digite o novo valor:"
        )

        label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            label
        )

        # =====================================
        # CAMPO
        # =====================================

        self.campo = QLineEdit()

        self.campo.setAlignment(
            Qt.AlignCenter
        )

        self.campo.setInputMethodHints(
            Qt.ImhPreferNumbers
        )

        if self.decimais == 0:

            texto_valor = (
                f"{float(valor):.0f}"
            )

        else:

            texto_valor = (
                f"{float(valor):.{self.decimais}f}"
            )

        self.campo.setText(
            texto_valor
        )

        self.campo.selectAll()

        layout.addWidget(
            self.campo
        )

        # =====================================
        # BOTÕES
        # =====================================

        botoes = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        botoes.accepted.connect(
            self.validar
        )

        botoes.rejected.connect(
            self.reject
        )

        layout.addWidget(
            botoes
        )

        self.campo.returnPressed.connect(
            self.validar
        )

        # =====================================
        # FOCO
        # =====================================

        self.campo.setFocus()

        # =====================================
        # TECLADO VIRTUAL
        # =====================================

        QTimer.singleShot(
            200,
            self.abrir_teclado
        )

    # =====================================================
    # ABRIR TECLADO VIRTUAL
    # =====================================================

    def abrir_teclado(self):

        try:

            QGuiApplication.inputMethod().show()

        except Exception:

            pass

    # =====================================================
    # VALIDAR
    # =====================================================

    def validar(self):

        texto = (
            self.campo.text()
            .strip()
            .replace(
                ",",
                "."
            )
        )

        if not texto:

            QMessageBox.warning(
                self,
                "Valor inválido",
                "Digite um valor."
            )

            self.campo.setFocus()

            return

        try:

            valor = float(
                texto
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Valor inválido",
                "Digite um número válido."
            )

            self.campo.setFocus()

            self.campo.selectAll()

            return

        if valor < self.minimo:

            QMessageBox.warning(
                self,
                "Valor inválido",
                (
                    f"O valor mínimo permitido é "
                    f"{self.minimo}."
                )
            )

            self.campo.setFocus()

            self.campo.selectAll()

            return

        if valor > self.maximo:

            QMessageBox.warning(
                self,
                "Valor inválido",
                (
                    f"O valor máximo permitido é "
                    f"{self.maximo}."
                )
            )

            self.campo.setFocus()

            self.campo.selectAll()

            return

        self.accept()

    # =====================================================
    # VALOR
    # =====================================================

    def valor(self):

        return float(
            self.campo.text()
            .strip()
            .replace(
                ",",
                "."
            )
        )


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

        # =====================================
        # BANCO
        # =====================================

        self.db = Database()

        # =====================================
        # ACESSO
        # =====================================

        self.acesso_liberado = False

        self.criar_interface()

        # =====================================
        # EVENTOS DAS TABELAS
        # =====================================

        self.tabela.cellClicked.connect(
            self.editar_celula_rack
        )

        self.tabela_maquina.cellClicked.connect(
            self.editar_celula_maquina
        )

        self.tabela_configuracoes.cellClicked.connect(
            self.editar_celula_configuracao
        )

        # =====================================
        # CARREGAR
        # =====================================

        self.carregar_coordenadas()

        self.bloquear()

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

        # =================================================
        # SCROLL
        # =================================================

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

        # =================================================
        # CONTEÚDO
        # =================================================

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

        # =================================================
        # TÍTULO
        # =================================================

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

        # =================================================
        # TABELA DO RACK
        # =================================================

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
            QAbstractItemView.SingleSelection
        )

        self.tabela.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela.setSizeAdjustPolicy(
            QAbstractItemView.AdjustToContents
        )

        for coluna in range(4):

            self.tabela.horizontalHeader().setSectionResizeMode(
                coluna,
                QHeaderView.Stretch
            )

        self.layout_conteudo.addWidget(
            self.tabela
        )

        # =================================================
        # POSIÇÕES DA EMPILHADEIRA
        # =================================================

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

        self.tabela_maquina.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.tabela_maquina.setSelectionMode(
            QAbstractItemView.SingleSelection
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

        self.layout_conteudo.addWidget(
            self.tabela_maquina
        )

        # =================================================
        # AJUSTES
        # =================================================

        titulo_ajustes = QLabel(
            "AJUSTES DA EMPILHADEIRA"
        )

        titulo_ajustes.setAlignment(
            Qt.AlignCenter
        )

        self.layout_conteudo.addWidget(
            titulo_ajustes
        )

        self.tabela_configuracoes = QTableWidget()

        self.tabela_configuracoes.setColumnCount(
            2
        )

        self.tabela_configuracoes.setHorizontalHeaderLabels(
            [
                "Configuração",
                "Valor"
            ]
        )

        self.tabela_configuracoes.setRowCount(
            5
        )

        self.tabela_configuracoes.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.tabela_configuracoes.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.tabela_configuracoes.setVerticalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela_configuracoes.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

        self.tabela_configuracoes.horizontalHeader().setSectionResizeMode(
            0,
            QHeaderView.Stretch
        )

        self.tabela_configuracoes.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        nomes_configuracoes = [
            "Z LEVANTAR",
            "Z APOIAR",
            "VELOCIDADE X",
            "VELOCIDADE Y",
            "VELOCIDADE Z"
        ]

        for linha, nome in enumerate(
            nomes_configuracoes
        ):

            item = QTableWidgetItem(
                nome
            )

            item.setTextAlignment(
                Qt.AlignCenter
            )

            self.tabela_configuracoes.setItem(
                linha,
                0,
                item
            )

        self.layout_conteudo.addWidget(
            self.tabela_configuracoes
        )

        # =================================================
        # BOTÕES
        # =================================================

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

        # =================================================
        # CONEXÕES
        # =================================================

        self.bt_desbloquear.clicked.connect(
            self.alternar_bloqueio
        )

        self.bt_salvar.clicked.connect(
            self.salvar_coordenadas
        )

        self.bt_atualizar.clicked.connect(
            self.carregar_coordenadas
        )

    # =========================================================
    # CRIAR ITEM NUMÉRICO
    # =========================================================

    def criar_item_numero(
        self,
        valor,
        decimais=3
    ):

        item = QTableWidgetItem()

        if decimais == 0:

            item.setText(
                f"{float(valor):.0f}"
            )

        else:

            item.setText(
                f"{float(valor):.{decimais}f}"
            )

        item.setTextAlignment(
            Qt.AlignCenter
        )

        return item

    # =========================================================
    # GARANTIR ACESSO
    # =========================================================

    def garantir_acesso(self):

        if self.acesso_liberado:

            return True

        self.solicitar_senha()

        return self.acesso_liberado

    # =========================================================
    # EDITAR CÉLULA DO RACK
    # =========================================================

    def editar_celula_rack(
        self,
        linha,
        coluna
    ):

        if coluna == 0:

            return

        if not self.garantir_acesso():

            return

        item = self.tabela.item(
            linha,
            coluna
        )

        if item is None:

            return

        self.abrir_edicao(
            item=item,
            decimais=3,
            minimo=-99999.999,
            maximo=99999.999
        )

    # =========================================================
    # EDITAR CÉLULA DA MÁQUINA
    # =========================================================

    def editar_celula_maquina(
        self,
        linha,
        coluna
    ):

        if coluna == 0:

            return

        if not self.garantir_acesso():

            return

        item = self.tabela_maquina.item(
            linha,
            coluna
        )

        if item is None:

            return

        self.abrir_edicao(
            item=item,
            decimais=3,
            minimo=-99999.999,
            maximo=99999.999
        )

    # =========================================================
    # EDITAR CONFIGURAÇÃO
    # =========================================================

    def editar_celula_configuracao(
        self,
        linha,
        coluna
    ):

        if coluna != 1:

            return

        if not self.garantir_acesso():

            return

        item = self.tabela_configuracoes.item(
            linha,
            coluna
        )

        if item is None:

            return

        # ---------------------------------------------
        # Z
        # ---------------------------------------------

        if linha in (0, 1):

            self.abrir_edicao(
                item=item,
                decimais=3,
                minimo=-99999.999,
                maximo=99999.999
            )

            return

        # ---------------------------------------------
        # VELOCIDADE
        # ---------------------------------------------

        self.abrir_edicao(
            item=item,
            decimais=0,
            minimo=1.0,
            maximo=10000.0
        )

    # =========================================================
    # ABRIR EDIÇÃO
    # =========================================================

    def abrir_edicao(
        self,
        item,
        decimais=3,
        minimo=-99999.999,
        maximo=99999.999
    ):

        try:

            valor_atual = float(
                item.text()
                .strip()
                .replace(
                    ",",
                    "."
                )
            )

        except ValueError:

            valor_atual = 0.0

        dialogo = EditValueDialog(
            valor=valor_atual,
            decimais=decimais,
            minimo=minimo,
            maximo=maximo,
            parent=self
        )

        if dialogo.exec() != QDialog.Accepted:

            return

        novo_valor = dialogo.valor()

        item.setText(
            f"{novo_valor:.{decimais}f}"
        )

        item.setTextAlignment(
            Qt.AlignCenter
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
    # SOLICITAR SENHA
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

        self.bt_desbloquear.setText(
            "BLOQUEAR"
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

        self.bt_desbloquear.setText(
            "DESBLOQUEAR"
        )

        self.bt_salvar.setEnabled(
            False
        )

        self.atualizar_estilo_status()

    # =========================================================
    # STATUS
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

        # =====================================================
        # RACK
        # =====================================================

        posicoes = (
            self.db.listar_coordenadas()
        )

        self.tabela.setRowCount(
            len(
                posicoes
            )
        )

        for linha, posicao in enumerate(
            posicoes
        ):

            endereco = posicao[0]

            x = posicao[1]
            y = posicao[2]
            z = posicao[3]

            # -----------------------------------------------
            # ENDEREÇO
            # -----------------------------------------------

            item_endereco = QTableWidgetItem(
                str(endereco)
            )

            item_endereco.setTextAlignment(
                Qt.AlignCenter
            )

            self.tabela.setItem(
                linha,
                0,
                item_endereco
            )

            # -----------------------------------------------
            # X
            # -----------------------------------------------

            self.tabela.setItem(
                linha,
                1,
                self.criar_item_numero(
                    x,
                    3
                )
            )

            # -----------------------------------------------
            # Y
            # -----------------------------------------------

            self.tabela.setItem(
                linha,
                2,
                self.criar_item_numero(
                    y,
                    3
                )
            )

            # -----------------------------------------------
            # Z
            # -----------------------------------------------

            self.tabela.setItem(
                linha,
                3,
                self.criar_item_numero(
                    z,
                    3
                )
            )

        # =====================================================
        # POSIÇÕES DA MÁQUINA
        # =====================================================

        posicoes_maquina = (
            self.db.listar_posicoes_maquina()
        )

        self.tabela_maquina.setRowCount(
            len(
                self.POSICOES_MAQUINA
            )
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

            # -----------------------------------------------
            # NOME
            # -----------------------------------------------

            item_nome = QTableWidgetItem(
                nome
            )

            item_nome.setTextAlignment(
                Qt.AlignCenter
            )

            self.tabela_maquina.setItem(
                linha,
                0,
                item_nome
            )

            # -----------------------------------------------
            # X
            # -----------------------------------------------

            self.tabela_maquina.setItem(
                linha,
                1,
                self.criar_item_numero(
                    x,
                    3
                )
            )

            # -----------------------------------------------
            # Y
            # -----------------------------------------------

            self.tabela_maquina.setItem(
                linha,
                2,
                self.criar_item_numero(
                    y,
                    3
                )
            )

            # -----------------------------------------------
            # Z
            # -----------------------------------------------

            self.tabela_maquina.setItem(
                linha,
                3,
                self.criar_item_numero(
                    z,
                    3
                )
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

        velocidade_x = (
            self.db.obter_configuracao_empilhadeira(
                "VELOCIDADE_X"
            )
        )

        velocidade_y = (
            self.db.obter_configuracao_empilhadeira(
                "VELOCIDADE_Y"
            )
        )

        velocidade_z = (
            self.db.obter_configuracao_empilhadeira(
                "VELOCIDADE_Z"
            )
        )

        valores_configuracao = [
            z_levantar if z_levantar is not None else 10.0,
            z_apoiar if z_apoiar is not None else 10.0,
            velocidade_x if velocidade_x is not None else 1000.0,
            velocidade_y if velocidade_y is not None else 1000.0,
            velocidade_z if velocidade_z is not None else 500.0,
        ]

        for linha, valor in enumerate(
            valores_configuracao
        ):

            decimais = (
                0
                if linha >= 2
                else 3
            )

            self.tabela_configuracoes.setItem(
                linha,
                1,
                self.criar_item_numero(
                    valor,
                    decimais
                )
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

        altura_configuracoes = (
            self.tabela_configuracoes.horizontalHeader().height()
        )

        altura_configuracoes += (
            self.tabela_configuracoes.rowCount()
            *
            self.tabela_configuracoes.verticalHeader().defaultSectionSize()
        )

        self.tabela_configuracoes.setFixedHeight(
            altura_configuracoes + 4
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

            item_endereco = self.tabela.item(
                linha,
                0
            )

            item_x = self.tabela.item(
                linha,
                1
            )

            item_y = self.tabela.item(
                linha,
                2
            )

            item_z = self.tabela.item(
                linha,
                3
            )

            if (
                item_endereco is None
                or
                item_x is None
                or
                item_y is None
                or
                item_z is None
            ):

                continue

            try:

                endereco = item_endereco.text()

                x = float(
                    item_x.text()
                    .replace(
                        ",",
                        "."
                    )
                )

                y = float(
                    item_y.text()
                    .replace(
                        ",",
                        "."
                    )
                )

                z = float(
                    item_z.text()
                    .replace(
                        ",",
                        "."
                    )
                )

            except ValueError:

                continue

            self.db.salvar_coordenadas(
                endereco,
                x,
                y,
                z
            )

        # =====================================================
        # POSIÇÕES DA MÁQUINA
        # =====================================================

        for linha, nome in enumerate(
            self.POSICOES_MAQUINA
        ):

            item_x = self.tabela_maquina.item(
                linha,
                1
            )

            item_y = self.tabela_maquina.item(
                linha,
                2
            )

            item_z = self.tabela_maquina.item(
                linha,
                3
            )

            if (
                item_x is None
                or
                item_y is None
                or
                item_z is None
            ):

                continue

            try:

                x = float(
                    item_x.text()
                    .replace(
                        ",",
                        "."
                    )
                )

                y = float(
                    item_y.text()
                    .replace(
                        ",",
                        "."
                    )
                )

                z = float(
                    item_z.text()
                    .replace(
                        ",",
                        "."
                    )
                )

            except ValueError:

                continue

            self.db.salvar_posicao_maquina(
                nome,
                x,
                y,
                z
            )

        # =====================================================
        # CONFIGURAÇÕES
        # =====================================================

        try:

            valores = []

            for linha in range(5):

                item = (
                    self.tabela_configuracoes.item(
                        linha,
                        1
                    )
                )

                if item is None:

                    raise ValueError

                valor = float(
                    item.text()
                    .replace(
                        ",",
                        "."
                    )
                )

                valores.append(
                    valor
                )

            (
                valor_z_levantar,
                valor_z_apoiar,
                valor_velocidade_x,
                valor_velocidade_y,
                valor_velocidade_z
            ) = valores

        except ValueError:

            QMessageBox.warning(
                self,
                "Valores inválidos",
                "Existe alguma configuração com valor inválido."
            )

            return

        # =====================================
        # LIMITES
        # =====================================

        valor_velocidade_x = max(
            1.0,
            min(
                10000.0,
                valor_velocidade_x
            )
        )

        valor_velocidade_y = max(
            1.0,
            min(
                10000.0,
                valor_velocidade_y
            )
        )

        valor_velocidade_z = max(
            1.0,
            min(
                10000.0,
                valor_velocidade_z
            )
        )

        # =====================================================
        # SALVAR
        # =====================================================

        self.db.salvar_configuracao_empilhadeira(
            "Z_LEVANTAR",
            valor_z_levantar
        )

        self.db.salvar_configuracao_empilhadeira(
            "Z_APOIAR",
            valor_z_apoiar
        )

        self.db.salvar_configuracao_empilhadeira(
            "VELOCIDADE_X",
            valor_velocidade_x
        )

        self.db.salvar_configuracao_empilhadeira(
            "VELOCIDADE_Y",
            valor_velocidade_y
        )

        self.db.salvar_configuracao_empilhadeira(
            "VELOCIDADE_Z",
            valor_velocidade_z
        )

        QMessageBox.information(
            self,
            "Sucesso",
            "Coordenadas e velocidades salvas com sucesso."
        )

        self.carregar_coordenadas()

    # =========================================================
    # ATUALIZAR
    # =========================================================

    def atualizar(self):

        self.carregar_coordenadas()